# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['threader3000']
entry_points = \
{'console_scripts': ['threader3000 = threader3000:main']}

setup_kwargs = {
    'name': 'threader3000',
    'version': '0.1.7',
    'description': 'Threader3000 - Multi-threaded Port Scanner',
    'long_description': '<h5>Multi-threaded Python Port Scanner for use on Linux or Windows</h5>\n<br>\n-----------------------------------------------------------------------\n<br>\nThreader3000 is a script written in Python3 that allows multi-threaded port scanning. \nThe program is interactive and simply requires you to run it to begin. Once started, \nyou will be asked to input an IP address or a FQDN as Threader3000 does resolve hostnames. \nA full port scan should take three minutes or less depending on your internet connection.\n<br>\nCheck me out on Twitter @joehelle, Twitch at https://twitch.tv/themayor11/, on Github at \nhttps://github.com/dievus, or visit my cybersec Discord at https://discord.gg/DW4Q4pp.\n',
    'author': 'The Mayor',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
