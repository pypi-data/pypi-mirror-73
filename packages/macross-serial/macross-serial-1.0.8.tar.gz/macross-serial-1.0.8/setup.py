# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'packages'}

packages = \
['macross_serial']

package_data = \
{'': ['*']}

install_requires = \
['aioserial', 'ipcq>=1.1.1,<2.0.0', 'plumbum']

entry_points = \
{'console_scripts': ['macross-serial = macross_serial.macross_serial:main']}

setup_kwargs = {
    'name': 'macross-serial',
    'version': '1.0.8',
    'description': '',
    'long_description': "# Introduction\n\n## The main goal\nThis project access for the serial port and It is able to script control.\n\n## Installation\n\n```\npip install macross-serial\n```\n\n### For developers\n\n```\ngit clone git@github.com:rondou/macross-serial.git\ncd macross-serial\npoetry install\n```\n\n## Usage\n\n### Access for the serial port and run script.\n\n```\nmacross-serial run [--repeat N] <port-name> <macro-file>\n```\n\n### Show serail port name.\n\n```\nmacross-serial list-port\n```\n\n## Macro file format\n\n```\n<method>\t<content>\t[<timeout-second>\t[progress-message]]\n```\n\n### Simple example\n\n`script.tsv`\n\n```tsv\nwait_for_str\t'system started at UTC'\nsend\t'account\\n'\nsend\t'password\\n'\nwait_for_regex\tr'\\b(([0-9A-Fa-f]{2}:){5})\\b'\nsend\t'reboot\\n'\n```\n\n### Methods\n\n#### send\n\nWrite data to serial port\n\nE.g.\n\n```\nsend\t'poweroff\\n'\n```\n\n#### wait_for_str\n\nWaiting until for find out a specific string then continue to execute next step.\n\nE.g.\n\n```\nwait_for_str\t'system started at UTC'\n```\n\n#### wait_for_regex\n\nWaiting until for find out a regular expression pattern then continue to execute next step.\n\nE.g.\n\n```\nwait_for_regex\tr'\\b(([0-9A-Fa-f]{2}:){5})\\b'\n```\n\n#### wait_for_second\n\nWait/sleep/pause for N seconds.\n\nE.g.\n\n```\nwait_for_second\t10\n```\n",
    'author': 'Rondou Chen',
    'author_email': '40and44sis@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rondou/macross-serial',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.1,<4.0.0',
}


setup(**setup_kwargs)
