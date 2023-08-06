# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['djydoc', 'djydoc.management.commands']

package_data = \
{'': ['*']}

install_requires = \
['django>=2.2.14,<3.0.0']

setup_kwargs = {
    'name': 'djydoc',
    'version': '0.1.3.dev0',
    'description': 'Django wrapper for pydoc',
    'long_description': "# Djydoc\n\nRead Python Documentation within a Django Project.\n\nSo you're happily going along in development and you want to quickly view\ndocumentation in a module. For python modules this is a piece of cake.\n\nHowever, when you try to find out more information about a Django app, you may\nhave come across an error like this...\n\n![error-1](https://gitlab.com/srcrr/djydoc/-/raw/0.1.0-dev/docs/images/error-1.png)\n\nOr like this...\n\n![error-2](https://gitlab.com/srcrr/djydoc/-/raw/0.1.0-dev/docs/images/error-2.png)\n\nAnd you may have done this...\n\n![scream](https://images.pexels.com/photos/3799830/pexels-photo-3799830.jpeg?auto=compress&cs=tinysrgb&h=640&w=426)\n\nBut after installing `djydoc` now you can do this:\n\n![relax](https://images.pexels.com/photos/846080/pexels-photo-846080.jpeg?auto=compress&cs=tinysrgb&h=640&w=426)\n\n\n> Djydoc aims to be a simple drop-in replacement as a `manage.py` command\n> for pydoc so that you can view\n> Python documentation without having to specify `DJANGO_SETTINGS_MODULE` or\n> run django.setup(). Djydoc does that for you.\n\n## Summary\n\n  - [Getting Started](#getting-started)\n  - [Runing the tests](#running-the-tests)\n  - [Deployment](#deployment)\n  - [Built With](#built-with)\n  - [Contributing](#contributing)\n  - [Versioning](#versioning)\n  - [Authors](#authors)\n  - [License](#license)\n  - [Acknowledgments](#acknowledgments)\n\n## Getting Started\n\nThese instructions will get you a copy of the project up and running on\nyour local machine for development and testing purposes. See deployment\nfor notes on how to deploy the project on a live system.\n\n### Prerequisites\n\n- Django 2.2.4+\n- Poetry (optional, to help easily install)\n\n### Installing\n\n#### Option 1 : PIP\n\n    $ pip install djydoc\n\n#### Option 2: Development install via poetry\n\n    $ git clone <git_url>\n    $ cd djydoc\n    $ poetry install\n\n#### Option 3: use as a Django app\n\nJust follow option 2, but don't install with poetry\n\n#### Options 1, 2, or 3: Setup\n\nAdd `'djydoc'` to `INSTALLED_APPS` in `settings`:\n\n```python\nINSTALLED_APPS += [\n  'djydoc'\n]\n```\n\n## Usage\n\nOnce installed djydoc should be available via the `./manage.py` command.\n\nThe intention is for this to be a drop-in replacement for pydoc, so all the\ncommands should work the same (currently `-w` is not implemented):\n\n    $ ./manage.py djydoc django.contrib.auth.models.User\n\n    [ documentation shown ]\n\n    $ ./manage.py djydoc -p 8080\n    Server ready at http://0.0.0.0:8080/\n    Server commands: [b]rowser, [q]uit\n    server>\n\n\n## Running the tests\n\nTesting TBD.\n\n\n## Deployment\n\nFollow common sense django deployment practices.\n\n## Built With\n\n  - [Contributor Covenant](https://www.contributor-covenant.org/) - Used\n    for the Code of Conduct\n  - [Creative Commons](https://creativecommons.org/) - Used to choose\n    the license\n\n## Contributing\n\nPlease read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code\nof conduct, and the process for submitting pull requests to us.\n\n## Versioning\n\nWe use [SemVer](http://semver.org/) for versioning. For the versions\navailable, see the [tags on this\nrepository](https://github.com/PurpleBooth/a-good-readme-template/tags).\n\n## Authors\n\n  - **Jordan H.** - *Code Author* -\n    [SrcRr](https://gitlab.com/srcrr)\n\n\n## License\n\nThis project is licensed under [MIT](LICENSE.md).\n\n## Acknowledgments\n\nTBD\n",
    'author': 'Jordan Hewitt',
    'author_email': 'srcrr@damngood.pro',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/srcrr/djydoc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
}


setup(**setup_kwargs)
