# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['ntfsdump']
entry_points = \
{'console_scripts': ['ntfsdump = ntfsdump:ntfsdump']}

setup_kwargs = {
    'name': 'ntfsdump',
    'version': '1.0.0',
    'description': 'A tool for exporting any files from an NTFS volume on a Raw Image file.',
    'long_description': '# ntfsdump',
    'author': 'sumeshi',
    'author_email': 'j15322sn@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sumeshi/ntfsdump',
    'package_dir': package_dir,
    'py_modules': modules,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
