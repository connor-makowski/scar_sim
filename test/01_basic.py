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
supplier_0 = simulation.add_object(
    Facility(
        processing_min_time=1,
        processing_avg_time=2,
        processing_sd_time=0.5,
        processing_cashflow_per_unit=-50,
        metadata={
            'loc': 'cn_ningbo',
            'otype': 'node_supplier',
        }
    )
)
factory_1 = simulation.add_object(
    Facility(
        processing_min_time=0.2,
        processing_avg_time=0.5,
        processing_sd_time=0.1,
        processing_cashflow_per_unit=-15,
        metadata={
            'loc': 'us_ks_kc',
            'otype': 'node_factory',
        }
    )
)

warehouse_2 = simulation.add_object(
    Facility(
        processing_min_time=0.5,
        processing_avg_time=1,
        processing_sd_time=0.2,
        processing_cashflow_per_unit=-20,
        metadata={
            'loc': 'us_ca_sf',
            'otype': 'node_warehouse',
        }    
    )
)

customer_3 = simulation.add_object(
    Customer(
        processing_min_time=0.1,
        processing_avg_time=0.3,
        processing_sd_time=0.05,
        processing_cashflow_per_unit=200,
        metadata={
            'loc': 'us_ca',
            'otype': 'node_customer',
        }
    )
)

# Create arcs between nodes
arc_0_1 = simulation.add_object(Arc(
    origin_node=supplier_0, 
    destination_node=factory_1, 
    processing_min_time=0.1, 
    processing_avg_time=0.2, 
    processing_sd_time=0.05, 
    processing_cashflow_per_unit=-10,
    metadata={
        'loc': 'oc_pa',
        'otype': 'arc_ocean',
    }
))
arc_1_2 = simulation.add_object(Arc(
    origin_node=factory_1, 
    destination_node=warehouse_2, 
    processing_min_time=0.1, 
    processing_avg_time=0.3, 
    processing_sd_time=0.1, 
    processing_cashflow_per_unit=-12,
    metadata={
        'loc': 'us_mo_ks',
        'otype': 'arc_road',
    }   
))

arc_2_3 = simulation.add_object(Arc(
    origin_node=warehouse_2,
    destination_node=customer_3,
    processing_min_time=0.2,
    processing_avg_time=0.4,
    processing_sd_time=0.1,
    processing_cashflow_per_unit=-8,
    metadata={
        'loc': 'us_ca',
        'otype': 'arc_lm',
    }
))

order = simulation.add_object(Order(
    origin_node=supplier_0,
    destination_node=customer_3,
    units=1,
    planned_path=simulation.graph.get_optimal_path(supplier_0, customer_3, 'cashflow')
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


simulation.run(max_time=10.0)

from pprint import pprint as print
print(simulation.orders[0].history)