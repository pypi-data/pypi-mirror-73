from trending_bay_messaging.client import Client

def request(channel, message, exchange = None ,**kwargs):
    client = Client(channel=channel)
    if exchange is None:
        exchange = "DEFAULT_EXCHANGE"
    return client.request(message, exchange, **kwargs)