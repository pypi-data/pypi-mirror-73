# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spanning_cidr']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'spanning-cidr',
    'version': '0.1.1',
    'description': 'Function that accepts a sequence of IP addresses returning a single subnet that is large enough to span the lower and upper bound IP addresses with a possible overlap on either end.',
    'long_description': None,
    'author': 'Vitalii Shishorin',
    'author_email': 'moskrc@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
