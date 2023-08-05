import pika

def publish(channel, body, exchange = None, **kwargs):
    if exchange is None:
        exchange = os.getenv("DEFAULT_EXCHANGE")
    return channel.basic_publish(exchange=exchange,
                          body=body)