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
    'version': '0.1.1',
    'description': 'A flake8 plugin used to improve use of pathlib module.',
    'long_description': '# flake8-pathlib\n\nA flake8 plugin used to improve use of pathlib module.',
    'author': 'Rodolphe Pelloux-Prayer',
    'author_email': 'rodolphe@damsy.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/RoPP/flake8-pathlib',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
