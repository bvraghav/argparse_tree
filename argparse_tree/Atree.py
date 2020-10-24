import logging as lg

from . import utils

class Atree :
  def __init__(
      self, pattern,
      root=None, parent_package=None,
      mod_to_key=utils.mod_to_key
  ) :
    from . utils import sanitize_root_path

    self.pattern = pattern
    self.root = sanitize_root_path(root)

    self.parent_package = parent_package

    self.mod_to_key = mod_to_key

  def collect_parsers(self) :
    return list(map(self.parser, self.collect()))

  def collect_keys(self) :
    return [
      self.get_key(path)
      for path in self.get_paths()
      if 'generic' not in str(path).lower()
    ]

  def collect_keyed_parsers(self) :
    return {
      self.get_key(path):
      self.parser(self.get_module(path))

      for path in self.get_paths()
    }

  @staticmethod
  def parser(module) :
    return module.cli_args()

  def get_module(self, path) :
    from importlib import import_module
    from pathlib import Path

    s = path.relative_to(self.root).with_suffix('')
    if self.parent_package :
      p = Path(self.parent_package.replace('.', '/'))
      c = Path('.').resolve()
      s = (p/s).resolve().relative_to(c)

    s = str(s).replace('/', '.')
    lg.debug(f'Atree.get_module: s: {s}')

    return import_module(s)

  def get_key(self, path) :

    start = str(
      path.relative_to(self.root)
      .with_suffix('')
    )

    return self.mod_to_key(start, self.pattern)
    

  def get_paths(self) :
    paths = list(self.root.glob(self.pattern))
    lg.debug(f'get_paths: pattern: {self.pattern} paths: {paths}')

    generics = [i for i in range(len(paths))
                if 'generic' in str(paths[i]).lower()]
    generics = (
      [paths.pop(generics.pop(0))]
      if generics
      else []
    )

    lg.debug(f'Atree.get_paths: generics: {generics}')

    return generics + paths

  # def get_all_paths(self) :
  #   from itertools import chain
  #   return list(chain(
  #     *map(
  #       self.get_paths,
  #       self.patterns
  #     )
  #   ))

  def collect(self) :
    return list(map(
      self.get_module,
      self.get_paths()
    ))
