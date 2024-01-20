# steam/routing.py
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from notificaciones.routing import application as notificaciones_application

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            notificaciones_application
        )
    ),
    # Otros protocolos aquí, si es necesario
})
