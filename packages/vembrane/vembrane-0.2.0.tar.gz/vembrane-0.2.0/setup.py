# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vembrane']

package_data = \
{'': ['*']}

install_requires = \
['pysam>=0.16,<0.17']

entry_points = \
{'console_scripts': ['vembrane = vembrane:main']}

setup_kwargs = {
    'name': 'vembrane',
    'version': '0.2.0',
    'description': 'Filter VCF/BCF files with Python expressions.',
    'long_description': None,
    'author': 'Till Hartmann',
    'author_email': None,
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
