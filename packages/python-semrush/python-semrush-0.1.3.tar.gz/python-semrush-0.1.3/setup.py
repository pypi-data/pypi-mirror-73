# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['python_semrush', 'python_semrush.tests']

package_data = \
{'': ['*']}

install_requires = \
['ipdb>=0.13.3,<0.14.0', 'requests>=2.24.0,<3.0.0']

setup_kwargs = {
    'name': 'python-semrush',
    'version': '0.1.3',
    'description': 'Python-Semrush is a wrapper around the SEMrush API version 3.0',
    'long_description': None,
    'author': 'Tulio Cesar Martins Pereira',
    'author_email': 'funroll.loops@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
