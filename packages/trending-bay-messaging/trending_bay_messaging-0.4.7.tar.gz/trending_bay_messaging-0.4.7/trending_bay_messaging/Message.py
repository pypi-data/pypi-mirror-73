import json

def get_routing_key(method, topic, status):
    return "{topic}.{method}.{status}".format(topic=topic, method=method, status=status)

class Message(object):
    def __init__(self, method, topic, status, body):
        self.method = method
        self.topic = topic
        self.status = status
        self.body = body
        self.routing_key = get_routing_key(method, topic, status)

    def get_dict(self):
        return {
            "method": self.method,
            "topic": self.topic,
            "status": self.status,
            "body": self.body
        }

    def get_json(self):
        return json.dumps(self.get_dict())

def from_dict(dic):
    return Message(dic["method"], dic["topic"], dic["status"], dic["body"])

def from_json(js):
    return from_dict(json.loads(js))
