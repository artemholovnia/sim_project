import celery, websocket, requests
from sim.celery import app
from requests.auth import HTTPBasicAuth
from channels.layers import get_channel_layer
from asgiref.sync import AsyncToSync
import asyncio, json

@app.task
def get_active_channels():
    group_name='channels_group'
    channel_layer = get_channel_layer()
    active_channels = requests.get('http://192.168.7.17:8088/ari/channels', auth=HTTPBasicAuth('roip_ari', 'roip_ari')).text
    channels_dict = {'group_name':group_name, 'celery_response':True, 'data':active_channels}
    AsyncToSync(channel_layer.group_send)(group_name, {'type':'send.celery', 'message':channels_dict})

@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(1, get_active_channels.s())

'''@app.task
def async_send(channel_name, text):
    channel_layer = get_channel_layer()
    AsyncToSync(channel_layer.send)(
            channel_name,
            {"type": "celery.message",
             "text": json.dumps(text)
             })'''

