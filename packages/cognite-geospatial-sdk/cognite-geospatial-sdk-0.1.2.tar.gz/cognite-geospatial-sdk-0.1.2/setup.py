# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'python/src'}

packages = \
['cognite',
 'cognite.geospatial',
 'cognite.geospatial._client',
 'cognite.geospatial._client.api',
 'cognite.geospatial._client.models']

package_data = \
{'': ['*']}

install_requires = \
['certifi>=2020.6,<2021.0',
 'numpy>=1.19,<2.0',
 'python-dateutil>=2.8,<3.0',
 'six>=1.15,<2.0',
 'tornado>=6.0.4,<7.0.0',
 'urllib3>=1.25,<2.0']

setup_kwargs = {
    'name': 'cognite-geospatial-sdk',
    'version': '0.1.2',
    'description': 'Cognite Geospatial SDK store and query spatial objects in 2D and 3D space',
    'long_description': None,
    'author': 'Cognite AS',
    'author_email': 'support@cognite.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
