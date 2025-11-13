from scar.entity import Supplier, Warehouse, FulfillmentCenter, Arc
from scar.order import Order
from scar.simulation import Simulation

simulation = Simulation()

# Create nodes
supplier_0 = simulation.add_object(
    Supplier(
        processing_min_time=1,
        processing_avg_time=2,
        processing_sd_time=0.5,
        processing_cost_per_unit=50
    )
)
warehouse_1 = simulation.add_object(
    Warehouse(
        processing_min_time=0.5,
        processing_avg_time=1,
        processing_sd_time=0.2,
        processing_cost_per_unit=20
    )
)
fc_2 = simulation.add_object(
    FulfillmentCenter(
        processing_min_time=0.2,
        processing_avg_time=0.5,
        processing_sd_time=0.1,
        processing_cost_per_unit=15
    )
)

# Create arcs between nodes
arc_0_1 = simulation.add_object(Arc(
    origin_node=supplier_0, 
    destination_node=warehouse_1, 
    processing_min_time=0.1, 
    processing_avg_time=0.2, 
    processing_sd_time=0.05, 
    processing_cost_per_unit=10
))
arc_1_2 = simulation.add_object(Arc(
    origin_node=warehouse_1, 
    destination_node=fc_2, 
    processing_min_time=0.1, 
    processing_avg_time=0.3, 
    processing_sd_time=0.1, 
    processing_cost_per_unit=12
))

order = simulation.add_object(Order(
    origin_node=supplier_0,
    destination_node=fc_2,
    units=1,
    planned_path=simulation.graph.get_optimal_path(supplier_0, fc_2, 'cost')
))

simulation.add_event(
    time_delta=1.0,
    func=order.start,
)

# simulation.add_event(
#     time_delta=1.5,
#     func=arc_1_2.change_processing_parameters,
#     kwargs={'processing_avg_time': 5},
# )

# simulation.add_event(
#     time_delta=10.0,
#     func=arc_1_2.reset_processing_parameters,
# )


simulation.run(max_time=20.0)

from pprint import pp as print
print(order.history)