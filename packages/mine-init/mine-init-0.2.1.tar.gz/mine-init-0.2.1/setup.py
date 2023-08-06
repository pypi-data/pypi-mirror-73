# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mine_init', 'mine_init.extra_files']

package_data = \
{'': ['*']}

install_requires = \
['packmaker==0.4.2']

entry_points = \
{'console_scripts': ['mine-init = mine_init:main']}

setup_kwargs = {
    'name': 'mine-init',
    'version': '0.2.1',
    'description': 'A docker friendly startup routine for Minecraft servers.',
    'long_description': '===========\n mine-init\n===========\n-------------------------------------------------------------\n A container friendly startup routine for Packmaker servers.\n-------------------------------------------------------------\n\n|build-status| |coverage|\n\nMain Documentation\n==================\n\n**mine-init** is a Python based startup routine for `Packmaker`_ based modded Minecraft servers. It can be run on any Linux system and in any container at present. It can be configured via environment variables, flags, and soon config files. (`ini`, `yaml` and `toml` formats are being considered)\n\nIt works by using `Packmaker`_ to download all mods based on a `Packmaker`_ yaml and lock file. It will download the latest mods, and sync the updated configuration and mods into the server directory in a stateful way that preserves runtime data, like the world.\n\nLike `Packmaker`_, **mine-init** can be given multiple pack files, which it will merge from first to last provided. This allows pack developers to release a server with pack related mods, and for server administrators to add their own maintenance packs, with mods for backup; sleep voting; and maps for example.\n\n`Main Index`_\n\n.. |build-status| image:: https://gitlab.routh.io/minecraft/tools/mine-init/badges/master/pipeline.svg\n    :target: https://gitlab.routh.io/minecraft/tools/mine-init/pipelines\n\n.. |coverage| image:: https://gitlab.routh.io/minecraft/tools/mine-init/badges/master/coverage.svg\n    :target: http://minecraft.pages.routh.io/tools/mine-init/reports/\n    :alt: Coverage status\n\n.. _Main Index: http://minecraft.pages.routh.io/tools/mine-init/\n\n.. _Packmaker: https://packmaker.readthedocs.io/\n',
    'author': 'Chris Routh',
    'author_email': 'chris@routh.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.routh.io/minecraft/tools/mine-init',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
