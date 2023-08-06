# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['healpix_alchemy', 'healpix_alchemy.tests']

package_data = \
{'': ['*']}

install_requires = \
['astropy', 'sqlalchemy']

setup_kwargs = {
    'name': 'healpix-alchemy',
    'version': '0.0.1',
    'description': 'SQLAlchemy extensions for HEALPix spatially indexed astronomy data',
    'long_description': None,
    'author': 'Leo Singer',
    'author_email': 'leo.singer@ligo.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/skyportal/healpix-alchemy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
