# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyside2_utils', 'pyside2_utils.signal_widgets']

package_data = \
{'': ['*']}

install_requires = \
['pyside2>=5.15.0,<6.0.0']

setup_kwargs = {
    'name': 'pyside2-utils',
    'version': '0.0.1',
    'description': 'PySide2 utilities.',
    'long_description': None,
    'author': 'MadaRa',
    'author_email': 'zaurik777to@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.8',
}


setup(**setup_kwargs)
