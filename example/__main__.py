import logging as lg

def cli_args() :
  from argparse import ArgumentParser
  from .. argparse_tree import (
    collect_parsers, add_commands,
    load_module_subparser_action,
  )

  parser = ArgumentParser(
    parents=collect_parsers(
      '*_style1.py', 'style2/*.py',
      parent_package = __package__
    ),
  )

  parser.add_argument(
    '-v', '--verbose', action='store_true',
    help="Verbosity switch."
  )

  add_commands(
    parser, '*_command.py',
    parent_package=__package__,
    action=load_module_subparser_action(
      '*_command.py', __package__
    ),
  )

  return parser

def main() :

  lg.basicConfig(
    level=lg.DEBUG,
    format='%(levelname)-8s: %(message)s'
  )

  parser = cli_args()
  args = parser.parse_args()
  lg.info(args)


main()
