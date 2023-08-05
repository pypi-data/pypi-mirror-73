# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jsontofu']

package_data = \
{'': ['*']}

install_requires = \
['jsonpickle']

setup_kwargs = {
    'name': 'jsontofu',
    'version': '1.0.0',
    'description': 'Json raw data to object',
    'long_description': '.. image:: jsontofu.png\n\nUsage\n-----\n\n.. code:: python\n\n    @dataclass\n    class Data:\n        str_data: str\n        int_data: int\n        \n    @dataclass\n    class DictData:\n        str_data: str\n        dict_data: Optional[Dict]\n        \n    @dataclass\n    class RecursiveData:\n        str_data: str\n        dict_data: Data\n        \n    json_data1 = {\n        \'str_data\': \'test\',\n        \'int_data\': 123\n    }\n             \n    json_data2 = {, \n        \'str_data\': \'test\',\n        \'dict_data\': {\'key1\': 123, \'key2\': 456}\n    }\n        \n    json_data3 = {, \n        \'str_data\': \'test\',\n        \'dict_data\': {\'str_data\': \'test\', \'int_data\': 456}\n    }\n    \n    print(jsontofu.decode(json_data1, Data)) # Data(str_data="test", int_data=123)\n    \n    print(jsontofu.decode(json_data2, DictData)) # DictData(str_data="test", dict_data={\'key1\': 123, \'key2\': 456})\n    \n    print(jsontofu.decode(json_data3, RecursiveData)) # RecursiveData(str_data="test", Data(str_data="test", int_data=456)\n    \n\nInstallation\n------------\n\n.. code:: sh\n\n    pip install git+git://github.com/rondou/jsontofu.git\n\nor\n\n.. code:: sh\n\n    pipenv install \'git+ssh://git@github.com/rondou/jsontofu.git#egg=jsontofu\'\n\n\nDevelopment\n-----------\n\n.. code:: sh\n\n    pipenv install\n    pipenv install -d\n    pipenv run "pytest -s"\n\nCoverage\n-----------\n\n.. code:: sh\n\n    pipenv run \'pytest tests --cov=jsontofu\'\n',
    'author': 'Rondou Chen',
    'author_email': '40and44sis@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rondou/jsontofu',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.7,<4.0.0',
}


setup(**setup_kwargs)
