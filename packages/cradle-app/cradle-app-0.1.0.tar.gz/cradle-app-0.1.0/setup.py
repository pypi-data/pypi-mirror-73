# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['cradle_app']

package_data = \
{'': ['*']}

install_requires = \
['black>=19.10b0,<20.0',
 'fastapi[all]>=0.59.0,<0.60.0',
 'gradio>=1.0.0,<2.0.0',
 'pre-commit>=2.6.0,<3.0.0',
 'typer[all]>=0.3.0,<0.4.0']

entry_points = \
{'console_scripts': ['cradle-app = cradle_app.main:app']}

setup_kwargs = {
    'name': 'cradle-app',
    'version': '0.1.0',
    'description': 'Test ML models in production (or otherwise)',
    'long_description': '# `cradle`\n\n![Lint](https://github.com/swiftdiaries/cradle/workflows/Lint/badge.svg)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n\ncradle is tool to test ML models in production.\n\n**Usage**:\n\n```console\n$ cradle [OPTIONS] COMMAND [ARGS]...\n```\n\n**Options**:\n\n* `--install-completion`: Install completion for the current shell.\n* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.\n* `--help`: Show this message and exit.\n\n**Commands**:\n\n* `init`: init cradle app\n* `launch`: Launch gradio instance\n\n## `cradle init`\n\ninit cradle app\n\n**Usage**:\n\n```console\n$ cradle init [OPTIONS]\n```\n\n**Options**:\n\n* `--help`: Show this message and exit.\n\n## `cradle launch`\n\nLaunch gradio instance\n\n**Usage**:\n\n```console\n$ cradle launch [OPTIONS]\n```\n\n**Options**:\n\n* `--help`: Show this message and exit.\n',
    'author': 'swiftdiaries',
    'author_email': 'adhita94@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
