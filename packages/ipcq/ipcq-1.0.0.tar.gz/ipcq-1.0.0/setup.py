# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'packages'}

packages = \
['ipcq']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ipcq',
    'version': '1.0.0',
    'description': '',
    'long_description': "# ipcq\n\nA simple inter-process communication (IPC) Queue built on top of the built-in library [multiprocessing](https://docs.python.org/3/library/multiprocessing.html).\n\n## Quick Start\n\n### On the server side\n\n```\nimport ipcq\n\n\nwith ipcq.QueueManagerServer(address=ipcq.Address.DEFAULT, authkey=ipcq.AuthKey.DEFAULT) as server:\n  server.get_queue().get()\n```\n\n### On the client side\n\n```\nimport ipcq\n\n\nclient = ipcq.QueueManagerClient(address=ipcq.Address.DEFAULT, authkey=ipcq.AuthKey.DEFAULT)\nclient.get_queue().put('a message')\n```\n\n## Example\n\nPlease checkout out the [examples](examples) folder.\n\n## API\n\n### class ipcq.QueueManagerServer\n\n#### Constructor\n\nThe same with [multiprocessing.managers.BaseManager](https://docs.python.org/3/library/multiprocessing.html#multiprocessing.managers.BaseManager), please refer to it.\n\n#### Methods\n\nAll methods in [multiprocessing.managers.BaseManager](https://docs.python.org/3/library/multiprocessing.html#multiprocessing.managers.BaseManager) are inherited.\nThe followings are the addtions.\n\n##### get_queue(ident: Optional[Union[AnyStr, int, type(None)]] = None) -> queue.Queue\n\n`ident` is the identity, it can be string-like objects, `int` or `None`. The default is `None`. This is for differetiate the obtained queues.\n\nReturn a queue corresponded with then `ident`.\n\n### class ipcq.QueueManagerClient\n\n#### Constructor\n\nThe same with [multiprocessing.managers.BaseManager](https://docs.python.org/3/library/multiprocessing.html#multiprocessing.managers.BaseManager), please refer to it.\n\n#### Methods\n\nAll methods in [multiprocessing.managers.BaseManager](https://docs.python.org/3/library/multiprocessing.html#multiprocessing.managers.BaseManager) are inherited.\nThe followings are the addtions.\n\n##### get_queue(ident: Optional[Union[AnyStr, int, type(None)]] = None) -> queue.Queue\n\n`ident` is the identity, it can be string-like objects, `int` or `None`. The default is `None`. This is for differetiate the obtained queues.\n\nReturn a queue corresponded with then `ident`.\n",
    'author': 'Henry Chang',
    'author_email': 'mr.changyuheng@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/changyuheng/ipcq',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
