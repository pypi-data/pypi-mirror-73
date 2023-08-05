# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['arcane']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'arcane-numbers',
    'version': '0.1.0',
    'description': 'Format numbers',
    'long_description': '# Arcane numbers\n\nThis package help us format numbers\n\n## Test\n`poetry run pytest tests`\n',
    'author': 'Arcane',
    'author_email': 'product@arcane.run',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
