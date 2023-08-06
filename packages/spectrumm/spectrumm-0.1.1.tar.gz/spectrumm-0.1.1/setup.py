# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spectrumm']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.2.2,<4.0.0',
 'numpy>=1.19.0,<2.0.0',
 'pydub>=0.24.1,<0.25.0',
 'scipy>=1.5.1,<2.0.0']

entry_points = \
{'console_scripts': ['spectrumm = spectrumm.cli:main']}

setup_kwargs = {
    'name': 'spectrumm',
    'version': '0.1.1',
    'description': 'A small CLI utlity to plot audiofiles',
    'long_description': '# Spectrumm\n\n\n\nA wrapper between pythons matplotlib and the terminal. Allows you to plot audiofiles quickly.\n\n\n\n## Installation\n\n`pip install spectrumm`',
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
