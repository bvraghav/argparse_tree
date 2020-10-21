import logging as lg

def sanitize_root_path(root) :
  from pathlib import Path
  from inspect import stack

  return (
    Path(root)
    if root 
    else Path(stack().pop(2).filename).parent
  )

def collect_parsers(
    *patterns,
    root=None,
    parent_package=None
) :
  from . import Atree

  from itertools import chain

  root = sanitize_root_path(root)
  lg.debug('collect_parsers: root: %s', root)

  lg.debug('collect_parsers: patterns: %s', patterns)

  parser_groups = [
    Atree(
      pat,
      root = root,
      parent_package = parent_package,
    ).collect_parsers()
    for pat in patterns
  ]
  lg.debug(f'collect_parsers: parser_groups: {parser_groups}')

  # commands = reduce_command_parsers(
  #   commands,
  #   root=root,
  #   parent_package=parent_package,
  # )
  # lg.debug(f'collect_parsers: commands: {commands}')

  return list(chain(*parser_groups))


def mod_to_key(module_name, pattern) :
  from functools import reduce
  from pathlib import Path

  eraser = lambda s, x : (
    s.replace(
      x, ''
    ).replace(
      str(Path(x).with_suffix('')),
      ''
    )
  )

  noise = pattern.split('*')
  noise = list(filter(lambda x: x, noise))
  noise.insert(0, module_name)

  key = reduce(eraser, noise)
  key = key.replace('_', '-')

  lg.debug(
    f'mod_to_key: module_name:{module_name} '
    f'pattern:{pattern} noise:{noise} key:{key}'
  )

  return key


def collect_keys(
    pattern,
    root=None,
    mod_to_key=mod_to_key,
) :
  from . import Atree

  root = sanitize_root_path(root)
  lg.debug('collect_keys: root: %s', root)
  lg.debug('collect_keys: pattern: %s', pattern)

  return Atree(
    pattern,
    root = root,
    mod_to_key=mod_to_key,
  ).collect_keys()

def add_commands(
    parser, pattern, *,
    root=None, parent_package=None,
    dest='command', action=None,
    mod_to_key=mod_to_key,
) :
  from . import Atree
  from argparse import ArgumentParser

  root = sanitize_root_path(root)
  lg.debug('add_commands: root: %s', root)

  commands = Atree(
    pattern,
    root = root,
    parent_package = parent_package,
    mod_to_key = mod_to_key
  ).collect_keyed_parsers()

  if commands :
    kwargs = dict()
    if action : kwargs['action'] = action
    subs = parser.add_subparsers(
      dest=dest, required=True, **kwargs
    )

    for name, prsr in commands.items() :

      lg.debug(f'reduce_command_parsers: name: {name}')
      lg.debug(f'reduce_command_parsers: prsr: {prsr}')

      subs.add_parser(name, parents=[prsr])

  else : # not commands
    lg.warning(f'add_commands: No match for pattern "{pattern}"')

  return parser

def key_to_mod(key, pattern, package=None) :
  from pathlib import Path

  lg.debug(f'key_to_mod: key:{key}, pattern:{pattern},'
           f' package:{package}')

  if isinstance(key, list) : key = key[0]
  key = key.replace('-', '_')
  mod = (
    str(Path(pattern).with_suffix(''))
    .replace('*', key).replace('/', '.')
  )

  if package : mod = f'{package}.{mod}'

  return mod
