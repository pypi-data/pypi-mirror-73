# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['gustavgrad']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.19.0,<2.0.0']

setup_kwargs = {
    'name': 'gustavgrad',
    'version': '0.1.1a0',
    'description': '',
    'long_description': "# gustavgrad\n[![Tests](https://github.com/gustavgransbo/gustavgrad/workflows/Tests/badge.svg)](https://github.com/gustavgransbo/gustavgrad/actions?workflow=Tests)\n[![codecov](https://codecov.io/gh/gustavgransbo/gustavgrad/branch/master/graph/badge.svg)](https://codecov.io/gh/gustavgransbo/gustavgrad)\n\nAn autograd library built on NumPy, inspired by [Joel Grus's livecoding](https://github.com/joelgrus/autograd/tree/master).\n\nThe idea behind gustavgrad is to define a Tensor class, and a set of arithmetic operations on tensors, which we know how to calculate the first order derivative for.\nUsing the chain-rule, the gradient of the composition of multiple operations can be calculated, since we know how to calculate the first order derivative of the basic operations.\n",
    'author': 'Gustav Gränsbo',
    'author_email': 'gustav.gransbo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gustavgransbo/gustavgrad',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
