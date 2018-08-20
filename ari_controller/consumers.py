import asyncio, json
from channels.consumer import AsyncConsumer
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from asgiref.sync import AsyncToSync
from channels.layers import get_channel_layer

class AriChannelsConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print('connected', event)
        await self.send({
            'type':'websocket.accept',
        })

    async def websocket_receive(self, event):
        #load_data = json.loads(event.get('text', None))
        #print(load_data)
        print('message', type(event.get('text')))
        message = event.get('text', None)
        if message is not None:
            await self.send({
                'type':'websocket.send',
                'text':message.upper(),
            })

    async def websocket_disconnect(self, event):
        print('disconnected', event)


class ChannelsConsumer(AsyncWebsocketConsumer):
    async def websocket_connect(self, event):
        if self.scope['user'].is_authenticated:
            await self.channel_layer.group_add('channels_group', self.channel_name)
            await self.accept()
            await self.channel_layer.send(self.channel_name, {'type':'send.message', 'message':'user {username} connected with channel name "{channel_name}"'.format(username=self.scope['user'].username,
                                                                                                                                                                     channel_name=self.channel_name)})
            await self.channel_layer.group_send('channels_group', {'type':'send.message', 'message':'user {username} connected with channel name "{channel_name}" to group "{group_name}"'.format(channel_name=self.channel_name,
                                                                                                                                                                                             group_name='channels_group',
                                                                                                                                                                                             username=self.scope['user'].username)})
        else:
            await self.channel_layer.send(self.channel_name, 'auth error')

    '''async def websocket_receive(self, event):
        #print(event)
        message = event.get('text')
        await self.channel_layer.group_send('test_group', {'type':'send.message', 'message':'hello group from {channel_name}'.format(channel_name=self.channel_name)})'''

        #data = json.loads(event.get('text'))
        #action, room_id = data.get('action', None), int(data.get('room_id', None))
        #if action == 'join':
        #    print('created_channel')

    async def websocket_disconnect(self, event):
        print('disconnected', event)

    async def send_message(self, message):
        #print(message)
        await self.send(message.get('message'))

    async def send_celery(self, message):
        await self.send(json.dumps(message))
