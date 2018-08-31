import celery, websocket, requests
from sim.celery import app
from requests.auth import HTTPBasicAuth
from requests.exceptions import ConnectionError
from channels.layers import get_channel_layer
from asgiref.sync import AsyncToSync
import asyncio, json

@app.task
def get_active_channels():
    group_name='channels_group'
    channel_layer = get_channel_layer()
    try:
        active_channels = requests.get('http://192.168.7.110 :8088/ari/channels', auth=HTTPBasicAuth('roip_ari', 'roip_ari')).text
        channels_dict = {'group_name':group_name, 'celery_response':True, 'data':active_channels}
        AsyncToSync(channel_layer.group_send)(group_name, {'type':'send.celery', 'message':channels_dict})
    except ConnectionError:
        AsyncToSync(channel_layer.group_send)(group_name, {'type':'send.message', 'message':'Blad polaczenia z Asteriskiem'})

@app.task
def bridges_connection_info():
    response_list = []
    group_name='bridges_connection_info_group'
    channel_layer = get_channel_layer()
    try:
        bridges_list = json.loads(requests.get('http://192.168.7.110:8088/ari/bridges', auth=HTTPBasicAuth('roip_ari', 'roip_ari')).text)
        print(bridges_list)
        channels_list = json.loads(requests.get('http://192.168.7.110:8088/ari/channels', auth=HTTPBasicAuth('roip_ari', 'roip_ari')).text)
        for bridge in bridges_list:
            itter=0
            bridge_dict = {'id':bridge.get('id'), 'creator':bridge.get('creator'), 'name':bridge.get('name'), 'ari':bridge, 'channels_list':[]}
            active_channels = bridge.get('channels')
            for channel in active_channels:
                for api_channel in channels_list:
                    if api_channel.get('id') == channel:
                        itter+=1
                        bridge_dict.get('channels_list').append(api_channel)
            bridge_dict.update({'channels_count':itter})
            response_list.append(bridge_dict)
        AsyncToSync(channel_layer.group_send)(group_name, {'type':'send.celery', 'message':response_list})
    except ConnectionError:
        AsyncToSync(channel_layer.group_send)(group_name,{'type': 'send.message', 'message': 'Blad polaczenia z Asteriskiem'})

@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(1, get_active_channels.s())
    sender.add_periodic_task(1, bridges_connection_info.s())


#[
# {"id":"2d59f9fa-dc23-4ea0-a6e8-6ca9f20ab4ab","technology":"softmix","bridge_type":"mixing","bridge_class":"base","creator":"ConfBridge","name":"1031","channels":["1535437322.14","1535437326.17"],"video_mode":"none"}
# ]

#[
# {"id":"1535437326.17","name":"SIP/1002-00000005","state":"Up","caller":{"name":"","number":"1002"},"connected":{"name":"","number":""},
# "accountcode":"","dialplan":{"context":"polaczenia","exten":"1031","priority":1},"creationtime":"2018-08-28T06:22:06.694+0000","language":"en"},

# {"id":"1535437322.14","name":"SIP/1001-00000004","state":"Up","caller":{"name":"","number":"1001"},"connected":{"name":"","number":""},
# "accountcode":"","dialplan":{"context":"polaczenia","exten":"1031","priority":1},"creationtime":"2018-08-28T06:22:02.117+0000","language":"en"}
# ]
