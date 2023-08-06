# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['weasel']
install_requires = \
['click>=7.1.2,<8.0.0']

entry_points = \
{'console_scripts': ['weasel = weasel:cli']}

setup_kwargs = {
    'name': 'weasel-cli',
    'version': '1.0.2a1',
    'description': "Simulate Dawkins' weasel experiment",
    'long_description': "# Dawkins' Weasel Program\n\n[![license](https://img.shields.io/github/license/wdsrocha/weasel-cli?color=blue)](https://github.com/wdsrocha/weasel-cli/blob/master/LICENSE)\n[![version](https://img.shields.io/pypi/v/weasel-cli)](https://pypi.org/project/weasel-cli/)\n[![build](https://img.shields.io/github/workflow/status/wdsrocha/weasel-cli/build)](https://github.com/wdsrocha/weasel-cli/actions?query=workflow%3Abuild)\n[![prs](https://img.shields.io/badge/PRs-welcome-brightgreen)](https://github.com/wdsrocha/weasel-cli/blob/master/CONTRIBUTING.md)\n\nSimple implementation of the classic [weasel program](https://en.wikipedia.org/wiki/Weasel_program).\n\n![demo](https://raw.githubusercontent.com/wdsrocha/weasel-cli/master/demo.png)\n\n## About\n\nAlthough the weasel simulation really works, I'm using this project mostly to test things like CLI development, Github Actions, PyPI deployment, etc.\n\n## Installation\n\n`pip install weasel-cli`\n\n## Usage\n\n```\n$ weasel --help\nUsage: weasel [OPTIONS]\n\n  Simulate Dawkins' weasel experiment\n\nOptions:\n  -t, --target TEXT               [default: METHINKS IT IS LIKE A WEASEL]\n  -p, --population-size INTEGER RANGE\n                                  [default: 100]\n  -r, --mutation-rate FLOAT RANGE\n                                  [default: 0.05]\n  --color / --no-color            Uses ANSI colors when reporting generation\n                                  results  [default: True]\n\n  --help                          Show this message and exit.\n```\n\n## License\n\nThis project is licensed under the terms of the MIT license - see the `LICENSE` file for details.\n",
    'author': 'Wesley Rocha',
    'author_email': 'wesleysr1997@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/wdsrocha/weasel-cli',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
