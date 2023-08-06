# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['synr']

package_data = \
{'': ['*']}

install_requires = \
['attrs']

setup_kwargs = {
    'name': 'synr',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Jared Roesch',
    'author_email': 'jroesch@octoml.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
