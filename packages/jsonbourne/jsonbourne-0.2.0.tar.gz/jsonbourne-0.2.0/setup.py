# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['jsonbourne', 'jsonbourne.jsonlib']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'jsonbourne',
    'version': '0.2.0',
    'description': 'Import the best JSON lib',
    'long_description': None,
    'author': 'jesse',
    'author_email': 'jesse@dgi.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
