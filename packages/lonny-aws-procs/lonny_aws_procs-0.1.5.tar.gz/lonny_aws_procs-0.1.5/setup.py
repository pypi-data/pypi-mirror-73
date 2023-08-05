# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lonny_aws_procs']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.14.16,<2.0.0']

setup_kwargs = {
    'name': 'lonny-aws-procs',
    'version': '0.1.5',
    'description': '',
    'long_description': None,
    'author': 'tlonny',
    'author_email': 't@lonny.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
