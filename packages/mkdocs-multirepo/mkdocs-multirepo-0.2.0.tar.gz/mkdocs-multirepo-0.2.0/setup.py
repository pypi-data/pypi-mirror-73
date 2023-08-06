# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mkdocs_multirepo']

package_data = \
{'': ['*'],
 'mkdocs_multirepo': ['.git/*',
                      '.git/hooks/*',
                      '.git/info/*',
                      'demo/*',
                      'demo/images/*',
                      'demo/site/images/*']}

install_requires = \
['beautifulsoup4>=4.9,<5.0', 'pyyaml>=5.3,<6.0']

entry_points = \
{'console_scripts': ['mkdocs-multirepo = mkdocs_multirepo:main']}

setup_kwargs = {
    'name': 'mkdocs-multirepo',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'Lars Wilhelmer',
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
