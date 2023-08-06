# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['calixa_proto_py']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['copy-py-proto-script = copy_generated_py_proto:start']}

setup_kwargs = {
    'name': 'calixa-proto-py',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Calixa  Platform',
    'author_email': 'everyone@calixa.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=2.7,<3.0',
}


setup(**setup_kwargs)
