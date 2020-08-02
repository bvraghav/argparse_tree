from pathlib import Path

# This may be interesting; but it is always better to
# provide an unambiguous argument instead of inspect!

class A :
  def __init__(self) :
    import inspect
    f = inspect.stack().pop(1)
    # print(f.filename)
    self.p = Path(f.filename).parent.resolve()
