# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yatb']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.5.1,<2.0.0']

entry_points = \
{'console_scripts': ['yatb = yatb.console:yatb']}

setup_kwargs = {
    'name': 'yatb',
    'version': '0.0.3',
    'description': 'Yet Another Telegram Bot implementation',
    'long_description': None,
    'author': 'denolehov',
    'author_email': 'denolehov@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
