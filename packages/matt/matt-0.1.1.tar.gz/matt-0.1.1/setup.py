# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['matt']

package_data = \
{'': ['*']}

install_requires = \
['pyxdg>=0.26,<0.27', 'termcolor>=1.1.0,<2.0.0']

extras_require = \
{':platform_system != "Windows"': ['readline>=6.2.4,<7.0.0'],
 ':sys_platform == "windows"': ['colorama>=0.4.3,<0.5.0']}

setup_kwargs = {
    'name': 'matt',
    'version': '0.1.1',
    'description': 'A maths test',
    'long_description': '# Matt\nMatt is a free software (licensed under the [GNU GPL v3 (or later)](https://www.gnu.org/licenses/gpl-3.0.html)) maths test program.\n"Matt" (or "MATT") is a recursive acronym for "MATT Arithmetic Training Test".\n\n## Installation\nMatt depends on:\n * [termcolor](https://pypi.org/project/termcolor/)\n * [pyxdg](https://www.freedesktop.org/wiki/Software/pyxdg/)\n * [colorama](https://pypi.org/project/colorama/) (windows only)\n\nThere are 2 methods of installation: via poetry and via pip:\n\n### Installation via [poetry](https://python-poetry.org/)\nPoetry should handle the installation of dependencies.\nTo install, first clone the git repository, then run:\n```sh\npoetry install\n```\n\n### Installation via pip\nPip should handle the installation of dependencies.\nTo install, run:\n```sh\npython3 -m pip install matt\n```\n\n## Usage\nRun `python3 -m matt -h` for help.\nMatt accepts the following arguments:\n * `--difficulty` or `-d` to set the difficulty (in the format "<namespace>:<number>").\n   The `default` namespace is reserved for the default difficulties.\n   If unspecified the default is `default:1`.\n * `--operations` or `-o` to set the available operations.\n   Operations are seperated by commas, the available operations are:\n   - `+`: Addition\n   - `-`: Subtraction\n   - `*`: Multiplication\n   - `/`: Division\n   Example: `-o +,-` to enable only addition and subtraction.\n * `--minimum` or `-m` to set the minumum, default (if not specified in difficulty): 0.\n * `--maximum` or `-M` to set the maximum, default (if not specified in difficulty): 10.\nNOTE: The maximum must not be equivalent to the minimum.\n\n## Config\nMatt has a configuration file, it is written in Python,\nand located at `$XDG_CONFIG_HOME/matt/config.py`.\nBy default `$XDG_CONFIG_HOME` is set to `~/.config`,\nso if you have not set it then it is probably `~/.config/matt/config.py`.\n\nThe configuration must provide a difficulty function that accepts 2 parameters:\n * `namespace` (str): The namespace of the difficulty.\n * ``number`` (int): The number of the difficulty.\n\nThe ``difficulty`` function must return a dict.\n\nA simple example is:\n```python\ndef difficulty(namespace: str, number: int) -> dict:\n    if namespace == "manual":\n       if number == 1:\n           return {\n               "operations": ["+", "-"],\n               "maximum": 20,\n               "minimum": 10\n           }\n```\n\nDue to the config file being written in Python,\nit is extemely configurable, for example:\n```python\ndef difficulty(namespace: str, number: int) -> dict:\n    if namespace == "automatic":\n        return {\n            "operations": ["+", "-", "*", "/"],\n            "maximum": number * 10\n        }\n```\n',
    'author': 'Noisytoot',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://codeberg.org/noisytoot/matt',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
