# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['websocket_notifications',
 'websocket_notifications.api',
 'websocket_notifications.migrations',
 'websocket_notifications.snitch']

package_data = \
{'': ['*'], 'websocket_notifications': ['templates/websocket_notifications/*']}

install_requires = \
['channels>=2.4.0,<3.0.0',
 'django-model-utils>=4.0.0,<5.0.0',
 'django-snitch>=1.7.1,<2.0.0',
 'django>=3.0.7,<4.0.0',
 'djangorestframework>=3.11.0,<4.0.0']

setup_kwargs = {
    'name': 'django-websocket-notifications',
    'version': '1.0.0',
    'description': 'A Django package to handle notifications using Django Channels and WebSockets.',
    'long_description': '==============================\nDjango Websocket Notifications\n==============================\n\nA Django application to deliver user notifications made with \n`django-snitch <https://github.com/marcosgabarda/django-snitch>`_ using WebSockets.\n',
    'author': 'Marcos Gabarda',
    'author_email': 'hey@marcosgabarda.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/marcosgabarda/django-websocket-notifications',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
