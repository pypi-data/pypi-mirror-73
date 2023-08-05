# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['user_visit', 'user_visit.migrations']

package_data = \
{'': ['*']}

install_requires = \
['django>=2.2,<4.0', 'user-agents>=2.1,<3.0']

setup_kwargs = {
    'name': 'django-user-visit',
    'version': '0.1.0.dev0',
    'description': 'Django app used to track user visits.',
    'long_description': "# django-user-visit\n\nDjango app for recording daily user visits\n\nThis app consists of middleware to record user visits, and a\nsingle `UserVisit` model to capture that data.\n\nThe principal behind this is _not_ to record every single\nrequest made by a user. It is to record each daily visit to\na site.\n\nThe one additional factor is that it will record a single daily\nvisit per user/session/device/ip combination. This means that if\na user visits a site multiple times from the same location / same\ndevice, without logging out, then they will be recorded once. If\nthe same user logs in from a different device, IP address, then\nthey will be recorded again.\n\nThe goal is to record unique daily visits per user 'context' (\nwhere context is the location / device combo).\n\nAdmin list view:\n\n![UserVisit list view](assets/screenshot-admin-list-view.png)\n\nAdmin edit view:\n\n![UserVisit edit view](assets/screenshot-admin-edit-view.png)\n",
    'author': 'YunoJuno',
    'author_email': 'code@yunojuno.com',
    'maintainer': 'YunoJuno',
    'maintainer_email': 'code@yunojuno.com',
    'url': 'https://github.com/yunojuno/django-user-visit',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
