from datetime import datetime

class Message:
    def __init__(self, message_id, stream_id, con_id, text):
        self.message_id = message_id
        self.stream_id = stream_id
        self.con_id = con_id
        self.timestamp = datetime.now().strftime("%m_%d_%Y_%H%M%S")
        self.text = text

    def __str__(self):
        return f"MESSAGE - connection: {self.con_id} stream: {self.stream_id} msg_id: {self.message_id} timestamp: {self.timestamp} \n text: {self.text}"



