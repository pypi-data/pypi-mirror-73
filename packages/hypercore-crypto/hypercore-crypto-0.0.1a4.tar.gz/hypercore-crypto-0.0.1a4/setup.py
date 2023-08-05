# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hypercore_crypto']

package_data = \
{'': ['*']}

install_requires = \
['merkle-tree-stream>=0.0.1-alpha.4,<0.0.2', 'pysodium>=0.7.5,<0.8.0']

setup_kwargs = {
    'name': 'hypercore-crypto',
    'version': '0.0.1a4',
    'description': 'Cryptography primitives for Hypercore',
    'long_description': '# hypercore-crypto\n\n[![Build Status](https://drone.autonomic.zone/api/badges/hyperpy/hypercore-crypto/status.svg)](https://drone.autonomic.zone/hyperpy/hypercore-crypto)\n\n## Cryptography primitives for Hypercore\n\n## Install\n\n```sh\n$ pip install hypercore-crypto\n```\n\n## Example\n\n```python\nfrom hypercore_crypto import data, key_pair\nfrom pysodium import crypto_sign_PUBLICKEYBYTES\n\npublic_key, secret_key = key_pair()\nassert len(public_key) == crypto_sign_PUBLICKEYBYTES\nprint(data(b"hello world").hex())\n```\n',
    'author': 'Decentral1se',
    'author_email': 'hi@decentral1.se',
    'maintainer': 'Decentral1se',
    'maintainer_email': 'hi@decentral1.se',
    'url': 'https://github.com/hyperpy/hypercore-crypto',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
