# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['oanda_chart']

package_data = \
{'': ['*'], 'oanda_chart': ['image_data/*']}

install_requires = \
['forex-types>=0.0.6,<0.0.7',
 'oanda-candles>=0.0.6,<0.0.7',
 'tk-oddbox>=0.0.3,<0.0.4']

setup_kwargs = {
    'name': 'oanda-chart',
    'version': '0.0.1',
    'description': 'Oanda forex candle chart tkinter widget.',
    'long_description': None,
    'author': 'Andrew Allaire',
    'author_email': 'andrew.allaire@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
