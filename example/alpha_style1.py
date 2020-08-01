def cli_args () :
  from argparse import ArgumentParser

  parser = ArgumentParser(add_help=False)
  group = parser.add_argument_group('Alpha Style 1')

  group.add_argument('--foo-alpha', help='Alpha Foo from style 1')


  return parser
