# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['python_semrush', 'python_semrush.tests']

package_data = \
{'': ['*']}

install_requires = \
['requests-async>=0.6.2,<0.7.0']

setup_kwargs = {
    'name': 'python-semrush',
    'version': '0.1.5',
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
