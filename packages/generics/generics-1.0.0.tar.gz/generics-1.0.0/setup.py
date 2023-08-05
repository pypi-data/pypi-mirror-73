# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['_generics', '_generics.entities', 'generics']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'generics',
    'version': '1.0.0',
    'description': 'A class-based toolkit designed with OOP in mind.',
    'long_description': '',
    'author': 'Artem Malyshev',
    'author_email': 'proofit404@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/generics/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
}


setup(**setup_kwargs)
