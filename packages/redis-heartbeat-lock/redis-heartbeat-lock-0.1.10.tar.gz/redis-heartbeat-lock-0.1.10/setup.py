# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['redis_heartbeat_lock', 'tests']

package_data = \
{'': ['*']}

install_requires = \
['redis', 'uuid']

setup_kwargs = {
    'name': 'redis-heartbeat-lock',
    'version': '0.1.10',
    'description': 'Top-level package for Redis heartbeat lock.',
    'long_description': '=====================\nRedis heartbeat lock\n=====================\n\nBasic Redis locking mechanism, implemented as an asynchronous context manager. Allows the caller to hold a lock, with a specified heartbeat, while doing a chunk of work.\n\n\n* Free software: MIT\n* Documentation: https://redis-heartbeat-lock.readthedocs.io.\n\n\nFeatures\n--------\n\n* TODO\n\nCredits\n-------\n\nThis package was created with Cookiecutter_ and the `briggySmalls/cookiecutter-pypackage`_ project template.\n\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _`briggySmalls/cookiecutter-pypackage`: https://github.com/briggySmalls/cookiecutter-pypackage\n',
    'author': 'Forrest Wallace',
    'author_email': 'forrest.wallace.vt@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fwallacevt/redis-heartbeat-lock',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
