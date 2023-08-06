import tempfile

import pyorc
from apache_beam.io import Read
from apache_beam.testing.test_pipeline import TestPipeline
from apache_beam.testing.util import assert_that
from apache_beam.testing.util import equal_to

from beamx.io import FileSource
from beamx.reader import OrcReader


class TestOrcSource():
  def test_read(self):
    schema = 'struct<a:int,b:struct<x:string,y:boolean>>'
    files = []
    with tempfile.NamedTemporaryFile() as f1, \
         tempfile.NamedTemporaryFile() as f2:
      files.append(f1.name)
      with pyorc.Writer(f1, schema) as writer:
        writer.write((1, ('x', True)))
      files.append(f2.name)
      with pyorc.Writer(f2, schema) as writer:
        writer.write((2, ('y', False)))
        writer.write((3, ('z', False)))
      with TestPipeline() as p:
        pc = (
            p | Read(
                FileSource(
                    file_patterns=files,
                    reader=OrcReader(
                        pyorc_options={
                            'struct_repr': pyorc.StructRepr.DICT,
                        }))))
      assert_that(
          pc,
          equal_to([
              {
                  'a': 1,
                  'b': {
                      'x': 'x',
                      'y': True,
                  },
              },
              {
                  'a': 2,
                  'b': {
                      'x': 'y',
                      'y': False,
                  },
              },
              {
                  'a': 3,
                  'b': {
                      'x': 'z',
                      'y': False,
                  },
              },
          ]))
