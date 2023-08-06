# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spectrumm']

package_data = \
{'': ['*'],
 'spectrumm': ['.git/*',
               '.git/hooks/*',
               '.git/info/*',
               '.git/logs/*',
               '.git/logs/refs/heads/*',
               '.git/logs/refs/remotes/origin/*',
               '.git/objects/3f/*',
               '.git/objects/75/*',
               '.git/objects/86/*',
               '.git/objects/b4/*',
               '.git/objects/b7/*',
               '.git/objects/c9/*',
               '.git/objects/ee/*',
               '.git/refs/heads/*',
               '.git/refs/remotes/origin/*']}

install_requires = \
['matplotlib>=3.2.2,<4.0.0',
 'numpy>=1.19.0,<2.0.0',
 'pydub>=0.24.1,<0.25.0',
 'scipy>=1.5.1,<2.0.0']

entry_points = \
{'console_scripts': ['spectrumm = spectrumm.cli:main']}

setup_kwargs = {
    'name': 'spectrumm',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'David Huss',
    'author_email': 'dh@atoav.com',
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
