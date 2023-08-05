import json

class Message(object):
    def __init__(self, method, topic, body):
        self.method = method
        self.topic = topic
        self.body = body

    def get_dict(self):
        return {
            "method": self.method,
            "topic": self.topic,
            "body": self.body
        }

    def get_json(self):
        return json.dumps(self.get_dict())