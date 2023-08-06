import pytest

from apache_beam.testing.test_pipeline import TestPipeline
from apache_beam.testing.util import assert_that
from apache_beam.testing.util import equal_to
from apache_beam.transforms import Create

from beamx.transforms import RestructDict
from beamx.transforms import RestructDictFn


class TestRestructDict():
  def test_invalid_filter_type(self):
    with pytest.raises(Exception):
      it = RestructDictFn(mappings={
          'fn': lambda x: x,
      }).process({
          'fn': 1,
      })
      for _ in it:  # pragma: no cover
        pass

  def test_run(self):
    elems = [
        {
            'a': 1,
            'b': 1,
            'c': {
                'x': 1, 'y': 1
            },
            'd': {
                'x': 1, 'y': 1
            },
            'e': 1,
            'f': 1,
            'g': 1,
            'h': 1
        },
        {
            'a': 2,
            'b': 2,
            'c': {
                'x': 2, 'y': 2
            },
            'd': {
                'x': 2, 'y': 2
            },
            'e': 2,
            'f': 2,
            'g': 2,
            'h': 2
        },
    ]
    with TestPipeline() as p:
      pc = (
          p
          | Create(elems)
          | RestructDict(
              mappings={
                  'a': 'moved_a',
                  'b': 'nested.moved_b',
                  'c.x': 'nested.moved_c_x',
                  'c.y': 'moved_c_y',
                  'd': True,
                  'e': False,
                  'f': None,
              }))
      assert_that(
          pc,
          equal_to([
              {
                  'moved_a': 1,
                  'nested': {
                      'moved_b': 1, 'moved_c_x': 1
                  },
                  'moved_c_y': 1,
                  'd': {
                      'x': 1, 'y': 1
                  }
              },
              {
                  'moved_a': 2,
                  'nested': {
                      'moved_b': 2, 'moved_c_x': 2
                  },
                  'moved_c_y': 2,
                  'd': {
                      'x': 2, 'y': 2
                  }
              },
          ]))
