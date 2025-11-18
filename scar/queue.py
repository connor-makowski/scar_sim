from heapq import heappop, heappush
from scar.utils import hard_round

class Queue:
    def __init__(self, log_events:bool=False, precision:int=4):
        self.__queue__ = []
        self.__current_time__ = 0.0
        self.__log__ = []
        self.__event_dict__ = {}
        self.__event_id__ = 0
        self.__log_events__ = log_events
        self.__precision__ = precision

    def add(self, time_delta:float, func, args:tuple=tuple(), kwargs:dict=dict()) -> None:
        if time_delta < 0:
            raise ValueError("Cannot schedule events in the past")
        self.__event_id__ += 1
        self.__event_dict__[self.__event_id__] = (self.__event_id__, func, args, kwargs)
        next_time = hard_round(self.__current_time__ + time_delta, self.__precision__)
        heappush(self.__queue__, (next_time, self.__event_id__))

    def process(self):

        self.__current_time__, event_id = heappop(self.__queue__)
        event_id, func, args, kwargs = self.__event_dict__.pop(event_id)
        func(*args, **kwargs)

        if self.__log_events__:
            self.__log__.append({
                'event_id': event_id,
                'time': self.__current_time__,
                'func': func.__name__,
                'args': args,
                'kwargs': kwargs
            })

    def run(self, max_time:float):
        while self.__queue__ and self.__queue__[0][0] <= max_time:
            self.process()
        