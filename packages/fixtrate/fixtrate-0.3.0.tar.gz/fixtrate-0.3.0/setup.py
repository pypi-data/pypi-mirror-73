# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fixtrate',
 'fixtrate.cli',
 'fixtrate.fix42',
 'fixtrate.fixt',
 'fixtrate.store',
 'fixtrate.utils']

package_data = \
{'': ['*'], 'fixtrate': ['specs/*', 'templates/*']}

install_requires = \
['aenum>=2.1.2',
 'aioredis>=1.1.0',
 'async-timeout>=2.0',
 'python-dateutil>=2.6.1',
 'simplefix>=1.0.12',
 'sortedcontainers>=2.2.2,<3.0.0',
 'typing_extensions>=3.7.4,<4.0.0',
 'untangle>=1.1.1']

entry_points = \
{'console_scripts': ['fixtrate = fixtrate.cli.main:run']}

setup_kwargs = {
    'name': 'fixtrate',
    'version': '0.3.0',
    'description': 'Tools for interacting with the FIX protocol.',
    'long_description': None,
    'author': 'Carlo Holl',
    'author_email': 'carloholl@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
