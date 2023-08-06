# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['modern_python_setup']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'desert>=2020.1.6,<2021.0.0',
 'marshmallow>=3.7.0,<4.0.0',
 'requests>=2.24.0,<3.0.0']

entry_points = \
{'console_scripts': ['modern-python-setup = modern_python_setup.console:main']}

setup_kwargs = {
    'name': 'modern-python-setup',
    'version': '0.1.0',
    'description': 'The Modern Python Setup project',
    'long_description': '[![Tests](https://github.com/hubplug/modern-python-setup/workflows/Tests/badge.svg)](https://github.com/hubplug/modern-python-setup/actions?workflow=Tests)\n[![Codecov](https://codecov.io/gh/hubplug/modern-python-setup/branch/master/graph/badge.svg)](https://codecov.io/gh/hubplug/modern-python-setup)\n\n# modern-python-setup\nBased on [Hypermodern Python](https://cjolowicz.github.io/posts/hypermodern-python-01-setup/) by [CLAUDIO JOLOWICZ](https://cjolowicz.github.io/)\n',
    'author': 'Hub Plug',
    'author_email': '31110528+hubplug@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hubplug/modern-python-setup',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
