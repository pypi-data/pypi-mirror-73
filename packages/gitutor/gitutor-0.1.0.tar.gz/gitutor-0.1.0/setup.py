# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gitutor']

package_data = \
{'': ['*']}

install_requires = \
['GitPython==3.1.3', 'click==7.1.2', 'gitdb==4.0.5', 'smmap==3.0.4']

setup_kwargs = {
    'name': 'gitutor',
    'version': '0.1.0',
    'description': 'Making git easier!',
    'long_description': None,
    'author': 'AMIA',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
