# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['emoji']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.1,<5.0.0',
 'lxml>=4.5.1,<5.0.0',
 'requests>=2.24.0,<3.0.0']

entry_points = \
{'console_scripts': ['emoji-search = console:main']}

setup_kwargs = {
    'name': 'emoji-search',
    'version': '0.0.3',
    'description': '',
    'long_description': '# `emoji-search`\n\n[![](https://img.shields.io/pypi/v/emoji-search.svg?style=flat)](https://pypi.org/pypi/emoji-search/)\n[![](https://img.shields.io/pypi/dw/emoji-search.svg?style=flat)](https://pypi.org/pypi/emoji-search/)\n[![](https://img.shields.io/pypi/pyversions/emoji-search.svg?style=flat)](https://pypi.org/pypi/emoji-search/)\n[![](https://img.shields.io/pypi/format/emoji-search.svg?style=flat)](https://pypi.org/pypi/emoji-search/)\n[![](https://img.shields.io/pypi/l/emoji-search.svg?style=flat)](https://github.com/dawsonbooth/emoji-search/blob/master/LICENSE)\n\n# Description\n\nThis is a short or long textual description of the package.\n\n# Installation\n\nWith [Python](https://www.python.org/downloads/) installed, simply run the following command to add the package to your project.\n\n```bash\npip install emoji-search\n```\n\n# Usage\n\nThe following is an example usage of the package:\n\n```python\nfrom foo import bar\n\nprint("Ok here we go")\n\ntry:\n    bar()\nexcept:\n    print("Ah good effort")\n```\n\nSome info about calling the program.\n\n```bash\npython whatever.py > out.txt\n```\nThen some output (console or file whatever)\n\n```txt\nOutput here I guess\n```\n\n# License\n\nThis software is released under the terms of [MIT license](LICENSE).\n',
    'author': 'Dawson Booth',
    'author_email': 'pypi@dawsonbooth.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dawsonbooth/emoji-search',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
