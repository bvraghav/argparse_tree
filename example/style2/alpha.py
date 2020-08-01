def cli_args () :
  from argparse import ArgumentParser

  parser = ArgumentParser(add_help=False)
  group = parser.add_argument_group('Alpha Style 2')

  group.add_argument('--bar-alpha', help='Alpha Bar from style 2')


  return parser
