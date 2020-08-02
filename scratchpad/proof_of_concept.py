import logging as lg
lg.basicConfig(level=lg.DEBUG, format='%(levelname)-8s: %(message)s')

from argparse import ArgumentParser

a_gen_parser = ArgumentParser(add_help=False)
a_gen_group = a_gen_parser.add_argument_group(
  'Generic A Group'
)
a_gen_group.add_argument('--foo',
                         help="Foo Argument")


a_one_parser = ArgumentParser(add_help=False)
a_one_group = a_one_parser.add_argument_group(
  'A One Group'
)
a_one_group.add_argument('--foo-one',
                         help="Foo One Argument")

a_two_parser = ArgumentParser(add_help=False)
a_two_group = a_two_parser.add_argument_group(
  'A Two Group'
)
a_two_group.add_argument('--foo-two',
                         help="Foo Two Argument")



parser = ArgumentParser(
  parents=[a_gen_parser, a_one_parser, a_two_parser],
)
parser.add_argument('--verbose', action='store_true',
                    help='Verbosity switch.')

lg.info(parser.parse_args())

'''
Result:
$ python proof_of_concept.py -h
usage: proof_of_concept.py [-h] [--foo FOO] [--foo-one FOO_ONE]
                           [--foo-two FOO_TWO] [--verbose]

optional arguments:
  -h, --help         show this help message and exit
  --verbose          Verbosity switch.

Generic A Group:
  --foo FOO          Foo Argument

A One Group:
  --foo-one FOO_ONE  Foo One Argument

A Two Group:
  --foo-two FOO_TWO  Foo Two Argument

'''
