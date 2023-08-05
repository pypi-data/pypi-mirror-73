# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flat_tree']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=19.3.0,<20.0.0']

setup_kwargs = {
    'name': 'flat-tree',
    'version': '0.0.1a8',
    'description': 'Utilities for navigating flat trees',
    'long_description': '# flat-tree\n\n[![Build Status](https://drone.autonomic.zone/api/badges/hyperpy/flat-tree/status.svg)](https://drone.autonomic.zone/hyperpy/flat-tree)\n\n## Utilities for navigating flat trees\n\n> Flat Trees are the core data structure that power Hypercore feeds. They allow\n> us to deterministically represent a tree structure as a vector. This is\n> particularly useful because vectors map elegantly to disk and memory. Because\n> Flat Trees are deterministic and pre-computed, there is no overhead to using\n> them. In effect this means that Flat Trees are a specific way of indexing\n> into a vector more than they are their own data structure. This makes them\n> uniquely efficient and convenient to implement in a wide range of languages.\n\n## Install\n\n```sh\n$ pip install flat-tree\n```\n\n## Example\n\n```python\nfrom flat_tree.accessor import FlatTreeIterator\n\ntree_iter = FlatTreeIterator()\nassert tree_iter.index == 0\nassert tree_iter.parent() == 1\nassert tree_iter.parent() == 3\n```\n',
    'author': 'Decentral1se',
    'author_email': 'hi@decentral1.se',
    'maintainer': 'Decentral1se',
    'maintainer_email': 'hi@decentral1.se',
    'url': 'https://github.com/hyperpy/flat-tree',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
