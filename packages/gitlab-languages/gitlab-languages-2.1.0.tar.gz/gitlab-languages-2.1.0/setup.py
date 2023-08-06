# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gitlab_languages']

package_data = \
{'': ['*']}

install_requires = \
['maya>=0.6.1,<0.7.0',
 'prometheus_client>=0.8.0,<0.9.0',
 'python-gitlab>=2.3.0,<3.0.0']

entry_points = \
{'console_scripts': ['gitlab-languages = gitlab_languages.__main__:main',
                     'gitlab_languages = gitlab_languages.__main__:main']}

setup_kwargs = {
    'name': 'gitlab-languages',
    'version': '2.1.0',
    'description': 'Utility to generate a Prometheus data source',
    'long_description': None,
    'author': 'Max Wittig',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
