# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['keepy']

package_data = \
{'': ['*']}

install_requires = \
['pykeepass>=3.2,<4.0']

setup_kwargs = {
    'name': 'keepy',
    'version': '0.0.1a0',
    'description': 'A Python Keepass CLI utility (placeholder package)',
    'long_description': None,
    'author': 'Patryk Tech',
    'author_email': 'git@patryk.tech',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
