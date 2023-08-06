# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vartoml']

package_data = \
{'': ['*']}

install_requires = \
['toml>=0.9']

setup_kwargs = {
    'name': 'vartoml',
    'version': '0.9.5',
    'description': 'Enable variables in a TOML file',
    'long_description': None,
    'author': 'Manfred Lotz',
    'author_email': 'manfred.lotz@posteo.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/manfredlotz/vartoml',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5',
}


setup(**setup_kwargs)
