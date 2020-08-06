def cli_args () :
  from argparse import ArgumentParser
  from ... argparse_tree import (
    collect_keys, load_module_action
  )

  parser = ArgumentParser(add_help=False)
  group = parser.add_argument_group('Generic Style 2')

  group.add_argument('--style2',
                     choices=collect_keys('*.py'),
                     action=load_module_action(
                       '*.py', __package__
                     ),
                     help='Select one of style 2')

  return parser
