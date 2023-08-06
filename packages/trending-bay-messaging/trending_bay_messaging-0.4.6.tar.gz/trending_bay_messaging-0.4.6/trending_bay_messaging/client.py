import pika
import uuid
import json

class Client(object):

    def __init__(self, channel, publish_only = False):
        # self.connection = pika.BlockingConnection(
        #     pika.ConnectionParameters(host='localhost'))
        #
        # self.channel = self.connection.channel()

        self.channel = channel

        self.publish_only = publish_only

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def request(self, message, exchange = None ,**kwargs):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        if exchange is None:
            exchange = "DEFAULT_EXCHANGE"
        self.channel.basic_publish(
            exchange=exchange,
            routing_key=message.routing_key,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=json.dumps(message.body))
        if not self.publish_only:
            while self.response is None:
                self.channel.connection.process_data_events()
            return json.loads(self.response)
        else:
            return

