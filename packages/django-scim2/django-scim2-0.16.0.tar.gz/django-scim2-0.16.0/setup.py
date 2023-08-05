# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['src', 'src.django_scim', 'src.django_scim.schemas']

package_data = \
{'': ['*'], 'src.django_scim.schemas': ['core/*', 'extension/*']}

install_requires = \
['Django>=2.0', 'python-dateutil>=2.7.3', 'scim2-filter-parser==0.3.4']

setup_kwargs = {
    'name': 'django-scim2',
    'version': '0.16.0',
    'description': '',
    'long_description': None,
    'author': 'Paul Logston',
    'author_email': 'paul@15five.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
