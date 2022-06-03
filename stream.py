from pyexpat.errors import messages

class Stream:
    def __init__(self, stream_id, con_id):
        self.stream_id = stream_id
        self.con_id = con_id
        self.messages = []

    def get_messages(self):
        return self.messages

    def add_message(self, msg):
        self.messages.append(msg)
    
    def __str__(self):
        info = f"stream: {self.stream_id} \n"
        for message in self.messages:
            info += str(message)
        return info

