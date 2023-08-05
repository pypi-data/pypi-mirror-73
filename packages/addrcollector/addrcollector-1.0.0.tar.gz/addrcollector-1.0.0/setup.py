# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['addrcollector']
install_requires = \
['docopt>=0.6,<0.7', 'xdg>=4,<5']

entry_points = \
{'console_scripts': ['addrcollector = addrcollector:main']}

setup_kwargs = {
    'name': 'addrcollector',
    'version': '1.0.0',
    'description': 'A Python application for collecting email addresses from email messages',
    'long_description': '=============\naddrcollector\n=============\n\nA Python application for collecting email addresses from email messages\n\n-----\nAbout\n-----\n\n*addrcollector* collects email addresses from email messages. This is\nsimilar to Thunderbird\'s "Collected Addresses" feature and\ncorresponding functionality in other software. In the case of\naddrcollector, however, email messages are read from standard input,\nor manually on the command line, and the email address database can be\nqueried by keyword.\n\nIt is possible for addrcollector to be integrated with a mail delivery\nsystem like Procmail or Maildrop to collect addresses from all\nmessages, or with mail clients like Mutt or Alpine to collect\naddresses selectively.\n\nDates and display names are also collected. If an address is seen more\nthan once, then (1) the date is updated and (2) the display name is\nupdated if the new one is longer than the old one.\n\n.. code:: console\n\n   $ addrcollector --help\n   addrcollector: Collect email addresses for later retrieval, or\n   search the database of previously collected addresses.\n\n   Usage:\n     addrcollector.py --add ADDRESS [NAME]\n     addrcollector.py --import\n     addrcollector.py --search WORD...\n     addrcollector.py --help\n\n   Options, arguments, and commands:\n     -a --add      Manually add an address.\n     ADDRESS       Email address to add to database.\n     NAME          Name to associate with email address (optional).\n     -i --import   Import addresses from headers of one message via standard input.\n     -s --search   Search database for addresses; multiple keys are ORed.\n     WORD          Search key.\n     -h --help     Usage help.\n\n------------\nDependencies\n------------\n\naddrcollector depends on the following Python packages not in the\nstandard library:\n\n- docopt\n- xdg\n\n---------------------\nCopyright and License\n---------------------\n\nCopyright 2020 Owen T. Heisler. Creative Commons Zero v1.0 Universal\n(CC0 1.0).\n\nThis program is distributed in the hope that it will be useful, but\nWITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.\n\nThis source code may be used, modified, and/or redistributed according\nto the terms of the Creative Commons Zero 1.0 Universal (CC0 1.0)\nlicense. You should have received a copy of this license along with\nthis program (see `LICENSE`). If not, see\n<https://creativecommons.org/publicdomain/zero/1.0/>.\n',
    'author': 'Owen T. Heisler',
    'author_email': 'writer@owenh.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://owenh.net/addrcollector',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
