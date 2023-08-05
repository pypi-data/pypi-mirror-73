# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fennel', 'fennel.client', 'fennel.client.aio', 'fennel.worker']

package_data = \
{'': ['*'], 'fennel.worker': ['lua/*']}

install_requires = \
['aioredis>=1.3.0,<2.0.0',
 'click>=7.0,<8.0',
 'colorama>=0.4.1,<0.5.0',
 'pydantic>=1.5,<2.0',
 'redis>=3.3,<4.0',
 'structlog>=20.0,<21.0',
 'uvloop>=0.14.0,<0.15.0']

entry_points = \
{'console_scripts': ['fennel = fennel.cli:cli']}

setup_kwargs = {
    'name': 'fennel',
    'version': '0.2.4',
    'description': 'A task queue for Python based on Redis Streams.',
    'long_description': None,
    'author': 'Matt Westcott',
    'author_email': 'm.westcott@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://fennel.readthedocs.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
