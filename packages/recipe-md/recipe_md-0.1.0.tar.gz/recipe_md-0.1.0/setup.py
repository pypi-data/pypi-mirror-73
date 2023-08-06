# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['recipe_md']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=7.2.0,<8.0.0',
 'flake8>=3.8.3,<4.0.0',
 'python-slugify>=4.0.1,<5.0.0',
 'recipe-scrapers>=8.0.1,<9.0.0',
 'requests>=2.24.0,<3.0.0',
 'typer>=0.3.0,<0.4.0']

entry_points = \
{'console_scripts': ['downrec = recipe_md.cli:main']}

setup_kwargs = {
    'name': 'recipe-md',
    'version': '0.1.0',
    'description': 'Scrape and convert recipes to markdown',
    'long_description': None,
    'author': 'rafa',
    'author_email': 'rafapi@gmail.com',
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
