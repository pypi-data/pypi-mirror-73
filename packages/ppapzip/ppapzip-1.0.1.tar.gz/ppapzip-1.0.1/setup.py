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
    'version': '1.0.1',
    'description': 'File encryption/decryption utility using RSA key',
    'long_description': '# ppap\n\n[![MIT License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENSE)\n[![PyPI version](https://badge.fury.io/py/ppapzip.svg)](https://badge.fury.io/py/ppapzip)\n[![Python Versions](https://img.shields.io/pypi/pyversions/ppapzip.svg)](https://pypi.org/project/ppapzip/)\n\nUtility to simplify zip file encryption using RSA keys.  \n~ for eradicate ppap ~\n\n## Overview\n\nPPAP means \n\n```\n- Password encrypted zip file\n- Password\n- Apartly Sending\n- Protocol\n```\n\nOriginal Meaning in Japanese.\n\n```\n- Passwordつきzip暗号化ファイルを送ります\n- Passwordを送ります\n- Aん号か*\n- Protocol\n```\n\n\\* = 暗号化 = Encryption\n\n[JIPDEC - S/MIME利用の最新動向](https://itc.jipdec.or.jp/common/images/4_20170227_otaishi.pdf)\n\n\n### Pros\n- Easy to send.\n- Misdelivery Prevention.\n\n### Cons\n- The recipient must be find the password and type it.\n- Bypassing malware detection filters.\n- In the first place, sending the password twice does not guarantee confidentiality.\n\n\n## Usage\n\n### Encryption\n```bash\n# it generates /path/to/your/ppap-yyyymmdd_HHMMssSSSSSS.zip\n$ ppap --encrypt /path/to/your/file --key ~/.ssh/your_key.pub\n```\n\n### Decryption\n```bash\n$ ppap --decrypt /path/to/your/ppap-yyyymmdd_HHMMssSSSSSS.zip --key ~/.ssh/your_key\n```\n\n### Help\n```\n$ ppap -h\n```\n\n## Installation\n```\n$ pip install ppapzip\n```\n\nThe source code for ppap is hosted at GitHub, and you may download, fork, and review it from this repository(https://github.com/sumeshi/ppap).\nPlease report issues and feature requests. :sushi: :sushi: :sushi:\n\n## License\nppap is released under the [MIT](LICENSE) License.\n',
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
