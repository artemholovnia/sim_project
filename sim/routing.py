from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from django.conf.urls import url
from ari_controller.consumers import AriChannelsConsumer, ChannelsConsumer, BridgesConnectionInfo
application = ProtocolTypeRouter({
    # Empty for now (http->django views is added by default)
    'websocket':AllowedHostsOriginValidator(
            AuthMiddlewareStack(
                URLRouter(
                    [
                        url(r'^/ws/ari_controller/channels/$', ChannelsConsumer),
                        url(r'^/ws/ari_controller/bridges_connection_info/$', BridgesConnectionInfo),
                        #url(r'^chat/$', ChatConsumer),
                    ]
                )
            )
    )
})