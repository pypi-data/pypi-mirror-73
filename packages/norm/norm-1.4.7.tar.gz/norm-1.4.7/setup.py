# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['norm']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'norm',
    'version': '1.4.7',
    'description': 'Easy peasy SQL generation',
    'long_description': None,
    'author': 'Justin Van Winkle',
    'author_email': 'justin.vanwinkle@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
