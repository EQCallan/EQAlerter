import subprocess
import shlex

class BaseMessage:

    def run(self):
        subprocess.call(shlex.split(self.command), close_fds=True)
