
import random
random.seed(42)

class SimulationObject:
    def __init__(self):
        self.id = None
        self.__simulation__ = None

class SimulationEntity(SimulationObject):
    def __init__(
            self,
            processing_min_time: float = 0.0,
            processing_avg_time: float = 0.0,
            processing_sd_time: float = 0.0,
            processing_cashflow_per_unit: float = 0.0,
            metadata: dict = dict()
        ):
        # Basic info
        super().__init__()
        self.entity_type = self.__class__.__name__
        # Split the entity type on uppercase letters and join with underscores
        self.cashflow_key = ''.join(['_' + letter.lower() if letter.isupper() else letter for letter in self.entity_type]).lstrip('_') + '_cashflow'
        self.metadata = metadata

        # Processing defaults
        self.default_processing_min_time = processing_min_time
        self.default_processing_avg_time = processing_avg_time
        self.default_processing_sd_time = processing_sd_time
        self.default_processing_cashflow_per_unit = processing_cashflow_per_unit

        # Live processing info
        self.processing_time_min = processing_min_time
        self.processing_time_avg = processing_avg_time
        self.processing_time_sd = processing_sd_time
        self.processing_cashflow_per_unit = processing_cashflow_per_unit

    def get_metadata(self, **kwargs) -> dict:
        # Return a copy of the metadata dictionary (in case it is modified later)
        return {**dict(self.metadata), **kwargs}

    def get_processing_time(self) -> float:
        return max(self.processing_time_min, random.gauss(self.processing_time_avg, self.processing_time_sd))
    
    def change_processing_parameters(
            self,
            processing_min_time: float | None = None,
            processing_avg_time: float | None = None,
            processing_sd_time: float | None = None,
            processing_cashflow_per_unit: float | None = None
        ) -> None:
        if processing_min_time is not None:
            self.processing_time_min = processing_min_time
        if processing_avg_time is not None:
            self.processing_time_avg = processing_avg_time
        if processing_sd_time is not None:
            self.processing_time_sd = processing_sd_time
        if processing_cashflow_per_unit is not None:
            self.processing_cashflow_per_unit = processing_cashflow_per_unit
        if self.__simulation__ is not None:
            self.__simulation__.graph.update_graphs(self)

    def reset_processing_parameters(self) -> None:
        self.change_processing_parameters(
            processing_min_time=self.default_processing_min_time,
            processing_avg_time=self.default_processing_avg_time,
            processing_sd_time=self.default_processing_sd_time,
            processing_cashflow_per_unit=self.default_processing_cashflow_per_unit
        )

    def get_cashflow(self, units:int) -> float:
        return self.processing_cashflow_per_unit * units

class Node(SimulationEntity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.outbound_id = None

class Arc(SimulationEntity):
    def __init__(self, origin_node: Node, destination_node: Node, **kwargs):
        super().__init__(**kwargs)
        self.origin_node = origin_node
        self.destination_node = destination_node
    
class Facility(Node):
    """
    A Facility class to represent nodes that can hold inventory and process orders.
    This includes Suppliers, Warehouses, and Fulfillment Centers.
    """
    def order_arrived(self, order):
        # TODO: Update inventory levels
        pass

    def order_placed(self, order):
        # TODO: Update capacity levels
        pass

    def order_shipped(self, order):
        # TODO: Update inventory levels
        pass

    def order_completed(self, order):
        """
        A placeholder method to handle logic when an order is completed at this facility.
        This can be overridden in subclasses to implement specific behavior.

        Requires:

        - order (Order): The order that has been completed.

        Returns:

        - None
        """
        pass
