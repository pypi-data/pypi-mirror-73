# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyvarint']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pyvarint',
    'version': '0.0.1a2',
    'description': 'Varints, a method of serializing integers using one or more bytes ',
    'long_description': '# pyvarint\n\n[![Build Status](https://drone.autonomic.zone/api/badges/hyperpy/pyvarint/status.svg)](https://drone.autonomic.zone/hyperpy/pyvarint)\n\n## Varints, a method of serializing integers using one or more bytes\n\n## Install\n\n```sh\n$ pip install pyvarint\n```\n\n## Example\n\n```python\nfrom random import sample\nfrom pyvarint import decode, encode\n\nten_rand_ints = sample(range(100), 10)\n\nfor rand_int in ten_rand_ints:\n    encoded = encode(rand_int)\n    decoded = decode(encoded)\n    assert decoded == rand_int\n```\n',
    'author': 'decentral1se',
    'author_email': 'hi@decentral1.se',
    'maintainer': 'decentral1se',
    'maintainer_email': 'hi@decentral1.se',
    'url': 'https://github.com/hyperpy/pyvarint',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
