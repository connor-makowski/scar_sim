
from scar.queue import Queue
from scar.entity import Node, Arc, SimulationObject
from scar.order import Order
from scar.graph import Graph


class Simulation:
    def __init__(self):
        # Simulation objects
        self.nodes = {}
        self.arcs = {}
        self.orders = []

        # Stateful queue and graphs
        self.__queue__ = Queue()
        self.graph = Graph()

    def current_time(self) -> float:
        return self.__queue__.__current_time__
    
    def add_event(self, time_delta: float, func, args:tuple=tuple(), kwargs:dict=dict()) -> None:
        self.__queue__.add(time_delta=time_delta, func=func, args=args, kwargs=kwargs)

    def add_object(self, obj: SimulationObject):
        if obj.id is not None:
            raise ValueError("Object is already added to the simulation")
        # Create a ref to this simulation in the object
        obj.__simulation__ = self
        if isinstance(obj, Node):
            # Adding an object to the graph sets its ID
            # It is important to use the graph to create node IDs
            # since nodes are actually two nodes in the graph (inbound and outbound)
            self.graph.add_object(obj)
            self.nodes[obj.id] = obj
        elif isinstance(obj, Arc):
            # Adding an object to the graph sets its ID
            # It is important to use the graph to create arc IDs
            self.graph.add_object(obj)
            self.arcs[obj.id] = obj
        elif isinstance(obj, Order):
            obj.id = len(self.orders)
            # Update the orders list
            self.orders.append(obj)
        else:
            raise ValueError("Object type not recognized for simulation")
        return obj

    def run(self, max_time: float):
        self.__queue__.run(max_time=max_time)