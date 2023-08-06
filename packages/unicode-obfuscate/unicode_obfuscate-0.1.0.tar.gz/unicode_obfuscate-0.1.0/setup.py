# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['unicode_obfuscate']

package_data = \
{'': ['*'], 'unicode_obfuscate': ['data/*']}

setup_kwargs = {
    'name': 'unicode-obfuscate',
    'version': '0.1.0',
    'description': 'Replace unicode characters with visually similar ones.',
    'long_description': None,
    'author': 'Lucas Bellomo',
    'author_email': 'lbellomo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
