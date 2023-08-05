# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['src']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'openpyxl>=3.0.4,<4.0.0']

entry_points = \
{'console_scripts': ['pyxl = src.main:cli']}

setup_kwargs = {
    'name': 'pyxl-cli',
    'version': '0.1.0',
    'description': 'openpyxl wrapper for cli use',
    'long_description': None,
    'author': 'wataru-kurashima',
    'author_email': 'wataru-kurashima@hands-lab.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
