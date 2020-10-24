from setuptools import setup

with open('README.md', 'r') as F :
  ldesc = F.read()

setup(
  name                          = 'argparse_tree',
  version                       = '0.1.3.post5',
  description                   = (
    'Split parse args into filesystem tree for '
    'complex projects.'
  ),
  long_description              = ldesc,
  long_description_content_type = 'text/markdown',
  url                           = 'https://github.com/bvraghav/argparse_tree',
  author                        = 'B.V. Raghav',
  licence                       = 'MIT',
  packages                      = ['argparse_tree'],
  classifiers                   = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
  python_requires               = '>=3',
)
