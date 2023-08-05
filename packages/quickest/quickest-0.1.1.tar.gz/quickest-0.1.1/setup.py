# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['quickest']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.2.1,<4.0.0',
 'numpy>=1.16.4,<2.0.0',
 'pandas>=1.0.5,<2.0.0',
 'pyyaml>=5.3.1,<6.0.0',
 'scipy>=1.4.1,<2.0.0']

setup_kwargs = {
    'name': 'quickest',
    'version': '0.1.1',
    'description': 'Tools for studying change detection problems. The justification for this package is that there are libraries for studying Markov chains, and there are libraries for numeric optimisation, but there is no standalone library for optimising the parameters of a Markov decision process.',
    'long_description': '\n# Install\n\n\nSet up the workspace:\n\n\n    . .env\n    chmod +x scripts/*\n\n## Option 1. Install from source\n\n\nInstall ``poetry``, ``pyenv``, ``pylint``, ``sphinx`` and ``pytest``.\n\nBuild and install the library into the local ``pyenv`` environment:\n\n\n    make install\n\n\n## Option 2. Install from PyPI\n\n\nThis is not guaranteed to be the same version as the source in this repository. Check [PyPI](https://pypi.org/project/quickest/) for the latest release date.\n\n    pip install quickest\n\n\n# Test \n\n    pytest\n\n\n# Use\n\n## Train a threshold\n\n    ./scripts/train.sh\n\n## View the last experiment\n\n    ./scripts/simulate.sh\n\n## Profile one training step\n\n    ./scripts/profile.sh\n\n\nPass a `-h` flag to a bash script to see more instructions.\n\n# Documentation\n\nGenerate documentation:\n\n    make doc',
    'author': 'Jenna Riseley',
    'author_email': 'j2.riseley@qut.edu.au',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
