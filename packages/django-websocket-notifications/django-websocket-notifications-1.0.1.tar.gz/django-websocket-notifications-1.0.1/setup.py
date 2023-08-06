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
    'version': '1.0.1',
    'description': 'A Django package to handle notifications using Django Channels and WebSockets.',
    'long_description': '==============================\nDjango Websocket Notifications\n==============================\n\nA Django application to deliver user notifications made with \n`django-snitch <https://github.com/marcosgabarda/django-snitch>`_ using WebSockets.\n\n.. image:: https://travis-ci.org/marcosgabarda/django-websocket-notifications.svg?branch=master\n    :target: https://travis-ci.org/marcosgabarda/django-snitch\n\n.. image:: https://img.shields.io/badge/code_style-black-000000.svg\n   :target: https://github.com/ambv/black\n\n\nQuick start\n-----------\n\nThis applications works using django-channels, so, you need to integrate this with \nyour project before to integrate django-websocket-notifications. So, to make the \nquick start as quick and simple as possible, we\'ve made the following assumptions:\n\n* You already have integrated django-channels\n* You are using a channel layer, like Redis\n* You have a `routing.py` file\n* Your project uses DRF to deliver a RESTful API\n\n**1** Install using pip:\n\n.. code-block:: bash\n\n    pip install django-websocket-notifications\n\n**2** Add "websocket_notifications" to your INSTALLED_APPS settings like this:\n\n.. code-block:: python\n\n    INSTALLED_APPS += (\'websocket_notifications\',)\n\n**3** Add the routing patterns to your `routing.py` file:\n\n.. code-block:: python\n\n    from channels.auth import AuthMiddlewareStack\n    from channels.routing import ProtocolTypeRouter, URLRouter\n    from websocket_notifications.routing import websocket_urlpatterns\n\n\n    application = ProtocolTypeRouter(\n        {"websocket": AuthMiddlewareStack(URLRouter(websocket_urlpatterns)),}\n    )\n\n**4** (Optional) In order to test the integration, you can add the following view to your `urls.py` file to be able to access to a testing view:\n\n.. code-block:: python\n\n    urlpatterns += [\n        path(\n            "websocket-notifications/",\n            include(\n                "websocket_notifications.urls",\n                namespace="websocket_notifications",\n            ),\n        ),\n    ]\n\nNow, you can access to `/websocket-notifications/listener/` to check the integration.\n\n**5** Add the ViewSet to the DRF router:\n\n.. code-block:: python\n\n    from websocket_notifications.api.rest_framework import NotificationGroupViewSet\n\n\n    router = routers.DefaultRouter()\n    router.register("websocket-notifications/groups", viewset=NotificationGroupViewSet)\n\n**6** Integrate with `django-snitch`:\n\n.. code-block:: python\n\n    from websocket_notifications.snitch.backends import WebSocketNotificationBackend\n\n\n    @snitch.register(EVENT)\n    class MyEventHandler(snitch.EventHandler):\n        ephemeral = True\n        notification_backends = [WebSocketNotificationBackend]',
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
