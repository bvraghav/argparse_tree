from argparse import Action

## Store Action Base
## ====================================================
# Base action class: argparse._StoreAction
class StoreActionBase(Action):

  def __init__(
      self,
      option_strings,
      dest,
      nargs = None,
      const = None,
      **kwargs
  ):
    if nargs == 0:
      raise ValueError(
        'nargs for store actions must be > 0; if you '
        'have nothing to store, actions such as store '
        'true or store const may be more appropriate.'
      )

    if const is not None and nargs != OPTIONAL:
      raise ValueError(
        f'nargs must be {argparse.OPTIONAL} to supply'
        ' const.'
      )

    # kwargs = sanitize_kwargs(kwargs)

    super(StoreActionBase, self).__init__(
      option_strings = option_strings,
      dest           = dest,
      nargs          = nargs,
      const          = const,
      **kwargs
    )

  def __call__(self, parser, namespace, values,
               option_string=None):
    setattr(namespace, self.dest, values)


def sanitize_kwargs(kwargs) :
  valid_keys = {
    'option_strings',
    'dest',
    'nargs',
    'const',
    'default',
    'type',
    'choices',
    'required',
    'help',
    'metavar',
  }

  return {
    k: kwargs[k]
    for k in kwargs
    if k in valid_keys
  }
    
