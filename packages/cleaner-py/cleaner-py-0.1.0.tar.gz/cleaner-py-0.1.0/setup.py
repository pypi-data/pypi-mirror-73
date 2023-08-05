# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cleaner', 'cleaner.commands']

package_data = \
{'': ['*']}

install_requires = \
['cleo>=0.8.1,<0.9.0', 'clikit>=0.6.2,<0.7.0', 'pyyaml>=5.3.1,<6.0.0']

setup_kwargs = {
    'name': 'cleaner-py',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Schumi543',
    'author_email': '12729148+Schumi543@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
