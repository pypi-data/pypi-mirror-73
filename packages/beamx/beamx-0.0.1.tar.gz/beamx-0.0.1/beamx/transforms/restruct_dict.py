from apache_beam.transforms import DoFn
from apache_beam.transforms import ParDo
from apache_beam.transforms import PTransform

__all__ = ['RestructDictFn', 'RestructDict']


class RestructDictFn(DoFn):
  def __init__(self, mappings):
    super().__init__()
    self.mappings = mappings

  def _get_data(self, d, path):
    for k in path.split('.'):
      d = d[k]
    return d

  def _set_data(self, d, path, value):
    p = path.split('.')
    for k in p[:-1]:
      if k not in d:
        d[k] = dict()
      d = d[k]
    d[p[-1]] = value

  def process(self, x):
    d = dict()
    for org, exp in self.mappings.items():
      if exp is None or exp is False:
        continue
      v = self._get_data(x, org)
      if exp is True:
        self._set_data(d, org, v)
      elif type(exp) is str:
        self._set_data(d, exp, v)
      else:
        raise Exception(f'unexpected filter type: {type(exp)}')
    yield d


class RestructDict(PTransform):
  def __init__(self, *args, **kwargs):
    super().__init__()
    self._fn = RestructDictFn(*args, **kwargs)

  def expand(self, pvalue):
    return pvalue | ParDo(self._fn)
