# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pypong']

package_data = \
{'': ['*'], 'pypong': ['assets/font/*', 'assets/sfx/*']}

install_requires = \
['pygame==2.0.0.dev10']

entry_points = \
{'console_scripts': ['pypong = pypong.game:main']}

setup_kwargs = {
    'name': 'pypong',
    'version': '0.1.0',
    'description': 'Yet another pong game written in Python',
    'long_description': 'PyPONG\n=======\n\nYet another Pong game written in Python.\n\n.. image:: https://raw.githubusercontent.com/julianolf/pypong/master/screenshot.png\n    :width: 640px\n    :alt: game play screenshot\n\nRequirements\n------------\n\n* Python >= 3.7, < 3.8\n\nInstalling\n----------\n\nUse ``pip`` to download and install the game. ::\n\n    $ pip install pypong\n\nRunning\n-------\n\nJust type ``pypong`` to run the game. ::\n\n    $ pypong\n\nControls\n--------\n\nUse the mouse cursor to control the paddle.\n',
    'author': 'Juliano Fernandes',
    'author_email': 'julianofernandes@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/julianolf/pypong',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
