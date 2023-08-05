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
    'version': '0.2.0',
    'description': 'openpyxl wrapper for cli use',
    'long_description': '# pyxl-cli\n\nopeypyxl wrapper for cli use.\n\n## install\n\n```sh\npip install pyxl-cli\n```\n\n## usage\n\n### read\noutput stdout CSV format\n\n```sh\npyxl read \\\n    --input_xlsx input.xlsx\n```\n\noutput file TSV format\n\n```sh\npyxl read \\\n    --input_xlsx input.xlsx \\\n    --output /tmp/output.tsv \\\n    --delimiter=\'\\t\'\n```\n\n### write\nfor CSV file\n\n```sh\npyxl write \\\n    --sheet_xy_csv 1 A1 input.csv \\\n    template.xlsx output.xlsx\n```\n\nfor 2 TSV files\n\n```sh\npyxl write \\\n    --sheet_xy_csv 1 A1 input_a.tsv \\\n    --sheet_xy_csv 1 F12 input_b.tsv \\\n    --delimiter="\\t" \\\n    template.xlsx output.xlsx\n```',
    'author': 'watarukura',
    'author_email': 'what.r.j150@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/watarukura',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
