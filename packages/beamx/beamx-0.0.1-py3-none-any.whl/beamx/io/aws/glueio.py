import boto3
import pyorc
from apache_beam.io.filesystem import CompressionTypes
#import botocore.exceptions as botoerror
from beamx.io import FileSource
from beamx.reader import TupleToDictReader
from beamx.reader import OrcReader

__all__ = ['GlueCatalogSource', 'GlueTableReader', 'default_reader_resolver']


def default_reader_resolver(serde, column_names, column_indices):
  if serde == 'org.apache.hadoop.hive.ql.io.orc.OrcSerde':
    return TupleToDictReader(
        column_names,
        OrcReader(
            pyorc_options={
                'struct_repr': pyorc.StructRepr.TUPLE,
                'column_indices': column_indices,
            }))


def as_glue_type(rep, data):
  if rep == 'string':
    return str(data)
  elif rep == 'bigint':
    return int(data)
  else:
    raise


class GlueTableReader():
  def __init__(self, partition_keys, reader):
    self.partition_keys = partition_keys
    self.reader = reader
    self.limit = None

  @property
  def batched(self):
    return False

  def _inject(self, x, pvs):
    for p in self.partition_keys:
      pk = p['Name']
      pt = p['Type']
      x[pk] = as_glue_type(pt, pvs.get(pk))
    return x

  def read(self, ctx, file, range_tracker):
    pvs = {
        pv[0]: pv[1]
        for pv in [i.split('=') for i in ctx.path.split('/')] if len(pv) > 1
    }
    for v in self.reader.read(ctx, file, range_tracker):
      if self.reader.batched:
        for i in v:
          x = self._inject(i, pvs)
          yield x
      else:
        yield self._inject(v, pvs)


def _get_part(key, value):
  n = key['Name']
  v = value.get(n)
  if v is None:
    raise
  return f'{n}={v}'


class GlueCatalogSource(FileSource):
  """A source for reading files from Glue Catalog."""
  def __init__(
      self,
      catalog_id: str,
      database_name: str,
      table_name: str,
      partition_values,
      filename_glob='*',
      reader_resolver=None,
      aws_session=None,
      column_names=None,
      min_bundle_size=0,
      compression_type=CompressionTypes.AUTO,
      validate=True):
    """Initialize GlueCatalogSource

    Args:
      catalog_id (str):
        in many cases it is your AWS account ID. e.g.) '123456789'
      database_name (str):
        Glue Catalog Database name.
      table_name (str):
        Glue Catalog Table name.
      partiyion_values (dict[str,str]):
        required. partition values are allowed wildcard ('*').
      aws_session (boto3.Session): if None, use default AWS client.
    """
    self.filename_glob = '*' if filename_glob is None else filename_glob

    glue = (
        boto3.client('glue')
        if aws_session is None else aws_session.client('glue'))

    # no catch exceptions
    self.glue_table_metadata = glue.get_table(
        CatalogId=catalog_id, DatabaseName=database_name,
        Name=table_name)['Table']
    self.glue_table_id = '{}:{}.{}'.format(
        catalog_id,
        self.glue_table_metadata['DatabaseName'],
        self.glue_table_metadata['Name'])
    self.glue_partition_keys = self.glue_table_metadata['PartitionKeys']

    desc = self.glue_table_metadata['StorageDescriptor']
    loc = desc.get('Location')
    if loc is None or len(loc) < 1:
      raise
    if partition_values is None or len(partition_values) < 1:
      partition_values = [{}]
    file_patterns = [
        '/'.join(
            [loc.strip('/')] +
            [_get_part(k, v) for k in self.glue_partition_keys] +
            [filename_glob.strip('/')])
        for v in partition_values
    ]
    print('file patterns', file_patterns)

    self.glue_column_names = [i['Name'] for i in desc['Columns']]
    self.column_names = column_names
    self.column_indices = []
    if column_names is None:
      self.columns_names = self.glue_column_names
    for c in column_names:
      self.column_indices.append(self.glue_column_names.index(c))  # ValueError

    serdei = desc.get('SerdeInfo')
    if serdei is None:
      raise
    serde = serdei.get('SerializationLibrary')
    if serde is None:
      raise
    if reader_resolver is None:
      reader_resolver = default_reader_resolver
    if not callable(reader_resolver):
      raise
    reader = reader_resolver(serde, self.column_names, self.column_indices)
    if reader is None:
      raise
    table_reader = GlueTableReader(self.glue_partition_keys, reader)
    super().__init__(
        file_patterns=file_patterns,
        reader=table_reader,
        min_bundle_size=min_bundle_size,
        validate=validate,
        splittable=False,
    )
