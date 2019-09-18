from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ApiConsumer(AsyncWebsocketConsumer):
  async def connect(self):
    self.api_endpoint = self.scope['url_route']['kwargs']['api_endpoint']
    self.api_group_name = 'api-%s' % self.api_endpoint

    if self.api_endpoint == 'events':
      await self.channel_layer.group_add(
        self.api_group_name,
        self.api_endpoint
      )

      await self.accept()

  async def disconnect(self, close_code):
    await self.channel_layer.group_discard(
      self.api_group_name,
      self.api_endpoint
    )
