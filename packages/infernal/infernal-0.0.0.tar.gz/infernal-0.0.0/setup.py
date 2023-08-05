# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['infernal', 'infernal.common', 'infernal.core', 'infernal.graphics']

package_data = \
{'': ['*'],
 'infernal': ['services/__metadata__/*',
              'services/__templates__/*',
              'services/lol-champion-mastery/*',
              'services/lol-champion/*',
              'services/lol-league-exp/*',
              'services/lol-league/*',
              'services/lol-match/*',
              'services/lol-spectator/*',
              'services/lol-status/*',
              'services/lol-summoner/*',
              'services/lol-third-party-code/*',
              'services/lol-tournament-stub/*',
              'services/lol-tournament/*']}

install_requires = \
['requests>=2.23.0,<3.0.0', 'selenium>=3.141.0,<4.0.0', 'vaex>=3.0.0,<4.0.0']

setup_kwargs = {
    'name': 'infernal',
    'version': '0.0.0',
    'description': 'Core library for the Infernal eSports Analytics Infernal library.',
    'long_description': None,
    'author': 'Shparki',
    'author_email': 'murrmat@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
