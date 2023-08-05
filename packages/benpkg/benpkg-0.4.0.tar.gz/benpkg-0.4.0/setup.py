# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['benpkg']

package_data = \
{'': ['*']}

install_requires = \
['pyqt5>=5.10,<6.0']

setup_kwargs = {
    'name': 'benpkg',
    'version': '0.4.0',
    'description': 'some package',
    'long_description': None,
    'author': 'Ben-Cheng',
    'author_email': 'bcheng@linz.govt.nz',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
