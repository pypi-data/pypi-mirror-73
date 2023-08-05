# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['hypermodern_pypras']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'desert>=2020.1.6,<2021.0.0',
 'marshmallow>=3.6.1,<4.0.0',
 'requests>=2.23.0,<3.0.0']

entry_points = \
{'console_scripts': ['hypermodern-pypras = hypermodern_pypras.console:main']}

setup_kwargs = {
    'name': 'hypermodern-pypras',
    'version': '0.1.0',
    'description': "The hypermodern Python Pras' project",
    'long_description': '[![Tests](https://github.com/prasetiyohadi/hypermodern-pypras/workflows/Tests/badge.svg)](https://github.com/prasetiyohadi/hypermodern-pypras/actions?workflow=Tests)\n[![Codecov](https://codecov.io/gh/prasetiyohadi/hypermodern-pypras/branch/master/graph/badge.svg)](https://codecov.io/gh/prasetiyohadi/hypermodern-pypras)\n[![PyPI](https://img.shields.io/pypi/v/hypermodern-python.svg)](https://pypi.org/project/hypermodern-python/)\n\n# hypermodern-pypras\n\nThe exercise project created as implementation of companion repository for the Hypermodern Python article series<br>\nhttps://medium.com/@cjolowicz/hypermodern-python-d44485d9d769\n',
    'author': 'Prasetiyo Hadi Purwoko',
    'author_email': 'pras@deuterion.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/prasetiyohadi/hypermodern-pypras',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
