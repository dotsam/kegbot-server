from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from kegbot.util import kbjson
from pykeg.proto import protolib



def publish_events(events):
    """Publishes a set of events on the websocket group."""
    channel_layer = get_channel_layer()

    events = [{'type': 'event', 'data': protolib.ToDict(e, True)} for e in events]
    for event in events:
        async_to_sync(channel_layer.group_send)('api-events', event)
