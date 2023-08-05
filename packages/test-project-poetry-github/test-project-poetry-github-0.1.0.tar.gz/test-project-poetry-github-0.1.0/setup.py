# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['test_project_poetry_github']

package_data = \
{'': ['*']}

install_requires = \
['django>=3.0.8,<4.0.0']

setup_kwargs = {
    'name': 'test-project-poetry-github',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Victor Silva',
    'author_email': 'victor.hos@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
