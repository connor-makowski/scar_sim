from scar.entity import Facility, Arc, Node, SimulationObject

class Order(SimulationObject):
    def __init__(self,
        origin_node: Facility,
        destination_node: Facility,
        units:int,
        planned_path: list[int],
        **kwargs
    ):
        super().__init__()
        self.origin_node = origin_node
        self.destination_node = destination_node
        self.units = units

        # History of the Order's progress
        self.history = []

        # Simulation and miscellaneous state
        self.__simulation__ = None
        self.__current_object__ = self.origin_node
        self.__started__ = False
        self.__prev_time__ = 0.0

        self.__planned_path__ = planned_path

    def start(self) -> None:
        if self.__started__:
            raise ValueError("Order has already been started")
        self.__started__ = True
        self.__prev_time__ = self.__simulation__.current_time()
        self.__next__(status="started")

    def __get_next_planned_arc__(self) -> int | None:
        next_object_id = self.__planned_path__[self.__planned_path__.index(self.__current_object__.outbound_id) + 1]
        return self.__simulation__.graph.arc_obj_graph[self.__current_object__.outbound_id][next_object_id]

    def set_current_cashflow(self, cashflow: int|float) -> None:
        self.history[-1]['cashflow'] = cashflow

    def inject_metadata(self, *args, **kwargs) -> dict:
        """
        Inject metadata about the Order into the history log entry when called.

        This method can be overridden to provide custom metadata such as time, order ID, customer info, product info, etc.

        By default, this returns the current simulation time in integer form as 'time'.
        """
        return {'time': int(self.__simulation__.current_time())}

    def __next__(self, status: str) -> None:
        # Log this item into the Order history
        self.history.append({
            'time': self.__simulation__.current_time(),
            'meta': self.__current_object__.get_metadata(**self.inject_metadata()),
            'status': status,
            'cashflow': 0.0,
            't_delta': round(self.__simulation__.current_time() - self.__prev_time__, 3),
        })

        self.__prev_time__ = self.__simulation__.current_time()

        if status == "started":
            # Validate that we are at a Facility that can process orders
            if not isinstance(self.__current_object__, Facility):
                raise ValueError("Current object must be a Facility when started")
            # Perform any logic at the origin facility to process the order (i.e., remove from capacity)
            self.__current_object__.order_placed(self)
            # Set up for shipping
            next_status = "shipped"
        elif status == "shipped":
            # If the current object is a Facility, we need to ship the order (i.e., remove from inventory)
            if isinstance(self.__current_object__, Facility):
                self.__current_object__.order_shipped(self)

            # Pay for processing an order when it is shipped from a node
            self.set_current_cashflow(self.__current_object__.get_cashflow(units=self.units))
            # Given the planned path, set the current object to the next planned Arc
            self.__current_object__ = self.__get_next_planned_arc__()
            next_status = "arrived"
        elif status == "arrived":
            if not isinstance(self.__current_object__, Arc):
                raise ValueError("Current object must be an Arc when arriving")
            # Pay for the transportation when a unit arrives at the destination node
            self.set_current_cashflow(self.__current_object__.get_cashflow(units=self.units))
            # Set the current object to the destination Node of the Arc
            self.__current_object__ = self.__current_object__.destination_node
            if not isinstance(self.__current_object__, Node):
                raise ValueError("Next object must be a Node when arriving")
            if isinstance(self.__current_object__, Facility):
                # Fire off the order arrived event at the Facility for processing (i.e., add to inventory)
                self.__current_object__.order_arrived(self)
            next_status = "completed" if self.__current_object__.id == self.destination_node.id else "shipped"
        elif status == "completed":
            # Validate that we are at a Facility that can receive Orders
            if not isinstance(self.__current_object__, Facility):
                raise ValueError("Current object must be a Facility when completed")
            # Fire off the order completed event at the Facility for processing (i.e., add to capacity)
            self.__current_object__.order_completed(self)
            # When called with "completed", we do not schedule any further events
            return
        else:
            raise ValueError(f"Unknown status: {status}")

        self.__simulation__.add_event(
            time_delta=self.__current_object__.get_processing_time() if next_status != "completed" else 0.0,
            func=self.__next__,
            kwargs={'status': next_status}
        )