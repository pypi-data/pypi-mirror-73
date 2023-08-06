# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jange', 'jange.ops', 'jange.ops.text', 'jange.stream']

package_data = \
{'': ['*']}

install_requires = \
['cytoolz>=0.10.0,<0.11.0',
 'pandas==0.24.2',
 'psycopg2-binary>=2.8.3,<3.0.0',
 'spacy>=2.2.0,<3.0.0',
 'sqlalchemy==1.3.1']

setup_kwargs = {
    'name': 'jange',
    'version': '0.1.0',
    'description': 'Easy NLP library for Python',
    'long_description': None,
    'author': 'Sanjaya Subedi',
    'author_email': 'jangedoo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
