from base_message import BaseMessage
import os

class VisualMessage(BaseMessage):

    def __init__(self, message):
        self.message = message
        username = os.getlogin()
        base_command = f'msg {username} /TIME:1 /W /I "{message}"'
        self.command = base_command
