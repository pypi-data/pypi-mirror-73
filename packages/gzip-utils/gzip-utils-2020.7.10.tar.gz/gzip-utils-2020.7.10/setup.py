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
    'version': '2020.7.10',
    'description': "Package with diffrent gzip-util's",
    'long_description': '# Gzip Utilities for Python\n\n[![Build Status](https://dev.azure.com/eossu/public/_apis/build/status/Eossu.gzip-utils?branchName=master)](https://dev.azure.com/eossu/public/_build/latest?definitionId=2&branchName=master)\n\nThis is a repository to hold diffrent utilities for gzip.\n\n## Utilities\n\n- [Compressed JSON List](docs/utils/compressed_json_list.md)\n',
    'author': 'Idar Bergli',
    'author_email': 'idar.bergli@protonmail.com',
    'maintainer': 'Idar Bergli',
    'maintainer_email': 'idar.bergli@protonmail.com',
    'url': 'https://github.com/Eossu/gzip-utils',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
