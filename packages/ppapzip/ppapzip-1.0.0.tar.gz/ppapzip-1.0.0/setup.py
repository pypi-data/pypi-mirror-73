# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['ppapzip']
install_requires = \
['pycryptodome>=3.9.8,<4.0.0', 'pyminizip>=0.2.4,<0.3.0']

entry_points = \
{'console_scripts': ['ppap = ppapzip:ppap']}

setup_kwargs = {
    'name': 'ppapzip',
    'version': '1.0.0',
    'description': 'File encryption/decryption utility using RSA key',
    'long_description': '# ppap\nFile encryption utility using a GitHub public key.\n',
    'author': 'sumeshi',
    'author_email': 'j15322sn@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sumeshi/ppap',
    'package_dir': package_dir,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
