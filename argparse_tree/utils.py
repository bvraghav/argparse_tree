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
  lg.info('collect_parsers: root: %s', root)

  lg.info('collect_parsers: patterns: %s', patterns)

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

def add_commands(
    parser, pattern, *,
    root=None, parent_package=None,
    dest='command', action=None,
) :
  from . import Atree
  from argparse import ArgumentParser

  root = sanitize_root_path(root)
  lg.info('add_commands: root: %s', root)

  commands = Atree(
    pattern,
    root = root,
    parent_package = parent_package,
  ).collect_keyed_parsers()

  if commands :
    kwargs = dict()
    if action : kwargs['action'] = action
    subs = parser.add_subparsers(
      dest=dest, required=True, **kwargs
    )

    for name, prsr in commands.items() :

      lg.info(f'reduce_command_parsers: name: {name}')
      lg.info(f'reduce_command_parsers: prsr: {prsr}')

      subs.add_parser(name, parents=[prsr])

  else : # not commands
    lg.warning(f'add_commands: No match for pattern "{pattern}"')

  return parser


def mod_to_key(module_name, pattern) :
  from functools import reduce
  from pathlib import Path

  eraser = lambda s, x : (
    s.replace(
      str(Path(x).with_suffix('')),
      ''
    )
  )

  noise = pattern.split('*')
  noise = list(filter(lambda x: x, noise))
  noise.insert(0, module_name)

  key = reduce(eraser, noise)
  key = key.replace('_', '-')

  lg.info(
    f'mod_to_key: module_name:{module_name} '
    f'pattern:{pattern} noise:{noise} key:{key}'
  )

  return key

def key_to_mod(key, pattern, package=None) :
  from pathlib import Path

  lg.debug(f'key_to_mod: key:{key}, pattern:{pattern},'
           f' package:{package}')

  key = key[0].replace('-', '_')
  mod = (
    str(Path(pattern).with_suffix(''))
    .replace('*', key).replace('/', '.')
  )

  if package : mod = f'{package}.{mod}'

  return mod