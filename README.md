# argparse_tree #

Let the commandline arguments be distributed along the
source directory, which can be collected into one with
a single collection as a parent before initialising the
command.

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
The proof of concept can be seen in [this code](./proof-of-concept.py).

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

The idea is the use this behaviour and search the caller's
parent path for the relevant module patterns.

This may be interesting; but it is always better to
provide an unambiguous argument instead of inspect!
