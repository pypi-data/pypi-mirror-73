# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['functional', 'functional.test']

package_data = \
{'': ['*'], 'functional.test': ['data/*', 'data/tmp/.gitkeep']}

install_requires = \
['dill>=0.3.2,<0.4.0', 'pandas[all]>=1.0.3,<2.0.0', 'tabulate<=1.0.0']

setup_kwargs = {
    'name': 'pyfunctional',
    'version': '1.4.0',
    'description': 'Package for creating data pipelines with chain functional programming',
    'long_description': None,
    'author': 'Pedro Rodriguez',
    'author_email': 'me@pedro.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0',
}


setup(**setup_kwargs)
