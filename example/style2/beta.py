def cli_args () :
  from argparse import ArgumentParser

  parser = ArgumentParser(add_help=False)
  group = parser.add_argument_group('Beta Style 2')

  group.add_argument('--bar-beta', help='Beta Bar from style 2')


  return parser
