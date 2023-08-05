# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['ca_bundle']
setup_kwargs = {
    'name': 'ca-bundle',
    'version': '0.1.1',
    'description': 'No more SSL errors because of unset REQUESTS_CA_BUNDLE.',
    'long_description': "# CA-bundle\n\nNo more `SSLError`s because of unset `REQUESTS_CA_BUNDLE`.\n\nThis package searches through common locations of SLL certificates on linux and sets\nthe first existing location to `REQUESTS_CA_BUNDLE` and `HTTPLIB2_CA_CERTS` environment variables.\n\n## Installation\n\n```sh\npip install ca-bundle\n```\n\n## Usage\n\n```python\nimport ca_bundle\n\nca_bundle.install()\n```\n\nInspired by [Go's implementation](https://golang.org/src/crypto/x509/root_linux.go).\n",
    'author': 'Matúš Ferech',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/matusf/ca-bundle/',
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
