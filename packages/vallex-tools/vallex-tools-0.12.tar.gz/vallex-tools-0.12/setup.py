# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vallex',
 'vallex.cli',
 'vallex.cli.commands',
 'vallex.data_structures',
 'vallex.gui',
 'vallex.scripts',
 'vallex.scripts.dynamic_properties',
 'vallex.scripts.mapreducers',
 'vallex.scripts.tests',
 'vallex.scripts.transforms',
 'vallex.server',
 'vallex.server.db_migrations',
 'vallex.vendor']

package_data = \
{'': ['*'], 'vallex': ['templates/*']}

install_requires = \
['jinja2', 'pyqt5==5.14.1', 'pyqtwebengine==5.14']

extras_require = \
{'server': ['gunicorn>=20.0.4,<21.0.0', 'setproctitle>=1.1.10,<2.0.0'],
 'updater': ['bsdiff4==1.1.5', 'pynacl']}

entry_points = \
{'console_scripts': ['vallex-cli = vallex.main:entry_point',
                     'vallex-gui = vallex.main:gui_entry_point',
                     'vallex-web = vallex.main:web_entry_point']}

setup_kwargs = {
    'name': 'vallex-tools',
    'version': '0.12',
    'description': 'A Python interface for working with vallency lexicon data.',
    'long_description': "Vallex Tools\n============\n\n| A Python interface to various vallency lexicon (Vallex) data.\n| https://verner.gitlab.io/pyvallex/\n\n.. code-block:: bash\n\n    pip install vallex-tools\n\n\nFeatures\n--------\n- `MIT <https://en.wikipedia.org/wiki/MIT_License>`_ licensed\n- parses lexicon data in txt and json formats\n- provides a cli for working with the data (searching, printing histogram, converting between txt/json, running data tests)\n- infrastructure to run data tests\n- Qt(WebEngine) based ui (searching, simple editing)\n- web based interface (searching)\n\nExample Use\n-----------\n\n.. code-block:: python\n\n    from vallex import LexiconCollection, add_file_to_collection\n    from vallex.grep import parse_pattern, filter_db\n\n\n    # Create a collection of lexicons\n    coll = LexiconCollection()\n\n    # Load a lexicon and add it to the collections\n    add_file_to_collection(coll, open('v-vallex.txt', 'r', encoding='utf-8'))\n\n\n    # Filter the collection looking for lexical units which have ACT in their frame\n    pat = parse_pattern('frame.functor=ACT')\n    coll = filter_db(coll, pat)\n\n\n    # Print out the frame attribute of each lexical unit in the filtered\n    # collection\n    for lu in coll.lexical_units:\n        print(lu.frame)\n\nIt also includes a cli interface:\n\n.. code-block:: bash\n\n    $ vallex-cli -i v-vallex.txt --filter frame,lemma,refl -- grep frame.functor=ACT\n\n      ...\n\n    * ŽRÁT SE\n      : id: blu-v-žrát-se-1\n      ~ impf: žrát se\n      + ACT(1;obl)CAUS(7,pro+4;typ)\n    #\n    # END ========== ../data-txt/v-vallex.txt ========== END\n\n    $ vallex-cli -i v-vallex.json --histogram frame.functor -- grep frame.functor=ACT\n\n      ...\n\n    NTT                                  (186/17819)\n    DPHR  *                               (286/17819)\n    DIR1  *                               (286/17819)\n    MANN  *                               (325/17819)\n    ORIG  *                               (382/17819)\n    DIR   **                              (484/17819)\n    EFF   ***                             (601/17819)\n    LOC   ***                             (606/17819)\n    DIR3  ***                             (610/17819)\n    BEN   ***                             (637/17819)\n    ADDR  ***                             (731/17819)\n    MEANS ****                            (809/17819)\n    PAT   ************************        (4836/17819)\n    ACT   ******************************* (6176/17819)\n\n\nInstalling the command-line tools\n---------------------------------\n\nUnix\n####\n\nWe suggest using the `pipx <https://pipxproject.github.io/pipx/>`_ or `pipsi <https://github.com/mitsuhiko/pipsi>`_ script installers:\n\n.. code-block:: bash\n\n    $ python3 -m pip install --user pipx\n    $ python3 -m pipx ensurepath\n    $ pipx install vallex-tools\n\n\nAlternatively, just create a Python3 virtualenv and run vallex-tools from there:\n\n.. code-block:: bash\n\n    $ python3 -m virtualenv -p `which python3` venv\n    $ . venv/bin/activate\n    (venv) $ pip install vallex-tools\n\nAssuming you used `pipx` to install vallex-tools, you can get bash command completion for `vallex-cli`,\nby putting the following line into your `.bashrc` or `.bash_profile`:\n\n.. code-block:: bash\n\n    eval $(pipx run vallex-cli completion)\n\n(For `pipsi`, replace `pipx` with `pipsi`. For the virtualenv, you need to first activate the virtualenv,\nthen run the eval with just `vallex-cli` instead of pipx, and then deactivate the environment again).\n\nWindows\n#######\n\nRun the `install-win.ps1 <https://verner.gitlab.io/pyvallex/_static/install-win.ps1>`_ script in a\n`PowerShell` prompt. This script will download and install a Python interpretter into `C:\\\\vallex-tools`\nand the it will use it to install the `vallex-tools` package. Finally, it will put a shortcut to run\nthe `vallex-gui` on the desktop. Using this method, all configuration & logs will live in the\n`C:\\\\vallex-tools` directory. To change this directory, you can edit the script and change the\ndefinition of the `$install_path` variable.\n\nContributing\n------------\n\nPlease see `Developer documentation <https://verner.gitlab.io/pyvallex/development.html>`_\nfor documentation describing how to set-up your environment for working on vallex-tools.\n\n\n.. Obtaining Lexicon Data\n.. ----------------------\n..\n..\n.. Command Line Interface\n.. ----------------------\n..\n..\n.. Web Interface\n.. -------------\n..\n..\n.. Data Validation Tests\n.. ---------------------\n..\n.. REST API\n.. --------\n..\n.. Please see :doc:`REST API documentation <restapi>`.\n..\n.. Development\n.. -----------\n..\n.. Please see :doc:`Developer documentation <development>`.\n\n.. Documentation\n.. -------------\n\n.. Please see the :doc:`Intro` for more details.\n\n\n.. Bugs/Requests\n.. -------------\n\n.. Please use the `GitLab issue tracker <{{cookiecutter.bug_url}}>`_ to submit bugs or request features.\n\n\n.. Changelog\n.. ---------\n\n.. Consult the :doc:`Changelog <changelog>` page for fixes and enhancements of each version.\n\n",
    'author': 'Jonathan L. Verner',
    'author_email': 'jonathan.verner@matfyz.cz',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://verner.gitlab.io/pyvallex/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
