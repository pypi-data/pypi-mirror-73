# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ankidmpy']

package_data = \
{'': ['*'], 'ankidmpy': ['templates/Default/*']}

entry_points = \
{'console_scripts': ['anki-dm = ankidmpy:main']}

setup_kwargs = {
    'name': 'ankidmpy',
    'version': '0.1.1',
    'description': 'Python port of github.com/OnkelTem/anki-dm',
    'long_description': '# **ankidmpy**\n\n**ankidmpy** ( pronounced "anki-dumpy" ) is a straightforward port of [anki-dm](https://github.com/OnkelTem/anki-dm)    to `python`.   The original **anki-dm** is written in `PHP` and is a tool to work with the [CrowdAnki plugin](https://github.com/Stvad/CrowdAnki) for the [Anki](https://apps.ankiweb.net/) spaced repetition memory app to facilitate collaborative building of flash card decks. \n\n## Overview\n**CrowdAnki** also aims to facilitate collaboration by extracting all the details of an Anki deck into a single json file for easier editing.  Building on this, **anki-dm** splits this single json file into several files: one containing the raw data, one each for template layout of the cards, one for css styling, etc. allowing each of them to be edited independently.\n\nReversing the process, you can *build* a **CrowdAnki** file from these edited files and in turn *import* these files back into **Anki** with the plug-in to be used for spaced repetition memorization.\n\n## Usage\nThe usage is nearly identical to the original **anki-dm** with only slight differences to accommodate standard arg parsing in `python`.\n\n```sh\n$ python -m ankidmpy --help\nusage: anki-dm [-h] [--base BASE] [--templates]\n               {init,import,build,copy,index} ...\n\nThis tool disassembles CrowdAnki decks into collections of files and\ndirectories which are easy to maintain. It then allows you to can create\nvariants of your deck via combining fields, templates and data that you really\nneed. You can also use this tool to create translations of your deck by\ncreating localized columns in data files.\n\npositional arguments:\n  {init,import,build,copy,index}\n    init                Create a new deck from a template.\n    import              Import a CrowdAnki deck to Anki-dm format\n    build               Build Anki-dm deck into CrowdAnki format\n    copy                Make reindexed copy of Anki-dm deck.\n    index               Set guids for rows missing them.\n\noptional arguments:\n  -h, --help            show this help message and exit\n  --base BASE           Path to the deck set directory. [Default: src]\n  --templates           List all available templates.\n$\n```\nThere are several sub-commands which each take their own options.   The `--base` switch applies to each of these sub-commands and must be supplied before the sub-command.   This switch indicates the root directory to use when looking for or generating new files.\n\nThe `--templates` switch simply lists the sample **CrowdAnki** decks which can be built upon to generate new decks and doesn\'t require a sub-command.\n\nHelp for the sub-commands can be found by applying `--help` to the sub-command:\n\n```sh\n$ python -m ankidmpy init --help\nusage: anki-dm init [-h] [--deck DECK] template\n\npositional arguments:\n  template     Template to use when creating the deck set.\n\noptional arguments:\n  -h, --help   show this help message and exit\n  --deck DECK  Name of the default deck of the deck set being created. If not\n               provided, then the original deck/template name will be used.\n$\n```\n\n## Building\n**ankidmpy** is currently written in Pure `Python` with no dependencies.  I\'ve only tried it with `python3.7` so far but it may work in earlier versions.\n\nYou can run **ankidmpy** with `python -m ankidmpy` by pointing your `PYTHONPATH` at the `src` directory or you can use [poetry](https://python-poetry.org/docs/) to build a wheel distribution like so:\n\n```sh\n$ poetry install\n$ poetry build\n```\nOnce you run `poetry install` you can also run **ankidmpy** using the **poetry** script like so:\n\n```sh\n$ poetry run anki-dm --help\n```\nSee the **poetry** documentation for more details.\n',
    'author': 'Douglas Mennella',
    'author_email': 'trx2358-pypi@yahoo.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gitonthescene/ankidmpy',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
