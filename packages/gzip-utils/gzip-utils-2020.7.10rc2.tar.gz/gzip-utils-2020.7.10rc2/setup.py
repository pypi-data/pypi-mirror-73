# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['gzip_utils']

package_data = \
{'': ['*']}

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1.7.0,<2.0.0']}

setup_kwargs = {
    'name': 'gzip-utils',
    'version': '2020.7.10rc2',
    'description': '',
    'long_description': None,
    'author': 'Idar Bergli',
    'author_email': 'idar.bergli@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
