# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ciphey',
 'ciphey.Decryptor',
 'ciphey.Decryptor.Encoding',
 'ciphey.Decryptor.Hash',
 'ciphey.Decryptor.basicEncryption',
 'ciphey.basemods',
 'ciphey.basemods.Checkers',
 'ciphey.basemods.Crackers',
 'ciphey.basemods.Decoders',
 'ciphey.basemods.Resources',
 'ciphey.basemods.Searchers',
 'ciphey.iface',
 'ciphey.neuralNetworkMod']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4.4,<2.0.0',
 'base58>=2.0.1,<3.0.0',
 'cipheycore>=0.2.2,<0.3.0',
 'cipheydists>=0.3.5,<0.4.0',
 'click-spinner>=0.1.10,<0.2.0',
 'click>=7.1.2,<8.0.0',
 'flake8>=3.8.2,<4.0.0',
 'loguru>=0.5.0,<0.6.0',
 'pybase62>=0.4.3,<0.5.0',
 'pylint>=2.5.2,<3.0.0',
 'pyyaml>=5.3.1,<6.0.0',
 'rich>=1.2.3,<2.0.0',
 'yaspin>=0.17.0,<0.18.0']

extras_require = \
{':python_version >= "3.6" and python_version < "3.8"': ['typing_inspect>=0.6.0,<0.7.0']}

entry_points = \
{'console_scripts': ['ciphey = ciphey.__main__:main']}

setup_kwargs = {
    'name': 'ciphey',
    'version': '5.0.0rc3',
    'description': 'Automated Decryption Tool',
    'long_description': None,
    'author': 'Brandon',
    'author_email': 'brandon@skerritt.blog',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
