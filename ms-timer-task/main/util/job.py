
import threading
from datetime import time, timedelta
import signal
import abc



class ProgramKilled(Exception):
    pass

def signal_handler(signum, frame):
    raise ProgramKilled


class Job(threading.Thread):
    def __init__(self, interval, execute, *args, **kwargs):
        threading.Thread.__init__(self)
        self.daemon = False # si termina la app, se destruye el hilo
        self.stopped = threading.Event()
        self.interval = interval
        self.execute = execute
        self.args = args
        self.kwargs = kwargs
        self.stop_value = False

    def stop(self):
        self.stop_value = True
        self.stopped.set()
        self.join()

    def run(self):
        while not self.stopped.wait(self.interval.total_seconds()):
            if self.stop_value == True:
                break
            self.execute(*self.args, **self.kwargs)

class Task(abc.ABC):
    
    def __init__(self, config = {}):
        self.__config = config
        self.__job = None
        self.init()
    
    def init(self):
        signal.signal(signal.SIGTERM, signal_handler)
        signal.signal(signal.SIGINT, signal_handler)
    
    def run(self):
        if self.__job and self.__job.stop_value == False:
            return
        timer_config = self.__config.get_object('timer')
        self.__job = Job(interval=timedelta(seconds=int(timer_config['WAIT_TIME_SECONDS'])), execute=self.run_task)
        self.__job.start()

    @abc.abstractmethod
    def run_task(self):
        pass

    def stop(self):
        self.__job.stop()