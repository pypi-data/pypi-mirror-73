# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lonny_proc']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['proc = lonny_proc.cli:run']}

setup_kwargs = {
    'name': 'lonny-proc',
    'version': '0.1.3',
    'description': '',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
