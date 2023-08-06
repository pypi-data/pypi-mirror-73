# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_migrate', 'fastapi_migrate.templates.fastapi']

package_data = \
{'': ['*']}

install_requires = \
['alembic>=1.4.2,<2.0.0', 'click>=7.1.2,<8.0.0', 'fastapi>=0.58.1,<0.59.0']

setup_kwargs = {
    'name': 'fastapi-migrate',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'pengyj',
    'author_email': 'p15281826276@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
