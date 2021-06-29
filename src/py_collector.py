from datetime import datetime, timezone, timedelta
from threading import Thread, Event
import signal

class Scheduler(Thread):
    ''' Controls scheduling for py_curator
    
    Based havily on Timer implementation here
    https://github.com/python/cpython/blob/3.9/Lib/threading.py
    '''
    initial_run = True
    alive = True
    
    def __init__(self, start_time=None, milliseconds=0, seconds=0, days=0,minutes=0, weeks=0,
                 timezone = None, count=1, separator=1 ):
        
        signal.signal(signal.SIGALRM, self.cancel)
        Thread.__init__(self)
        self.finished = Event()
        self.count = count
        self.separator_delta =separator
        start_time = datetime.now() if start_time == None else start_time
        
        self.start_diff = abs(round((datetime.now() - start_time).total_seconds(),3))
        self.delta = timedelta(weeks=weeks, 
                               days=days, 
                               minutes=minutes, 
                               seconds=seconds, 
                               milliseconds=milliseconds).total_seconds()
    
    def cancel(self, signum, frame):
        #self.finished.set()
        self.alive = False
        
    def init_run(self, func):
        ''' initial run to handle the wait'''
        if self.initial_run:
            self.initial_run = False
            self.finished.wait(self.start_diff)
            func()
            
    def schedule(self, func):
        ''' takes in a last run datetime, if the specified time interval + last run = 
        _now, return true, otherwise false'''
        
        while self.alive:
            self.init_run(func)

            self.finished.wait(self.delta)
            for i in range(self.count):
                func()
                self.finished.wait(self.separator_delta)

            self.schedule(func)

class Collector:
    
    def upload(self)->None:
        ''' What errors should be here?'''
        raise NotImplementedError('Please see documentation for implementation example')
    
    def is_new(self)->bool:
        raise NotImplementedError('Please see documentation for implementation example')
        
    def orchestrate(self):
        if self.is_new():
            self.upload()
            self.last_run = datetime.now()
        
    def monitor(self)->None:
        self.scheduler.schedule(self.orchestrate)

class Manager:
    
    def __init__(self,  *args):
        self.collectors = args
        
    def verify_collectors(self):
        if len(self.collectors)==0:
            raise RuntimeError('No Collectors were provided!')
            
        for i in self.collectors:
            if not issubclass(i,Collector):
                raise TypeError(f'Was expecing class to subtype Collector, got {i} instead')
                
    def start(self):
        self.verify_collectors()
        for i in self.collectors:
            Thread(target=i().monitor, daemon=True).start()
    