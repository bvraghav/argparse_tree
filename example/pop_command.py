def cli_args () :
  from argparse import ArgumentParser

  parser = ArgumentParser(add_help=False)
  parser.add_argument('--foo-pop', help='Foo from pop command.')


  return parser
