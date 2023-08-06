# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mttools',
 'mttools.AlgebraTools',
 'mttools.CalculusTools',
 'mttools.geometry_tools',
 'mttools.linear_algebra_tools',
 'mttools.number_theory_tools',
 'mttools.utils']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'mttools',
    'version': '0.2.3',
    'description': 'A Collection of Mathmatical Tools',
    'long_description': None,
    'author': 'kgb33',
    'author_email': 'github@bassingthwaite.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
