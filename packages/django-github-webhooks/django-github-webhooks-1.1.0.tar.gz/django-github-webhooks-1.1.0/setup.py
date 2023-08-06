# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['github_webhooks']

package_data = \
{'': ['*']}

install_requires = \
['django>=2.2,<4.0']

extras_require = \
{'black': ['black>=19.10b0,<20.0'],
 'dev': ['tox<3.8',
         'pytest>=5.2,<6.0',
         'pytest-django>=3.9.0,<4.0.0',
         'pytest-cov>=2.1.0,<3.0.0',
         'sphinx>=3,<4',
         'black>=19.10b0,<20.0',
         'isort[pyproject]>=4.3.21,<5.0.0'],
 'docs': ['sphinx>=3,<4'],
 'isort': ['isort[pyproject]>=4.3.21,<5.0.0'],
 'test': ['pytest>=5.2,<6.0',
          'pytest-django>=3.9.0,<4.0.0',
          'pytest-cov>=2.1.0,<3.0.0']}

setup_kwargs = {
    'name': 'django-github-webhooks',
    'version': '1.1.0',
    'description': 'GitHub webhooks for Django.',
    'long_description': '.. image:: https://img.shields.io/pypi/v/django-github-webhooks\n    :target: https://pypi.org/project/django-github-webhooks/\n    :alt: PyPI\n\n.. image:: https://img.shields.io/pypi/djversions/django-github-webhooks\n    :alt: PyPI - Django Version\n\n.. image:: https://github.com/OpenWiden/django-github-webhooks/workflows/Tests/badge.svg?branch=master\n    :target: https://github.com/OpenWiden/django-github-webhooks/workflows/Tests/badge.svg?branch=master\n    :alt: Tests passed\n\n.. image:: https://codecov.io/gh/OpenWiden/django-github-webhooks/branch/master/graph/badge.svg\n    :target: https://codecov.io/gh/OpenWiden/django-github-webhooks\n    :alt: Code coverage\n\n.. image:: https://readthedocs.org/projects/django-github-webhooks/badge/?version=latest\n    :target: https://django-github-webhooks.readthedocs.io/en/latest/?badge=latest\n    :alt: Documentation Status\n\n.. image:: https://pyup.io/repos/github/OpenWiden/django-github-webhooks/shield.svg\n     :target: https://pyup.io/repos/github/OpenWiden/django-github-webhooks/\n     :alt: Updates\n\n===============\nGitHub webhooks\n===============\n\nGitHub webhooks for Django.\n\n* Documentation: https://django-github-webhooks.readthedocs.io/en/latest/\n\nFeatures\n--------\n* Python >= 3.7.\n* Django >= 2.1.\n* Fully tested.\n* Easily extendable.\n',
    'author': 'stefanitsky',
    'author_email': 'stefanitsky.mozdor@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/OpenWiden/django-github-webhooks',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
