# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['archwiki']

package_data = \
{'': ['*']}

install_requires = \
['html2text>=2020.1.16,<2021.0.0', 'requests>=2.24.0,<3.0.0']

entry_points = \
{'console_scripts': ['archwiki = archwiki.archwiki:run']}

setup_kwargs = {
    'name': 'archwiki',
    'version': '0.3.0',
    'description': 'Explore e salve tópicos da biblioteca do ArchLinux',
    'long_description': None,
    'author': 'renantamashiro',
    'author_email': None,
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
