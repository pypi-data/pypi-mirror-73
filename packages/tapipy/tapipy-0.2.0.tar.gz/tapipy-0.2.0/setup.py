# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tapipy']

package_data = \
{'': ['*'], 'tapipy': ['resources/*']}

install_requires = \
['certifi>=14.05.14,<15.0.0',
 'jwt>=1.0.0,<2.0.0',
 'openapi_core>=0.13.0,<0.14.0',
 'python_dateutil>=2.5.3,<3.0.0',
 'requests',
 'setuptools>=21.0.0,<22.0.0',
 'six>=1.10,<2.0',
 'urllib3>=1.15.1,<2.0.0']

setup_kwargs = {
    'name': 'tapipy',
    'version': '0.2.0',
    'description': 'Python lib for interacting with an instance of the Tapis API Framework',
    'long_description': "# tapipy - Tapis V3 Python SDK\n\nPython library for interacting with an instance of the Tapis API Framework.\n\n## Development\n\nThis project is under active development, exploring different approaches to SDK generation.\n\n## Installation\n\n```\npip install tapipy\n```\n\n## Running the tests\n\nTests resources are contained within the `test` directory. `Dockerfile-tests` is at root.\n1. Build the test docker image: `docker build -t tapis/tapipy-tests -f Dockerfile-tests .`\n2. Run these tests using the built docker image: `docker run -it --rm  tapis/tapipy-tests`\n\n## Usage\n\nTODO - provide working examples, e.g., \n```\nimport tapipy\nt = tapipy.Tapis(base_url='http://localhost:5001')\nreq = t.tokens.NewTokenRequest(token_type='service', token_tenant_id='dev', token_username='admin')\nt.tokens.create_token(req)\n\nimport openapi_client\nconfiguration = openapi_client.Configuration()\nconfiguration.host = 'http://localhost:5001'\napi_instance = openapi_client.TokensApi(openapi_client.ApiClient(configuration))\n\nnew_token = openapi_client.NewTokenRequest(token_type='service', token_tenant_id='dev', token_username='admin')\n\nresp = api_instance.create_token(new_token)\njwt = resp.get('result').get('access_token').get('access_token')\n```\n\n## Build instructions\n\nBuilding is done with poetry as follows:\n```\npip install poetry\npoetry install\n```\nThis installs `tapipy` to a virtual environment. Run a shell in this environment with:\n```\npoetry shell\n```\n\nTo install locally (not in a virtual environment):\n```\npip install poetry\npoetry build\ncd dists\npip install *.whl\n```\n",
    'author': 'Joe Stubbs',
    'author_email': 'jstubbs@tacc.utexas.edu',
    'maintainer': 'Joe Stubbs',
    'maintainer_email': 'jstubbs@tacc.utexas.edu',
    'url': 'https://github.com/tapis-project/python-sdk',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
