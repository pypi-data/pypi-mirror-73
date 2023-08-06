# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aimai_search']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=19.3.0,<20.0.0',
 'cutlet>=0.1.3,<0.2.0',
 'more-itertools>=8.4.0,<9.0.0',
 'rapidfuzz>=0.9.1,<0.10.0',
 'unidic-lite>=1.0.6,<2.0.0']

setup_kwargs = {
    'name': 'aimai-search',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'reiyw',
    'author_email': 'reiyw.setuve@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
