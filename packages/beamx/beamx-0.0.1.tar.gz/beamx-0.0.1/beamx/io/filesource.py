#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from dataclasses import dataclass
from apache_beam.internal import pickler
from apache_beam.io.concat_source import ConcatSource
from apache_beam.io.filesystem import CompressionTypes
from apache_beam.io.filesystems import FileSystems
from apache_beam.io.iobase import BoundedSource
from apache_beam.io.iobase import SourceBundle
from apache_beam.io.range_trackers import OffsetRangeTracker
from apache_beam.io.range_trackers import UnsplittableRangeTracker
from apache_beam.io.restriction_trackers import OffsetRange
from apache_beam.options.value_provider import StaticValueProvider
from apache_beam.options.value_provider import ValueProvider
from apache_beam.options.value_provider import check_accessible
from apache_beam.transforms.display import DisplayDataItem

__all__ = ['FileSource']


@dataclass
class ReaderContext:
  path: str


class FileSource(BoundedSource):
  def __init__(
      self,
      reader,
      file_patterns,
      min_bundle_size=0,
      compression_type=CompressionTypes.AUTO,
      splittable=True,
      validate=True):
    if not isinstance(file_patterns, ValueProvider):
      file_patterns = StaticValueProvider(list, file_patterns)
    self._patterns = file_patterns
    self._pickle_reader = pickler.dumps(reader)
    self._reader = None
    self._concat_source = None
    self._min_bundle_size = min_bundle_size
    if not CompressionTypes.is_valid_compression_type(compression_type):
      raise TypeError(
          'compression_type must be CompressionType object but '
          'was %s' % type(compression_type))
    self._compression_type = compression_type
    self._splittable = splittable
    if validate and file_patterns.is_accessible():
      self._validate()

  def display_data(self):
    return {
        'file_patterns': DisplayDataItem(
            str(self._patterns), label="File Patterns"),
        'compression': DisplayDataItem(
            str(self._compression_type), label='Compression Type')
    }

  def _get_reader(self):
    if self._reader is None:
      self._reader = pickler.loads(self._pickle_reader)
    return self._reader

  @check_accessible(['_patterns'])
  def _get_concat_source(self):
    if self._concat_source is None:
      patterns = self._patterns.get()

      single_file_sources = []
      for match_result in FileSystems.match(patterns):
        file_based_source_ref = pickler.loads(pickler.dumps(self))

        for file_metadata in match_result.metadata_list:
          file_name = file_metadata.path
          file_size = file_metadata.size_in_bytes
          if file_size == 0:
            continue  # Ignoring empty file.

          # We determine splittability of this specific file.
          splittable = (
              self.splittable and
              _determine_splittability_from_compression_type(
                  file_name, self._compression_type))

          single_file_source = _SingleFileSource(
              file_based_source_ref,
              file_name,
              0,
              file_size,
              min_bundle_size=self._min_bundle_size,
              splittable=splittable)
          single_file_sources.append(single_file_source)
      self._concat_source = ConcatSource(single_file_sources)
    return self._concat_source

  def open_file(self, file_name):
    return FileSystems.open(
        file_name,
        'application/octet-stream',
        compression_type=self._compression_type)

  @check_accessible(['_patterns'])
  def _validate(self):
    """Validate if there are actual files in the specified glob patterns
    """
    patterns = self._patterns.get()

    # Limit the responses as we only want to check if something exists
    match_result = FileSystems.match(patterns, limits=[1] * len(patterns))[0]
    if len(match_result.metadata_list) <= 0:
      raise IOError('No files found based on the file patterns %s' % patterns)

  def split(
      self, desired_bundle_size=None, start_position=None, stop_position=None):
    return self._get_concat_source().split(
        desired_bundle_size=desired_bundle_size,
        start_position=start_position,
        stop_position=stop_position)

  @check_accessible(['_patterns'])
  def estimate_size(self):
    patterns = self._patterns.get()
    match_result = FileSystems.match(patterns)[0]
    return sum([f.size_in_bytes for f in match_result.metadata_list])

  def read(self, range_tracker):
    return self._get_concat_source().read(range_tracker)

  def get_range_tracker(self, start_position, stop_position):
    return self._get_concat_source().get_range_tracker(
        start_position, stop_position)

  def read_records(self, file_name, offset_range_tracker):
    ctx = ReaderContext(file_name)
    with self.open_file(file_name) as f:
      for i in self._get_reader().read(ctx, f, offset_range_tracker):
        yield i

  @property
  def splittable(self):
    return self._splittable


def _determine_splittability_from_compression_type(file_path, compression_type):
  if compression_type == CompressionTypes.AUTO:
    compression_type = CompressionTypes.detect_compression_type(file_path)
  return compression_type == CompressionTypes.UNCOMPRESSED


class _SingleFileSource(BoundedSource):
  """Denotes a source for a specific file type."""
  def __init__(
      self,
      file_based_source,
      file_name,
      start_offset,
      stop_offset,
      min_bundle_size=0,
      splittable=True):
    if not isinstance(start_offset, int):
      raise TypeError(
          'start_offset must be a number. Received: %r' % start_offset)
    if stop_offset != OffsetRangeTracker.OFFSET_INFINITY:
      if not isinstance(stop_offset, int):
        raise TypeError(
            'stop_offset must be a number. Received: %r' % stop_offset)
      if start_offset >= stop_offset:
        raise ValueError(
            'start_offset must be smaller than stop_offset. Received %d and %d '
            'for start and stop offsets respectively' %
            (start_offset, stop_offset))

    self._file_name = file_name
    self._start_offset = start_offset
    self._stop_offset = stop_offset
    self._min_bundle_size = min_bundle_size
    self._file_based_source = file_based_source
    self._splittable = splittable

  def split(self, desired_bundle_size, start_offset=None, stop_offset=None):
    if start_offset is None:
      start_offset = self._start_offset
    if stop_offset is None:
      stop_offset = self._stop_offset

    if self._splittable:
      splits = OffsetRange(start_offset, stop_offset).split(
          desired_bundle_size, self._min_bundle_size)
      for split in splits:
        yield SourceBundle(
            split.stop - split.start,
            _SingleFileSource(
                # Copying this so that each sub-source gets a fresh instance.
                pickler.loads(pickler.dumps(self._file_based_source)),
                self._file_name,
                split.start,
                split.stop,
                min_bundle_size=self._min_bundle_size,
                splittable=self._splittable),
            split.start,
            split.stop)
    else:
      # Returning a single sub-source with end offset set to OFFSET_INFINITY (so
      # that all data of the source gets read) since this source is
      # unsplittable. Choosing size of the file as end offset will be wrong for
      # certain unsplittable source, e.g., compressed sources.
      yield SourceBundle(
          stop_offset - start_offset,
          _SingleFileSource(
              self._file_based_source,
              self._file_name,
              start_offset,
              OffsetRangeTracker.OFFSET_INFINITY,
              min_bundle_size=self._min_bundle_size,
              splittable=self._splittable),
          start_offset,
          OffsetRangeTracker.OFFSET_INFINITY)

  def estimate_size(self):
    return self._stop_offset - self._start_offset

  def get_range_tracker(self, start_position, stop_position):
    if start_position is None:
      start_position = self._start_offset
    if stop_position is None:
      # If file is unsplittable we choose OFFSET_INFINITY as the default end
      # offset so that all data of the source gets read. Choosing size of the
      # file as end offset will be wrong for certain unsplittable source, for
      # e.g., compressed sources.
      stop_position = (
          self._stop_offset
          if self._splittable else OffsetRangeTracker.OFFSET_INFINITY)

    range_tracker = OffsetRangeTracker(start_position, stop_position)
    if not self._splittable:
      range_tracker = UnsplittableRangeTracker(range_tracker)

    return range_tracker

  def read(self, range_tracker):
    return self._file_based_source.read_records(self._file_name, range_tracker)

  def default_output_coder(self):
    return self._file_based_source.default_output_coder()
