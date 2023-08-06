# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flake8_pathlib']

package_data = \
{'': ['*']}

install_requires = \
['flake8>=3.8.3,<4.0.0']

entry_points = \
{'flake8.extension': ['P = flake8_pathlib:PathlibChecker']}

setup_kwargs = {
    'name': 'flake8-pathlib',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Rodolphe Pelloux-Prayer',
    'author_email': 'rodolphe@damsy.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
