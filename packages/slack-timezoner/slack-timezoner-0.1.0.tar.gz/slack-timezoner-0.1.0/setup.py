# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['slack_timezoner']

package_data = \
{'': ['*']}

install_requires = \
['django>=3.0.8,<4.0.0',
 'python-dotenv>=0.14.0,<0.15.0',
 'slackclient>=2.7.2,<3.0.0']

setup_kwargs = {
    'name': 'slack-timezoner',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Chris Adams',
    'author_email': 'chris@productscience.co.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
