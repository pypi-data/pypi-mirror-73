# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['neo4j_gds', 'neo4j_gds.algorithms', 'neo4j_gds.queries', 'neo4j_gds.tests']

package_data = \
{'': ['*']}

install_requires = \
['py2neo>=5.0b5,<6.0']

setup_kwargs = {
    'name': 'neo4j-gds',
    'version': '0.1.1',
    'description': "Library to build neo4j's queries with special attention on Graph Data Science library calls",
    'long_description': None,
    'author': 'Pablo Cabezas',
    'author_email': 'pabcabsal@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
