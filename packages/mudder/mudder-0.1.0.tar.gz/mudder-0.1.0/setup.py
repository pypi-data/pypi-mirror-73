# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['mudder']
setup_kwargs = {
    'name': 'mudder',
    'version': '0.1.0',
    'description': 'Python port of mudderjs',
    'long_description': None,
    'author': 'Patrick Gingras',
    'author_email': '775.pg.12@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.6,<4',
}


setup(**setup_kwargs)
