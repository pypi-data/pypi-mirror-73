# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flake8_pathlib']

package_data = \
{'': ['*']}

install_requires = \
['flake8>=3.8.3,<4.0.0']

extras_require = \
{':python_version >= "3.6" and python_version < "3.7"': ['dataclasses>=0.7,<0.8']}

entry_points = \
{'flake8.extension': ['P = flake8_pathlib:PathlibChecker']}

setup_kwargs = {
    'name': 'flake8-pathlib',
    'version': '0.1.2',
    'description': 'A plugin for flake8 finding use of functions that can be replace by pathlib module.',
    'long_description': '# flake8-pathlib\n\nA plugin for flake8 finding use of functions that can be replace by pathlib module.',
    'author': 'Rodolphe Pelloux-Prayer',
    'author_email': 'rodolphe@damsy.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/RoPP/flake8-pathlib',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
