# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lonny_aws_bin']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.14.16,<2.0.0']

entry_points = \
{'console_scripts': ['awsbin = lonny_aws_bin:run']}

setup_kwargs = {
    'name': 'lonny-aws-bin',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'None',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
