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
    'version': '1.0.4',
    'description': "Simulate Dawkins' weasel experiment",
    'long_description': '<p align="center"><a href="https://pypi.org/project/weasel-cli/" target="_blank" rel="noopener noreferrer"><img width="100" src="https://raw.githubusercontent.com/wdsrocha/weasel-cli/master/logo.svg" alt="Weasel CLI logo"></a></p>\n\n<p align="center">\n  <a href="https://github.com/wdsrocha/weasel-cli/blob/master/LICENSE"><img src="https://img.shields.io/github/license/wdsrocha/weasel-cli?color=blue" alt="license"></a>\n  <a href="https://pypi.org/project/weasel-cli/"><img src="https://img.shields.io/pypi/v/weasel-cli" alt="version"></a>\n  <a href="https://github.com/wdsrocha/weasel-cli/actions?query=workflow%3Abuild"><img src="https://img.shields.io/github/workflow/status/wdsrocha/weasel-cli/build" alt="build"></a>\n  <a href="https://github.com/wdsrocha/weasel-cli/blob/master/CONTRIBUTING.md"><img src="https://img.shields.io/badge/PRs-welcome-brightgreen" alt="prs"></a>\n</p>\n\n<h1 align="center">Dawkins\' Weasel CLI</h1>\n\nSimple implementation of the classic [weasel program](https://en.wikipedia.org/wiki/Weasel_program).\n\n![demo](https://raw.githubusercontent.com/wdsrocha/weasel-cli/master/cli_demo.png)\n\n## About\n\nAlthough the weasel simulation really works, I\'m using this project mostly to test things like CLI development, Github Actions, PyPI deployment, etc.\n\n## Installation\n\n`pip install weasel-cli`\n\n## Usage\n\n```\n$ weasel --help\nUsage: weasel [OPTIONS]\n\n  Simulate Dawkins\' weasel experiment\n\nOptions:\n  -t, --target TEXT               [default: METHINKS IT IS LIKE A WEASEL]\n  -p, --population-size INTEGER RANGE\n                                  [default: 100]\n  -r, --mutation-rate FLOAT RANGE\n                                  [default: 0.05]\n  --color / --no-color            Uses ANSI colors when reporting generation\n                                  results  [default: True]\n\n  --help                          Show this message and exit.\n```\n\n## Contributing\n\nSee [CONTRIBUTING.md](https://github.com/wdsrocha/weasel-cli/blob/master/CONTRIBUTING.md) file for more information.\n\n## License\n\nThis project is licensed under the terms of the MIT license - see the `LICENSE` file for details.\n\n---\n\nIcons made by [Freepik](https://www.flaticon.com/authors/freepik) from [www.flaticon.com](https://www.flaticon.com/).',
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
