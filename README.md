# `argparse_tree` #

Let the commandline arguments be distributed along the
source directory, which can be collected into one with
a single collection as a parent before initialising the
command.

# Installation #

## Using `pip` ##
```shell
pip install argparse_tree
```

## Using `pip` but with a cloned repository ##
```shell
git clone "https://github.com/bvraghav/argparse_tree"
cd argparse_tree
pip install .
```

# Usage #

A detailed usage can be found in the folder
[`example`](./example). The crux of the matter is
illustrated below:

```python
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
```

Inside of [`style2/generic.py`](./example/style2/generic.py)
```python
parser.add_argument(
  '--style2', choices=collect_keys('style2/*.py'),
  action=load_module_action('*.py', __package__)
)
```

Four functions namely,
[`collect_parsers`](./argparse_tree/utils.py#L13),
[`collect_keys`](./argparse_tree/utils.py#L73),
[`add_commands`](./argparse_tree/utils.py#L90), and
[`load_module_subparser_action`](./argparse_tree/load_module_action.py#L31)
are utilized to achieve the desired behaviour, that is

1. To have a set of argument groups collected from a
   set of files following a convenvention in names;
2. To allow, non-homogeneity in such groups; and
3. To extend this behaviour for sub-parsers.

## Convention ##
A set of files, each containing a function
[`cli_args`](./example/alpha_style1.py#L1) that returns
parser information, are grouped together using a
certain convention in their file names, for example,
using a suffix say,`*_data.py` may represent different
datasets. The arguments generic to all datasets may be
written to `generic_data.py`. They are all collected
using the function `collect_parsers`.

The convention may have simple been altered to follow a
prefixed format, say `data/*.py` --- should work
equally well.

## [`collect_parsers`](./argparse_tree/utils.py#L13) ##

```python
collect_parsers(
  *patterns, 
  root=None,
  parent_package=None
)
```

Glob the `ROOT` folder with `PATTERNS`, one at a time,
and collect their parsers. If not specified, `ROOT` is
computed, using the `inspect` API, to be the folder
where the caller script resides. 

`PARENT_PACKAGE` is the name of package corresponding
to `ROOT` folder. If not specified, `PARENT_PACKAGE` is
not used.

## [`collect_keys`](./argparse_tree/utils.py#L73)  ##

```python
collect_keys(
  pattern,
  root=None,
  mod_to_key=utils.mod_to_key
)
```
Glob the `ROOT` folder with `PATTERN` and create a key
corresponding to each module. Key is computed using
`MOD_TO_KEY` functional, which follows the same
signature as
[`utils.mod_to_key`](./argparse_tree/utils.py#L47).


## [`add_commands`](./argparse_tree/utils.py#L90) ##

```python
add_commands(
  parser, pattern, 
  *,
  root=None,
  parent_package=None,
  dest='command',
  action=None,
  mod_to_key=utils.mod_to_key
)
```

Create subcommands to cli using `PARSER`, one
corresponding to each `PATTERN`. Command name is
computed using `MOD_TO_KEY` functional, which follows
the same signature as
[`utils.mod_to_key`](./argparse_tree/utils.py#L47).

The same convention as
[`collect_parsers`](#collect_parsers) is followed for
`PATTERN`, `ROOT`, and `PARENT_PACKAGE`.

`DEST` and `ACTION` are forwarded to
[`argparse.ArgumentParser.add_subparsers`](https://docs.python.org/3/library/argparse.html?highlight=argparse%20argumentparser%20add_subparsers#argparse.ArgumentParser.add_subparsers).


## [`load_module_subparser_action`](./argparse_tree/load_module_action.py#L31) ##

```python
load_module_subparser_action(
  pattern,
  package=None,
  key_to_mod=utils.key_to_mod
)
```

Create an `argparse.Action` to load a module
corresponding to a user-given key, based on `PATTERN`,
and `PACKAGE` using a decoder `KEY_TO_MOD` functional,
which follows the same signature as
[`utils.key_to_mod`](./argparse_tree/utils.py#L110).

In case it is desirable to load a module corresponding
to value in user-specified argument, at the time of
parsing the args, use this as value of `action` in
[`argparser.ArgumentParser.add_argument`](https://docs.python.org/3/library/argparse.html?highlight=argparse%20argumentparser%20add_argument#argparse.ArgumentParser.add_argument).

### Update ###
**Version >= 0.1.3** : Code issues separate actions
corresponding to `store` action and `subparser` action,
as `load_module_store_action` and
`load_module_subparser_action`
respectively. *BREAKING*: `load_module_action` is an
alias for `load_module_store_action`.


# Motivation #

The core idea behind this project is to exploit [this
argparse
functionality](https://docs.python.org/3/library/argparse.html?highlight=parents#parents):

```python
local_parser = argparse.ArgumentParser()
local_parser.add_argument('--foo')

global_parser = argparse.ArgumentParser(
  parents=[local_parser, ...]
)
```

The proof of concept can be seen in [this
code](./scratchpad/proof_of_concept.py).

For example in machine learning training routines,
there can be many models, many solvers, many datasets,
each with different set of options. We can have
something like:

```python
## generic_dataset.py

def cli_parser() :
  from argparse import ArgumentParser
  parser = ArgumentParser(add_help=False)
  group = parser.add_argument_group(
    'Generic Dataset Options'
  )
  group.add_arguemnt('--foo')
  
  return parser
  
```

And similarly add cli parsers for `a_dataset.py`,
`b_dataset.py` and so forth. Here, we have followed the
norm of suffxing `dataset` to each python module. We
can collect them into the global parser as follows:

```python

from argparse import 
import argparse_tree as Atree

def cli_parser() :
  parser = ArgumentParser(
    parents=Atree.collect(['*_dataset.py'])
  )
  parser.add_argument(
    '--verbose', help="Verbosity switch."
  )
  
  return parser
```

We can also have an option of collection from any
pattern. For example,

+ `data/*.py` for any module in folder `data`.
+ Any other pattern compatible with
  [`pathllib.Path.glob`](https://docs.python.org/3/library/pathlib.html?highlight=glob#pathlib.Path.glob)
  


# Scratchpad #

## Can an instance initializer know the caller file path ##
  
Here is an experiment which has an affirmative result.
```python
## alpha.py ##
## ----------------------------------------------------
class A :
  def __init__(self) :
    from pathlib import Path
    import inspect
    f = inspect.stack().pop(1)
    # print(f.filename)
    self.p = Path(f.filename)
```

```python
## beta.py ##
## ----------------------------------------------------
from alpha import A
print (A().p)
```

The idea is the use this behaviour and search the
caller's parent path for the relevant module patterns.

This may be interesting; but it is always better to
provide an unambiguous argument instead of inspect!
