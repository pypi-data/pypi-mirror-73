# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['flask_threaded_sockets']

package_data = \
{'': ['*']}

install_requires = \
['flask>=1.1.2,<2.0.0', 'werkzeug>=1.0.1,<2.0.0']

setup_kwargs = {
    'name': 'flask-threaded-sockets',
    'version': '0.1.0',
    'description': 'Barebones websocket extension for Flask, using Pythonthreading for low-traffic concurrency',
    'long_description': None,
    'author': 'Joel Collins',
    'author_email': 'joel@jtcollins.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
