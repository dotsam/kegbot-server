from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import pykeg.web.ws.routing

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter(
          pykeg.web.ws.routing.websocket_urlpatterns
        )
    ),
})
