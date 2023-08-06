import pika
import json
from trending_bay_messaging.Message import Message, from_json

def respond(channel, callback, exchange=None, **kwargs):
    channel.queue_declare(queue='rpc_queue')
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='rpc_queue', on_message_callback=lambda ch, method, props, body: on_request(callback, ch, method, props, body, exchange))

    print(" [x] Awaiting RPC requests")
    channel.start_consuming()

def on_request(callback, ch, method, props, message, exchange = None):
    if exchange is None:
        exchange = "DEFAULT_EXCHANGE"
    response = callback(from_json(message).body)

    ch.basic_publish(exchange=exchange,
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=Message(message.method, message.topic, "approved", response).get_json())
    ch.basic_ack(delivery_tag=method.delivery_tag)