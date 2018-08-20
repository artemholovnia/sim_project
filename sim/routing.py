from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from django.conf.urls import url
from ari_controller.consumers import AriChannelsConsumer, ChannelsConsumer
application = ProtocolTypeRouter({
    # Empty for now (http->django views is added by default)
    'websocket':AllowedHostsOriginValidator(
            AuthMiddlewareStack(
                URLRouter(
                    [
                        url(r'^ari_controller/channels/$', ChannelsConsumer),
                        #url(r'^chat/$', ChatConsumer),
                    ]
                )
            )
    )
})