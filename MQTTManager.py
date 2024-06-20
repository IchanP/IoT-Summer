from lib.simple import MQTTClient 
import ujson

# TODO needs to be reworked slightly.

class MQTTManager:

    def __init__(self, client_id: str, server: str, port: int):
        self.client = MQTTClient(client_id, server, port)
        self.client.connect()

    def enable_subcsription(self, topic, callback):
        self.client.set_callback(callback)
        self.client.subscribe(topic)

    def publish(self, topic: str, msg: str):
        json_msg = ujson.dumps(msg)
        self.client.publish(topic, json_msg)

    def check_msg(self):
        self.client.check_msg()