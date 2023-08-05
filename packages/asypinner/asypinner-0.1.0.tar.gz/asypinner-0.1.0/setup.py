# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['asypinner']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.3,<0.5.0']

setup_kwargs = {
    'name': 'asypinner',
    'version': '0.1.0',
    'description': 'Async command-line spinner',
    'long_description': None,
    'author': 'Hiroki Konishi',
    'author_email': 'relastle@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
