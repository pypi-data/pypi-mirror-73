# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['benpkg']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'benpkg',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Ben-Cheng',
    'author_email': 'bcheng@linz.govt.nz',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=2.7,<3.0',
}


setup(**setup_kwargs)
