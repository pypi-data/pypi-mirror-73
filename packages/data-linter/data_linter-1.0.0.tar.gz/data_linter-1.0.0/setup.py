# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['data_linter']

package_data = \
{'': ['*'], 'data_linter': ['schemas/*']}

install_requires = \
['boto3>=1.14.7,<2.0.0',
 'dataengineeringutils3>=1.0.1,<2.0.0',
 'goodtables>=2.5.0,<3.0.0',
 'iam_builder>=3.7.0,<4.0.0',
 'importlib-metadata>=1.7,<2.0',
 'jsonschema>=3.2.0,<4.0.0',
 'pyyaml>=5.3.1,<6.0.0']

entry_points = \
{'console_scripts': ['data_linter = data_linter.command_line:main']}

setup_kwargs = {
    'name': 'data-linter',
    'version': '1.0.0',
    'description': 'data linter',
    'long_description': None,
    'author': 'Thomas Hirsch',
    'author_email': 'thomas.hirsch@digital.justice.gov.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
