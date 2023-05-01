import subprocess

class BaseMessage:

    def run(self):
        subprocess.Popen(self.command, shell=True)

