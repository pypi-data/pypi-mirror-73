# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['matchy', 'matchy.matching_algorithms']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'numpy>=1.19.0,<2.0.0']

entry_points = \
{'console_scripts': ['matchy = matchy.cli:cli']}

setup_kwargs = {
    'name': 'matchy',
    'version': '0.1.0',
    'description': 'A tool for matching analog IC layout designs.',
    'long_description': None,
    'author': 'Fabian Torres',
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
