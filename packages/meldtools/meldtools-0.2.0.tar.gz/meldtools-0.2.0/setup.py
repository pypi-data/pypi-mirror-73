# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['meldtools']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'pandas>=1.0.5,<2.0.0', 'pandasql>=0.7.3,<0.8.0']

entry_points = \
{'console_scripts': ['meldtools = meldtools.__main__:main']}

setup_kwargs = {
    'name': 'meldtools',
    'version': '0.2.0',
    'description': 'Tools used to work with MELD texts',
    'long_description': '# Meldtools - investigating Middle English documents in Python\n\nMeldtools is a package that allows you to conveniently search Middle English Local Documents corpus.\nIt lets you query the corpus, slice it to easily-definable chunks and work with transcriptions, all\nin one place.\n\n\n# Setting up development environment\n\n* Clone this repository and `cd` into it.\n\n## Python version manager\n\n* Use a Python version manager of your choice.\n* The recommended one to use is [pyenv](https://github.com/pyenv/pyenv).\n* Install Python ^3.8 with your version manager.\n\n## Python package manager\n\n* [Poetry](https://python-poetry.org/) is the package manager used in this project.\n* Follow the installation guide on the website to install Poetry.\n* Run `poetry install` so that Poetry can create a virtual envionment and install the packages into it.\n* Poetry uses `pyproject.toml`, the new configuration file for Python laid out in [PEP 517](https://www.python.org/dev/peps/pep-0517/) and [PEP 518](https://www.python.org/dev/peps/pep-0518/).\n\n## Testing\n\nTo quickly run unit tests run the command like this\n```{sh}\nmake test\n```\n\nOr if you want a full coverage report\n```{sh}\nmake ctest\n```\n\nCheck for type hints by running\n```{sh}\nmake mypy\n```\n\n# Running the command-line program\n\nIn order to run the program key in the following:\n```{sh}\npoetry run meldtools jsonify -d dir/with/rec/files -r path/to/register/csv -\n```\n\nThe program works the Unix way, and it accepts a file or - as a special file that refers to stdout.\n```{sh}\npoetry run meldtools jsonify -d dir/with/rec/files -r path/to/register/csv -\n\n# OR\n\npoetry run meldtools jsonify -d dir/with/rec/files -r path/to/register/csv out.json\n```\n\nYou can direct stdout to a file by appending `> meld.json` to the previous command.\nYou can also pipe stdout directly to `jq`, for example, `poetry run vl-lingo jsonify -d dir/with/rec/files -r /path/to/register/csv - | jq`.\n',
    'author': 'Michał Adamczyk',
    'author_email': 'michal.adamczyk.1990@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
