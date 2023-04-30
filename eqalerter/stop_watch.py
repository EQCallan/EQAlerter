import time, sys, math
import pyttsx3
from win10toast import ToastNotifier

def format_time(seconds):
    if (seconds < 120):
        return str(seconds) + 's'
    else:
        mins=int(seconds/60)
        left=seconds % 60
        return str(mins) + 'm:'+ str(left) + 's'

def stopwatch(duration = 2, alert_msg = "timer ended", granularity = 1, title = 'timer'):
    granularity=float(granularity)
    duration=float(duration)
    start = time.time()
    curr = time.time()
    last = start
    fmt = "\r%%.%sf" % (int(abs(round(math.log(granularity,10))))  if granularity<1 else "")
    while (curr-start < duration):
        curr = time.time()
        time_since_screen_update = (curr-last)
        if time_since_screen_update > granularity:
            time_to_run = int(duration) - int(curr-start)
            sys.stdout.write(fmt % (time_to_run) + ' / ' + str(int((duration))) + 's')
            sys.stdout.write("\x1b]2;" + title + ' ' + format_time(time_to_run) + "\x07")
            sys.stdout.flush()
            last = curr
        else:
            time.sleep( granularity - time_since_screen_update )

    engine = pyttsx3.init()
    engine.say(alert_msg)
    engine.runAndWait()

    toaster = ToastNotifier()
    toaster.show_toast(title, alert_msg, duration=5)

if __name__ == '__main__':
    stopwatch(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
