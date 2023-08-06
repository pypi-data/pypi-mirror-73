# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spanning_cidr']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'spanning-cidr',
    'version': '0.1.0',
    'description': '',
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
