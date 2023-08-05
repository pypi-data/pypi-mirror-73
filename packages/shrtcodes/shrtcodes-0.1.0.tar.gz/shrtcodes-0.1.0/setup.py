# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['shrtcodes']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'shrtcodes',
    'version': '0.1.0',
    'description': 'Simple shortcodes for Python',
    'long_description': None,
    'author': 'Peter Byfield',
    'author_email': 'byfield554@gmail.com>',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3,<4',
}


setup(**setup_kwargs)
