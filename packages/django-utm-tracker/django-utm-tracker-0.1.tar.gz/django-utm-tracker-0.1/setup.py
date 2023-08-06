# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['utm_tracker', 'utm_tracker.migrations']

package_data = \
{'': ['*']}

install_requires = \
['django>=2.2,<4.0']

setup_kwargs = {
    'name': 'django-utm-tracker',
    'version': '0.1',
    'description': 'Django app for extracting and storing UTM tracking values.',
    'long_description': '# Django UTM Tracker\n\nDjango app for extracting and storing UTM tracking values.\n',
    'author': 'YunoJuno',
    'author_email': 'code@yunojuno.com',
    'maintainer': 'YunoJuno',
    'maintainer_email': 'code@yunojuno.com',
    'url': 'https://github.com/yunojuno/django-utm-tracker',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
