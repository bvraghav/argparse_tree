def cli_args () :
  from argparse import ArgumentParser

  parser = ArgumentParser(add_help=False)
  group = parser.add_argument_group('Beta Style 1')

  group.add_argument('--foo-beta', help='Beta Foo from style 1')


  return parser
