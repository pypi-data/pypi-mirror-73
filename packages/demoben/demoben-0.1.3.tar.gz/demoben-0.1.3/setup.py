# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['demoben']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'demoben',
    'version': '0.1.3',
    'description': 'This is a test',
    'long_description': None,
    'author': 'Ben-Cheng',
    'author_email': 'bcheng@linz.govt.nz',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
