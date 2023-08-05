# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tensorbank', 'tensorbank.tf']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.19.0,<2.0.0', 'tensorflow>=2.0']

setup_kwargs = {
    'name': 'tensorbank',
    'version': '0.1.1',
    'description': 'a collection of assorted algorithms expressed in Tensors.',
    'long_description': '# TensorBank\n\n[![PyPI version](https://badge.fury.io/py/tensorbank.svg)](https://badge.fury.io/py/tensorbank)\n[![Build Status](https://travis-ci.com/pshved/tensorbank.svg?branch=master)](https://travis-ci.com/pshved/tensorbank)\n[![Documentation Status](https://readthedocs.org/projects/tensorbank/badge/?version=latest)](https://tensorbank.readthedocs.io/en/latest/?badge=latest)\n\nTensorBank is a collection of assorted algorithms expressed in Tensors.\n\nWe do not intend to limit ourselves to a specific domain.  The initial batch of\nalgorithms is focused on point and box gemoetry for some object detection\ntasks, but more algorithms will be added later.\n\nWe are open to all backends, including Tensorflow, Pytorch, and NumPy.\n\nPrimarily, this project is to avoid copy-pasting the "utils" directory from one\nproject to the next :-)\n\n## Installation\n\n```\npip install tensorbank\n```\n\n## Usage\n\nIf you\'re using TensorFlow, import TensorBank as follows and use the `tb.`\nprefix:\n\n```python\nimport tensorbank.tf as tb\n\ntb.axis_aligned_boxes.area(\n\t [[1, 1, 2, 2],\n\t\t[-1, -1, 1, 2]])\n>>> tf.Tensor([1 6], shape=(2,), dtype=int32)\n```\n\nSee [API Reference on Readthedocs][api] for the full list of the algorithms\noffered and comprehensive usage examples.\n\n[api]: https://tensorbank.readthedocs.io/\n\n',
    'author': 'Paul Shved',
    'author_email': 'pavel.shved@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://github.com/pshved/tensorbank',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
