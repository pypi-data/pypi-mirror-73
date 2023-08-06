# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['matt']

package_data = \
{'': ['*']}

install_requires = \
['pyxdg>=0.26,<0.27', 'termcolor>=1.1.0,<2.0.0']

extras_require = \
{':sys_platform == "windows"': ['colorama>=0.4.3,<0.5.0']}

setup_kwargs = {
    'name': 'matt',
    'version': '0.1.0',
    'description': 'A maths test',
    'long_description': None,
    'author': 'Noisytoot',
    'author_email': 'noisytoot@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://git.noisytoot.org/noisytoot/matt',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
