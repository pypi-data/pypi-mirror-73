# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pythons']

package_data = \
{'': ['*'], 'pythons': ['assets/font/*']}

install_requires = \
['pygame']

entry_points = \
{'console_scripts': ['pythons = pythons.game:main']}

setup_kwargs = {
    'name': 'pythons',
    'version': '0.1.0',
    'description': 'Yet another snake game written in Python',
    'long_description': 'PYTHONS\n=======\n\nYet another Snake game written in Python.\n\n.. |img1| image:: img/game_start.png\n    :width: 320px\n\n.. |img2| image:: img/game_play.png\n    :width: 320px\n\n.. |img3| image:: img/game_over.png\n    :width: 320px\n\n+--------+--------+--------+\n| |img1| | |img2| | |img3| |\n+--------+--------+--------+\n\nRequirements\n------------\n\n* Python 3.7+\n\nInstalling\n----------\n\nUse ``pip`` to download and install the game. ::\n\n    $ pip install pythons\n\nRunning\n-------\n\nJust type ``pythons`` to run the game. ::\n\n    $ pythons\n',
    'author': 'Juliano Fernandes',
    'author_email': 'julianofernandes@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/julianolf/pythons',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
