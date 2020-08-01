def cli_args () :
  from argparse import ArgumentParser

  parser = ArgumentParser(add_help=False)
  parser.add_argument('--bar-bang', help='Bar from bang command.')


  return parser
