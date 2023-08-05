# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['crashalyser']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'croniter>=0.3.34,<0.4.0',
 'python-crontab>=2.5.1,<3.0.0']

entry_points = \
{'console_scripts': ['crashalyser = crashalyser.cli:cli']}

setup_kwargs = {
    'name': 'crashalyser',
    'version': '0.4.0',
    'description': 'Automatically analyse and record via email or file backtraces from core dumps',
    'long_description': None,
    'author': 'Ross Cousens',
    'author_email': 'rcousens@kixeye.com',
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
