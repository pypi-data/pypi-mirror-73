# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['inso_toolbox',
 'inso_toolbox.filter',
 'inso_toolbox.impute',
 'inso_toolbox.smoother',
 'inso_toolbox.utils']

package_data = \
{'': ['*']}

install_requires = \
['cognite-sdk-experimental>=0.11.0,<0.12.0',
 'pytest-custom-exit-code>=0.3.0,<0.4.0',
 'scipy>=1.4.1,<2.0.0',
 'sphinx>=3.1.2,<4.0.0',
 'sphinx_rtd_theme>=0.5.0,<0.6.0']

setup_kwargs = {
    'name': 'cognite-inso-toolbox',
    'version': '1.0.0',
    'description': 'Inso Toolbox',
    'long_description': None,
    'author': 'cognite',
    'author_email': 'gustavo.zarruk@cognite.com, johannes.kolberg@cognite.com, nicolas.agnes@cognite.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
