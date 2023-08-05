# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['cltk',
 'cltk.alphabet',
 'cltk.alphabet.grc',
 'cltk.core',
 'cltk.data',
 'cltk.dependency',
 'cltk.embeddings',
 'cltk.languages',
 'cltk.lemmatize',
 'cltk.lemmatize.french',
 'cltk.lemmatize.greek',
 'cltk.lemmatize.latin',
 'cltk.lemmatize.old_english',
 'cltk.morphology',
 'cltk.ner',
 'cltk.phonology',
 'cltk.phonology.akkadian',
 'cltk.phonology.arabic',
 'cltk.phonology.arabic.utils',
 'cltk.phonology.arabic.utils.pyarabic',
 'cltk.phonology.gothic',
 'cltk.phonology.greek',
 'cltk.phonology.latin',
 'cltk.phonology.middle_english',
 'cltk.phonology.middle_high_german',
 'cltk.phonology.old_english',
 'cltk.phonology.old_norse',
 'cltk.phonology.old_swedish',
 'cltk.prosody',
 'cltk.prosody.greek',
 'cltk.prosody.latin',
 'cltk.prosody.middle_high_german',
 'cltk.prosody.old_norse',
 'cltk.readers',
 'cltk.sentence',
 'cltk.stem',
 'cltk.stem.akkadian',
 'cltk.stem.french',
 'cltk.stem.latin',
 'cltk.stem.middle_english',
 'cltk.stem.middle_high_german',
 'cltk.stem.sanskrit',
 'cltk.stops',
 'cltk.tag',
 'cltk.tokenize',
 'cltk.tokenize.akkadian',
 'cltk.tokenize.arabic',
 'cltk.tokenize.greek',
 'cltk.tokenize.latin',
 'cltk.tokenize.middle_english',
 'cltk.tokenize.middle_high_german',
 'cltk.tokenize.old_french',
 'cltk.tokenize.old_norse',
 'cltk.tokenize.sanskrit',
 'cltk.tokenizers',
 'cltk.tokenizers.lat',
 'cltk.utils',
 'cltk.wordnet']

package_data = \
{'': ['*']}

install_requires = \
['boltons>=20.0.0,<21.0.0',
 'fasttext>=0.9.1,<0.10.0',
 'gensim>=3.8.1,<4.0.0',
 'gitpython>=3.0,<4.0',
 'greek-accentuation>=1.2.0,<2.0.0',
 'nltk>=3.5,<4.0',
 'python-Levenshtein>=0.12.0,<0.13.0',
 'requests>=2.22.0,<3.0.0',
 'stanza>=1.0.0,<2.0.0',
 'toml>=0.10.1,<0.11.0',
 'tqdm>=4.41.1,<5.0.0']

setup_kwargs = {
    'name': 'cltk',
    'version': '1.0.0a4',
    'description': 'The Classical Language Toolkit',
    'long_description': '.. image:: https://travis-ci.org/cltk/cltk.svg?branch=master\n    :target: https://travis-ci.org/cltk/cltk\n\nAbout\n-----\n\nExperimental CLTK with new ``NLP()`` class.\n\nInstallation\n------------\n\n.. code-block:: bash\n\n   $ pip install cltk\n\n\nDocumentation\n-------------\n\n``$ make docs``\n\n\nDevelopment\n-----------\n\nThe following steps will give you a working development environment.\n\nPython setup\n============\n\nUse ``pyenv`` to manage Python versions and ``poetry`` for package builds.\n\n* Install ``pyenv``:\n   - First time installation; ``curl https://pyenv.run | bash``\n   - To update: ``pyenv update``\n   - Resource: `Managing Multiple Python Versions With pyenv <https://realpython.com/intro-to-pyenv/>`_\n* Install supported versions of the Python language through ``pyenv`` into a dedicated virtualenv:\n   - ``$ pyenv install --list | grep 3.8``\n   - ``$ pyenv install 3.8.3`` (or whatever is latest)\n   - ``$ pyenv virtualenv 3.8.3 cltk``\n   - ``$ pyenv local cltk``. Open a new window and this should be activated (check with ``$ python --version``).\n* Install ``poetry`` to support packaging: ``$ curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python`` (`<https://poetry.eustace.io/docs/>`_)\n* Install dependencies in ``poetry.lock``: ``$ poetry install``\n* Install Stanford NLP models: ``$ poetry run python scripts/download_misc_dependencies.py``\n* Install Graphiz (necessary for building docs): https://graphviz.gitlab.io/download/\n\n\nPackaging\n=========\n\n* Validate structure of ``pyproject.toml``: ``$ poetry check``\n* Update project version with ``poetry``: ``$ poetry version prepatch`` (e.g., ``1.0.0`` to ``1.0.1-alpha.0``)\n   - For minor version: ``$ poetry version preminor`` (``1.0.0`` to ``1.1.0-alpha.0``)\n   - For major version: ``$ poetry version premajor`` (``1.0.0`` to ``2.0.0-alpha.0``)\n* Update all dependencies to latest version (optional): ``$ make updateDependencies``\n* Make package (sdist and wheel): ``$ make build``\n* Check typing: ``$ make typing``\n   - View report at ``.mypy_cache/index.html``\n* Run linter: ``$ make lint``\n   - View report at ``pylint/pylint.html``\n* Auto-format code: ``$ make format``\n* Build docs: ``$ make docs``\n   - View docs at ``docs/_build/html/index.html``\n* Make UML diagrams: ``$ make uml``\n   - View diagrams at ``docs/classes.png`` and ``docs/packages.png``\n* Run the above at each commit  with ``pre-commit``: ``$ poetry run pre-commit install`` (just once)\n* Run tests: ``$ make test``\n* Publish pre-release (permissions required): ``$ make uploadTest``\n* Install from TestPyPI: ``$ make installPyPITest``\n* Repeat the above as necessary\n* Bump version: ``$ poetry version patch`` (e.g., ``1.0.1-alpha.0`` to ``1.0.1``)\n   - For minor version: ``$ poetry version minor`` (``1.0.1-alpha.0`` to ``1.1.0``)\n   - For major version: ``$ poetry version major`` (``1.0.1-alpha.0`` to ``2.0.0``)\n   - If you need to publish multiple versions of an alpha pre-release, run ``$ poetry version prerelease`` (e.g., ``1.0.1-alpha.0`` to ``1.0.1-alpha.1`` to ``1.0.1-alpha.2``)\n* Publish to PyPI (permissions required): ``$ make upload``\n',
    'author': 'Kyle P. Johnson',
    'author_email': 'kyle@kyle-p-johnson.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://cltk.org',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
