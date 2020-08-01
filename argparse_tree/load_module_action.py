import logging as lg

from . store_action import StoreActionBase


## Load Module
## ====================================================
class LoadModuleError(Exception) :
  pass


class LoadModuleActionBase(StoreActionBase) :
  def __call__(self, parser, namespace, values,
               option_string=None,) :

    # Modify values as needed
    values = self.value_decoder(values)
    lg.info(f'LoadModuleAction: values: {values}')

    # Import module
    from importlib import import_module
    values = import_module(values)
    lg.info(f'LoadModuleAction: values: {values}')

    # Save
    super().__call__(parser, namespace, values,
                     option_string=None,)

def load_module_action(pattern, package=None) :
  from . utils import key_to_mod
  from functools import partial
  from . sub_parsers_action import SubParsersAction

  class LoadModuleAction(
      LoadModuleActionBase, SubParsersAction
  ) :
    value_decoder = partial(
      key_to_mod, pattern=pattern, package=package
    )

  return LoadModuleAction