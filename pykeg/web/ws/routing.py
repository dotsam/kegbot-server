from django.conf.urls import url

from . import consumers

websocket_urlpatterns = [
    url(r"^/api/(?P<api_endpoint>[a-zA-Z0-9_]+)/$", consumers.ApiConsumer),
]
