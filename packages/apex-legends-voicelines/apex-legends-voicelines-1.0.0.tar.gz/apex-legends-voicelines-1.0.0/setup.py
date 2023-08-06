# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['apex_legends_voicelines', 'apex_legends_voicelines.assets']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['apex-voicelines = apex_legends_voicelines.__main__:main']}

setup_kwargs = {
    'name': 'apex-legends-voicelines',
    'version': '1.0.0',
    'description': 'Python program to get a random voiceline from an Apex Legend',
    'long_description': '# Apex Legends voicelines\n\n[[_TOC_]]\n\n## What is this package?\n\nI love Apex Legends voice lines so much that I wanted to use it as my window title of my text editor so I created this.\n\nYou can also use it in your terminal too. \n\nJust run `apex-voicelines` in the terminal and it will randomly print one voiceline.\n\n## Install\n\nThis package is available on [PyPI](https://pypi.org/project/apex-legends-voicelines/).\n\nRecommended way to install is by using [pipx](https://github.com/pipxproject/pipx/).\n\nPipx will add isolation so that your system is always unaffected.\n\n```sh\npipx install apex-legends-voicelines\n```\n\nBut you can also install using your standard `pip`.\n\n```sh\npython3 -m pip install apex-legends-voicelines # or pip3 install apex-legends-voicelines\n```\n\n### Prerequsities\n\nYou need Python 3. \n\nRecommended version is Python 3.8.\n\n## Usage\n\nTo use just run `apex-voicelines`\n\nExample:\n\n```sh\n$ apex-voicelines\nMy squad must be very proud - MRVN aka Pathfinder                                                                                               \n```\n\n---\n\n**TODO** Legend selection\n\nMaybe some time later, I will work on specifying which Legend voicelines you need as some argument.\n\nI am thinking of doing something like `apex-voicelines --legend wraith`.\n\n---\n\n**TODO** VSCode support\n\nI don\'t use VSCode much so I don\'t know how to make it work with it. But maybe I will look into it.\n\n---\n\n*If anyone figured on how to use it for some other purpose let me know, I\'m excited.*\n\n### Using inside Emacs\n\nThese voicelines can be used inside Emacs.\n\nYou can use the voicelines as the frame title.\n\nThis is how I use it.\n\n#### As frame title on startup\n\nAdd this to your config\n\n```emacs-lisp\n(setq frame-title-format (shell-command-to-string "apex-voicelines"))\n```\n\n#### Use interactively\n\nYou can also add this in your config and change the title on demand\n\n```emacs-lisp\n(defun change-emacs-title-apex ()\n  (interactive)\n  (setq frame-title-format (shell-command-to-string "apex-voicelines")))\n```\n\nJust run `M-x change-emacs-title-apex` to do so.\n\n## License\n\nMIT License\n',
    'author': 'Justine Kizhakkinedath',
    'author_email': 'justine@kizhak.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://justine.kizhak.com/projects/apex-legends-voicelines',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
