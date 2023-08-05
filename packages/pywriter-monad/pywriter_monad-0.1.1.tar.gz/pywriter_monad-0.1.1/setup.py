# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['writer']

package_data = \
{'': ['*']}

install_requires = \
['toolz>=0.10.0,<0.11.0', 'typing-extensions>=3.7.4,<4.0.0']

setup_kwargs = {
    'name': 'pywriter-monad',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Yohei Tamura',
    'author_email': 'tamuhey@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
