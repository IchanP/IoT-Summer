from lib.simple import MQTTClient 


class MTTQManager:

    def __init__(self, client_id: str, server: str, port: int, user: str, password: str):
        self.user = user
        self.client = MQTTClient(client_id, server, port, user, password)
        self.client.connect()

    def enable_subcsription(self, topic, callback):
        fullfeed = f"{self.user}/feeds/{topic}"
        self.client.set_callback(callback)
        self.client.subscribe(fullfeed)

    def publish(self, topic: str, msg: str):
        fullfeed = f"{self.user}/feeds/{topic}"
        self.client.publish(fullfeed, msg)

    def check_msg(self):
        self.client.check_msg()