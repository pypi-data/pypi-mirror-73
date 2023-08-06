from trending_bay_messaging.client import Client

def request(channel, message, publish_only = False, exchange = None, **kwargs):
    client = Client(channel=channel, publish_only=publish_only, **kwargs)
    if exchange is None:
        exchange = "DEFAULT_EXCHANGE"
    return client.request(message, exchange, **kwargs)