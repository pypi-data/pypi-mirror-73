# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['excel2json_gui']

package_data = \
{'': ['*'], 'excel2json_gui': ['images/*']}

install_requires = \
['PyQt5>=5.15.0,<6.0.0', 'openpyxl>=3.0.4,<4.0.0']

entry_points = \
{'console_scripts': ['excel2json-gui = excel2json_gui.main:main']}

setup_kwargs = {
    'name': 'excel2json-gui',
    'version': '0.1.6',
    'description': 'GUI program to convert CH5 spreadsheet to JSON',
    'long_description': None,
    'author': 'mflorczak',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
