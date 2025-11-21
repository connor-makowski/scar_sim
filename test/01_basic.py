from scar.entity import Facility, Arc, Node
from scar.order import Order
from scar.simulation import Simulation


# Class extensions for custom logic
class Customer(Facility):
    def order_completed(self, order):
        # Set the order_completed method to allocate cashflow when an order completes at the customer.
        # This is needed because the Customer never ships the order further, so the cashflow must be
        # applied on completion.
        order.set_current_cashflow(self.get_cashflow(units=order.units))


simulation = Simulation()

# Create nodes
supplier_00 = simulation.add_object(
    Facility(
        processing_min_time=1,
        processing_avg_time=2,
        processing_sd_time=0.5,
        processing_cashflow_per_unit=-50,
        metadata={
            "loc": "cn_ningbo",
            "oid": "node_supplier_00",
        },
    )
)
factory_01 = simulation.add_object(
    Facility(
        processing_min_time=0.2,
        processing_avg_time=0.5,
        processing_sd_time=0.1,
        processing_cashflow_per_unit=-15,
        metadata={
            "loc": "us_mo_kc",
            "oid": "node_factory_01",
        },
    )
)

warehouse_02 = simulation.add_object(
    Facility(
        processing_min_time=0.5,
        processing_avg_time=1,
        processing_sd_time=0.2,
        processing_cashflow_per_unit=-20,
        metadata={
            "loc": "us_ca_sf",
            "oid": "node_warehouse_02",
        },
    )
)

customer_03 = simulation.add_object(
    Customer(
        processing_min_time=0.1,
        processing_avg_time=0.3,
        processing_sd_time=0.05,
        processing_cashflow_per_unit=200,
        metadata={
            "loc": "us_ca",
            "oid": "node_customer_03",
        },
    )
)

# Create arcs between nodes
arc_00_01 = simulation.add_object(
    Arc(
        origin_node=supplier_00,
        destination_node=factory_01,
        processing_min_time=0.1,
        processing_avg_time=0.2,
        processing_sd_time=0.05,
        processing_cashflow_per_unit=-10,
        metadata={
            "loc": "oc_pa",
            "oid": "arc_ocean_00_01",
        },
    )
)
arc_01_02 = simulation.add_object(
    Arc(
        origin_node=factory_01,
        destination_node=warehouse_02,
        processing_min_time=0.1,
        processing_avg_time=0.3,
        processing_sd_time=0.1,
        processing_cashflow_per_unit=-12,
        metadata={
            "loc": "us_mo_ks",
            "oid": "arc_road_01_02",
        },
    )
)

arc_02_03 = simulation.add_object(
    Arc(
        origin_node=warehouse_02,
        destination_node=customer_03,
        processing_min_time=0.2,
        processing_avg_time=0.4,
        processing_sd_time=0.1,
        processing_cashflow_per_unit=-8,
        metadata={
            "loc": "us_ca",
            "oid": "arc_lm_02_03",
        },
    )
)

order = simulation.add_object(
    Order(
        origin_node=supplier_00,
        destination_node=customer_03,
        units=1,
        planned_path=simulation.graph.get_optimal_path(
            supplier_00, customer_03, "cashflow"
        ),
    )
)

simulation.add_event(
    time_delta=1.0,
    func=order.start,
)

simulation.add_event(
    time_delta=0.5,
    func=arc_01_02.change_processing_parameters,
    kwargs={"processing_avg_time": 5},
)

simulation.add_event(
    time_delta=5.0,
    func=arc_01_02.reset_processing_parameters,
)


simulation.run(max_time=10.0)

from pprint import pprint as print

print(simulation.orders[0].history)
