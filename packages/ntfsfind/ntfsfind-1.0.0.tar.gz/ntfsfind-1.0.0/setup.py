# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['ntfsfind']
install_requires = \
['mft>=0.5.3,<0.6.0', 'ntfsdump>=1.0.3,<2.0.0']

entry_points = \
{'console_scripts': ['ntfsfind = ntfsfind:ntfsfind']}

setup_kwargs = {
    'name': 'ntfsfind',
    'version': '1.0.0',
    'description': '',
    'long_description': '# ntfsfind',
    'author': 'sumeshi',
    'author_email': 'j15322sn@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sumeshi/ntfsfind',
    'package_dir': package_dir,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
