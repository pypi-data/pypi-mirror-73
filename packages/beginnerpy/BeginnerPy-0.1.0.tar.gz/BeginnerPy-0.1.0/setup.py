# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['beginnerpy',
 'beginnerpy.challenges.adventure_game',
 'beginnerpy.challenges.daily']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'beginnerpy',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Zech Zimmerman',
    'author_email': 'hi@beginnerpy.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7.4,<4.0.0',
}


setup(**setup_kwargs)
