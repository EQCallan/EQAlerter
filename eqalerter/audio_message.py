import pyttsx3
from base_message import BaseMessage

class AudioMessage(BaseMessage):
    def __init__(self, message):
        self.message = message
        self.engine = pyttsx3.init()
        self.engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0')
        self.engine.setProperty('rate', 150)  # You can adjust the speech rate here

    def run(self):
        self.engine.say(self.message)
        self.engine.runAndWait()
