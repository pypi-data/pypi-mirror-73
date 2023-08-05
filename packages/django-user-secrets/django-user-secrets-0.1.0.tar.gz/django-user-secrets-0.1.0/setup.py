# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['user_secrets',
 'user_secrets.migrations',
 'user_secrets_tests',
 'user_secrets_tests.management',
 'user_secrets_tests.management.commands',
 'user_secrets_tests.tests']

package_data = \
{'': ['*'],
 'user_secrets_tests': ['media/*',
                        'static/*',
                        'templates/admin/*',
                        'templates/demo/*']}

install_requires = \
['cryptography', 'django']

entry_points = \
{'console_scripts': ['dev_server = manage:start_test_server',
                     'publish = user_secrets.publish:publish',
                     'update_rst_readme = user_secrets.publish:update_readme']}

setup_kwargs = {
    'name': 'django-user-secrets',
    'version': '0.1.0',
    'description': 'Store user secrets encrypted into database.',
    'long_description': '===================\ndjango-user-secrets\n===================\n\nStore user secrets encrypted into database.\n\nCurrent project state: "Pre-Alpha"\n\nLicence: GPL v3 or above\n\n--------\nthe idea\n--------\n\nStore a user\'s secrets in the database encrypted with his password.\n\nOnly the user can decrypt the stored data. His password is used for encryption and decryption. This password is only transmitted in plain text when logging in (Django itself only saves a salted hash of the password).\n\nThe intermediate-user-secret is decrypted and stored with the clear text password in RAM after successful login. All user secrets will be encrypted and decrypted with his intermediate-user-secret.\n\nLimitations and/or facts:\n\n* Only the same user can decrypt his own data.\n\n* The decrypted data can only be used during an active session.\n\n* A intermediate-user-secret is used, so that a password can be changed without losing the encrypted data.\n\n----\nDEMO\n----\n\nPrepare: `install poetry <https://python-poetry.org/docs/#installation>`_ e.g.:\n\n::\n\n    ~$ sudo apt install python3-pip\n    ~$ pip3 install -U pip --user\n    ~$ pip3 install -U poerty --user\n\nClone the sources, e.g.:\n\n::\n\n    ~$ git clone https://github.com/jedie/django-user-secrets.git\n    ~$ cd django-user-secrets\n    \n    # install via poetry:\n    ~/django-user-secrets$ poetry install\n    \n    # Start Django dev. server:\n    ~/django-user-secrets$ poetry run dev_server\n\nYou can also use our Makefile, e.g.:\n\n::\n\n    ~/django-user-secrets$ make help\n    help                 List all commands\n    install-poetry       install or update poetry\n    install              install django-user-secrets via poetry\n    update               update the sources and installation\n    lint                 Run code formatters and linter\n    fix-code-style       Fix code formatting\n    tox-listenvs         List all tox test environments\n    tox                  Run pytest via tox with all environments\n    tox-py36             Run pytest via tox with *python v3.6*\n    tox-py37             Run pytest via tox with *python v3.7*\n    tox-py38             Run pytest via tox with *python v3.8*\n    pytest               Run pytest\n    update-rst-readme    update README.rst from README.creole\n    publish              Release new version to PyPi\n    start-dev-server     Start Django dev. server with the test project\n\nAlternative/Related projects:\n=============================\n\n* `https://github.com/erikvw/django-crypto-fields <https://github.com/erikvw/django-crypto-fields>`_\n\n* `https://github.com/incuna/django-pgcrypto-fields <https://github.com/incuna/django-pgcrypto-fields>`_\n\n* `https://github.com/georgemarshall/django-cryptography <https://github.com/georgemarshall/django-cryptography>`_\n\n(Random order: No prioritization)\n\n-------\nhistory\n-------\n\n* *dev* - `compare v0.1.0...master <https://github.com/jedie/django-user-secrets/compare/v0.1.0...master>`_\n\n* TBC\n\n* v0.1.0 - 04.07.2020 - `compare init...v0.1.0 <https://github.com/jedie/django-user-secrets/compare/d5700b952...v0.1.0>`_ \n\n    * first release on PyPi\n\n------------\n\n``Note: this file is generated from README.creole 2020-07-04 18:52:44 with "python-creole"``',
    'author': 'Jens Diemer',
    'author_email': 'django-user-secrets@jensdiemer.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jedie/django-user-secrets/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
