# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lirc']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'lirc',
    'version': '0.1.0',
    'description': 'Interact with the daemon in the Linux Infrared Remote Control package',
    'long_description': "LIRC Python Package\n===================\n\n.. image:: https://img.shields.io/badge/python-3.6%20%7C%203.7%20%7C%203.8-blue\n   :target: https://www.python.org/downloads/\n   :alt: Python Version\n.. image:: https://img.shields.io/pypi/v/lirc\n   :target: https://pypi.org/project/lirc/\n   :alt: Project Version\n.. image:: https://readthedocs.org/projects/lirc/badge/?version=latest\n  :target: https://lirc.readthedocs.io/en/latest/?badge=latest\n  :alt: Documentation Status\n.. image:: https://github.com/eugenetriguba/lirc/workflows/python%20package%20ci/badge.svg?branch=master\n  :target: https://github.com/eugenetriguba/lirc/actions/\n  :alt: Build Status\n.. image:: https://codecov.io/gh/eugenetriguba/lirc/graph/badge.svg\n  :target: https://codecov.io/gh/eugenetriguba/lirc\n  :alt: Code Coverage\n.. image:: https://api.codeclimate.com/v1/badges/62b96571ae84f2895531/maintainability\n   :target: https://codeclimate.com/github/eugenetriguba/lirc/maintainability\n   :alt: Maintainability\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/psf/black\n    :alt: Code Formatter\n.. image:: https://img.shields.io/badge/contributions-welcome-brightgreen.svg\n    :target: https://github.com/eugenetriguba/lirc/issues\n    :alt: Contributing\n.. image:: https://img.shields.io/pypi/l/lirc\n   :target: https://pypi.python.org/pypi/lirc/\n   :alt: License\n\nThis is a python package that allows you to interact with the daemon in the\n`Linux Infrared Remote Control <https://lirc.org>`_ package. Interacting with\nthe daemon allows you to send IR signals from a computer.\n\nMore information on the lircd daemon, socket interface,\nreply packet format, etc. can be found at https://www.lirc.org/html/lircd.html\n\nInstallation\n------------\n\nThis package is hosted on PyPI and can be installed\nthrough pip.\n\n.. code-block:: bash\n\n  $ pip install lirc\n\nHowever since this is a wrapper around the LIRC daemon, it\nis expected that LIRC is installed and setup on the given\nsystem as well.\n\nMore information on that can be found in the `installation <https://lirc.readthedocs.io/en/latest/installation.html>`_\nportion of the documentation.\n\nUsing the Lirc Package\n----------------------\n\n.. code-block:: python\n\n  from lirc import Lirc\n\n  lirc = Lirc()\n  response = lirc.version()\n\n  print(response.command)\n  >>> 'VERSION'\n  print(response.success)\n  >>> True\n  print(response.data)\n  >>> ['0.10.1']\n\nTo get started with the package, we import ``Lirc`` and can\ninitialize it with the defaults by passing it no arguments.\n\nThis will assume a socket path of ``/var/run/lirc/lircd``.\nFurthermore, this will also then assume a socket connection\nusing ``AF_UNIX`` and ``SOCK_STREAM``. These are both the defaults\nthat should work on a Linux system. There are ports of LIRC\nto Windows and macOS but using the package there is far less\ncommon. However, both of these are configurable through options\npassed to ``Lirc`` to allow it to be used on those operating systems\nas well.\n\nAfter sending any command to the LIRC daemon, this package will create\na ``LircResponse`` for us that it returns. That response contains the\ncommand we sent to LIRC, whether it was successful, and any data that\nwas returned back to us.\n\nFurther Documentation\n---------------------\n\nMore information on how to setup the system installed LIRC, how to use this python library,\nand a full API specification can be found at https://lirc.readthedocs.io/\n",
    'author': 'Eugene Triguba',
    'author_email': 'eugenetriguba@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/eugenetriguba/lirc',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
