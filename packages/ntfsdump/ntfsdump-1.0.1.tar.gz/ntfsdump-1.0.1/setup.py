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
    'version': '1.0.1',
    'description': 'A tool for exporting any files from an NTFS volume on a Raw Image file.',
    'long_description': '# ntfsdump\n\n[![MIT License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENSE)\n[![PyPI version](https://badge.fury.io/py/ntfsdump.svg)](https://badge.fury.io/py/ntfsdump)\n[![Python Versions](https://img.shields.io/pypi/pyversions/ntfsdump.svg)](https://pypi.org/project/ntfsdump/)\n\nA tool for exporting any files from an NTFS volume on a Raw Image file.\n\n\n## Usage\n\n```bash\n$ ntfsdump <dump_target_winpath> --output-path ./out ./path/to/your/imagefile.raw\n```\n\n### Example\nThe target path can be either alone or in a directory.\nIn the case of a directory, it dumps the lower files recursively.\n\n```.bash\n$ ntfsdump /Windows/System32/winevt/Logs -o ./dump ./path/to/your/imagefile.raw\n```\n\n### Required Dependencies\nThis software requires `The Sleuth Kit`.\n\nhttps://www.sleuthkit.org/sleuthkit/\n\n```bash\n$ brew install sleuthkit\n```\n\n## Installation\n\n### via pip\n\n```\n$ pip install ntfsdump\n```\n\nThe source code for ntfsdump is hosted at GitHub, and you may download, fork, and review it from this repository(https://github.com/sumeshi/ntfsdump).\n\nPlease report issues and feature requests. :sushi: :sushi: :sushi:\n\n## License\n\nntfsdump is released under the [MIT](https://github.com/sumeshi/ntfsdump/blob/master/LICENSE) License.\n\nPowered by [](https://github.com/omerbenamram/pyevtx-rs).  ',
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
