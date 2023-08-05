# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ueosio']

package_data = \
{'': ['*']}

install_requires = \
['base58>=2.0.0,<3.0.0', 'cryptos>=1.36,<2.0', 'requests>=2.23.0,<3.0.0']

setup_kwargs = {
    'name': 'ueosio',
    'version': '0.2.2',
    'description': 'uEOSIO python library',
    'long_description': '# µEOSIO\n**General purpose library for the EOSIO blockchains**\n\nMicro EOSIO allows you to interact with any EOSio chain using Python.\n\n# Install\n\n    pip3 install ueosio\n\n# Build from source\n\n    git clone https://github.com/AntarticaLabs/ueosio\n    cd ueosio\n    python3 -m venv venv\n    source venv/bin/activate\n    pip3 install -r examples/requirements.txt\n\n### Examples:\n\n[tx.py](https://github.com/AntarticaLabs/ueosio/blob/master/examples/tx.py): Send a transaction on any given chain.\n\n[keys.py](https://github.com/AntarticaLabs/ueosio/blob/master/examples/keys.py): Generate a key pair or get the public key of any given private key.\n\n[approve_multisig.py](https://github.com/AntarticaLabs/ueosio/blob/master/examples/approve_multisig.py): Approve a multisig transaction.\n\n[create_account.py](https://github.com/AntarticaLabs/ueosio/blob/master/examples/create_account.py): Create an account, buy ram and delegate bandwidth and CPU.\n\n_____\n\n\n[MIT License](LICENSE) \\\nCopyright (c) 2020 EOS Argentina\n',
    'author': 'EOS Argentina',
    'author_email': 'matias@eosargentina.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/AntarticaLabs/ueosio',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
