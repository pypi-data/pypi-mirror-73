import pyorc
from apache_beam.io.iobase import RangeTracker

__all__ = ['OrcReader']


class OrcReader():
  def __init__(self, pyorc_options=None):
    self.pyorc_options = pyorc_options if pyorc_options is not None else {}

  def read(self, ctx, file, range_tracker):
    pos = -1

    def split_points_unclaimed(stop_pos):
      if pos >= stop_pos:
        return 0
      return RangeTracker.SPLIT_POINTS_UNKNOWN

    range_tracker.set_split_points_unclaimed_callback(split_points_unclaimed)

    start_offset = range_tracker.start_position()
    if start_offset is None:
      start_offset = 0

    idx = 0
    reader = pyorc.Reader(file, **self.pyorc_options)
    if reader.num_of_stripes > 0:
      pos = 0
    else:
      pos = range_tracker.stop_position()

    while range_tracker.try_claim(pos):
      stripe = reader.read_stripe(idx)
      if idx + 1 < reader.num_of_stripes:
        idx = idx + 1
        pos = stripe.bytes_offset
      else:
        pos = range_tracker.stop_position()

      yield stripe.read()

  @property
  def batched(self):
    return True
