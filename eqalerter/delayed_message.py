from base_message import BaseMessage

class DelayedMessage(BaseMessage):

    def __init__(self, timeout, message, title):
        self.message = message
        self.title = title
        self.timeout = timeout
        self.command = f'start cmd /c "timeout /t {timeout} && python stop_watch.py \\"{message}\\" 1 \\"{title}\\""'