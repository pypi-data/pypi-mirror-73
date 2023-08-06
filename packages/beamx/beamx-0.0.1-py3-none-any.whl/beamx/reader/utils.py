__all__ = ['TupleToDictReader']


class TupleToDictReader():
  def __init__(self, column_names, reader):
    self.column_names = column_names
    self.reader = reader

  @property
  def batched(self):
    return self.reader.batched

  def _to_dict(self, x):
    return {
        name: value
        for name, value in zip(self.column_names, x)
    }

  def read(self, ctx, file, range_tracker):
    for x in self.reader.read(ctx, file, range_tracker):
      if self.reader.batched:
        yield [self._to_dict(i) for i in x]
      else:
        yield self._to_dict(x)
