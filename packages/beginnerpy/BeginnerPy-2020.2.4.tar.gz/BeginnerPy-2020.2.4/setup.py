# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['beginnerpy',
 'beginnerpy.challenges',
 'beginnerpy.challenges.adventure_game',
 'beginnerpy.challenges.daily',
 'beginnerpy.challenges.testing']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.3,<0.5.0', 'toml>=0.10.1,<0.11.0']

setup_kwargs = {
    'name': 'beginnerpy',
    'version': '2020.2.4',
    'description': '',
    'long_description': None,
    'author': 'Zech Zimmerman',
    'author_email': 'hi@beginnerpy.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
