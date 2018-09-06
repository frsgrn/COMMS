import json

# Requests
class Request():
    def __init__(self, route, body):
        self.route = route
        self.body = body
    @staticmethod
    def parse_request(raw):
        try:
            j = json.loads(raw)
            return Request(j["route"], j["body"])
        except:
            return None

# Responses
class Response():
    def __init__(self, sender, content):
        self.sender = sender
        self.content = content
    
    def send_to(self, connection):
        try:
            connection.send(self.get_json().encode())
            return True
        except:
            return False

    def get_json(self):
        return '{"sender": ' + self.sender.get_json() + ', "content": "' + self.content + '"}'

class Sender():
    def __init__(self, name):
        self.name = name
    
    def get_json(self):
        return '{"name":"' + self.name + '"}'

class ServerSender(Sender):
    def __init__(self):
        super(ServerSender, self).__init__("server")

class UserSender(Sender):
    def __init__(self, name, addr):
        super(UserSender, self).__init__(name)
        self.addr = addr

    def get_json(self):
        return '{"name": "' + self.name + '", "addr": "' + self.addr + '"}'