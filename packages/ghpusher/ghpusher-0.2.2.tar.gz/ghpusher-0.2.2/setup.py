# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ghpusher']

package_data = \
{'': ['*']}

install_requires = \
['Click>=7.0,<8.0', 'plumbum>=1.6.9,<2.0.0']

entry_points = \
{'console_scripts': ['gh-pusher = ghpusher.gh_pusher:gh_push']}

setup_kwargs = {
    'name': 'ghpusher',
    'version': '0.2.2',
    'description': 'Push HTML to a github pages branch',
    'long_description': '# gh-pusher\n\nA tool to push changes to a gh-pages branch.\n\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ghpusher) ![PyPI](https://img.shields.io/pypi/v/ghpusher.svg) [![Actions Status](https://github.com/dbradf/gh-pusher/workflows/test-python-project/badge.svg)](https://github.com/dbradf/gh-pusher/actions)\n\n\n## Install\n\n```bash\n$ pip install ghpusher\n```\n\n## Usage\n\n```\n$ gh-pusher --help\nUsage: gh-pusher [OPTIONS]\n\n  Publish documentation changes to a github changes branch.\n\n  Move a directory of built documentation from the build directory to  the\n  base on the repository on the target github pages branch. If there are any\n  changes to the documention, they will be added in a commit under the same\n  author and commit message as the last commit message on the active branch.\n\nOptions:\n  --target-branch TEXT  Branch to publish documentation.\n  --build-dir PATH      Directory containing documentation to publish.\n                        [required]\n\n  --git-binary PATH     Path to git binary.\n  --repo-base PATH      Path to base of repository.\n  --help                Show this message and exit.\n```\n',
    'author': 'David Bradford',
    'author_email': 'david.bradford@mongodb.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dbradf/gh-pusher',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
