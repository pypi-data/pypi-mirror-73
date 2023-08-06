# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['grpc_interceptor']

package_data = \
{'': ['*']}

install_requires = \
['grpcio>=1.8.0,<2.0.0']

setup_kwargs = {
    'name': 'grpc-interceptor',
    'version': '0.1.0',
    'description': 'Simplifies gRPC interceptors',
    'long_description': '# Summary\n\nSimplified Python gRPC interceptors.\n',
    'author': 'Dan Hipschman',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/d5h/grpc-interceptor',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
