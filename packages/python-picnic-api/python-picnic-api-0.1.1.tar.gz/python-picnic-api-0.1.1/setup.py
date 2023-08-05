# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['python_picnic_api']

package_data = \
{'': ['*'], 'python_picnic_api': ['config/default.yaml']}

install_requires = \
['pyyaml>=5.3.1,<6.0.0', 'requests>=2.24.0,<3.0.0']

setup_kwargs = {
    'name': 'python-picnic-api',
    'version': '0.1.1',
    'description': '',
    'long_description': 'Python-Picnic-API\n=================\n\nUnofficial Python wrapper for the Picnic_ API. This API can be used to track upcoming deliveries and to check and manipulate your cart. Use the same credentials as you use for the app. \n\nThis library is not affiliated with Picnic and retrieves data from the endpoints of the mobile application. Use at your own risk.\n\n.. _Picnic: https://picnic.app/nl/',
    'author': 'Mike Brink',
    'author_email': 'mjh.brink@icloud.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/MikeBrink/python-picnic-api',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
