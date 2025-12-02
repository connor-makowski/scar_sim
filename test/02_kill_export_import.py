from scar_sim.entity import Facility, Arc, Node
from scar_sim.order import Order
from scar_sim.simulation import Simulation


simulation = Simulation()

# Create nodes
supplier_0 = simulation.add_object(
    Facility(
        processing_min_time=0.8,
        processing_avg_time=1.0,
        processing_sd_time=0.02,
        processing_cashflow_per_unit=-50,
        metadata={
            "loc": "cn_ningbo",
            "otype": "node_supplier",
        },
    )
)
factory_1 = simulation.add_object(
    Facility(
        processing_min_time=0.2,
        processing_avg_time=0.4,
        processing_sd_time=0.1,
        processing_cashflow_per_unit=-15,
        metadata={
            "loc": "us_ks_kc",
            "otype": "node_factory",
        },
    )
)

# Create arcs between nodes
arc_0_1 = simulation.add_object(
    Arc(
        origin_node=supplier_0,
        destination_node=factory_1,
        processing_min_time=2.0,
        processing_avg_time=2.0,
        processing_sd_time=0.05,
        processing_cashflow_per_unit=-10,
        metadata={
            "loc": "oc_pa",
            "otype": "arc_ocean",
        },
    )
)

order = simulation.add_object(
    Order(
        origin_node=supplier_0,
        destination_node=factory_1,
        units=1,
        planned_path=simulation.graph.get_optimal_path(
            supplier_0, factory_1, "cashflow"
        ),
    )
)

simulation.add_event(
    time_delta=0.0,
    func=order.start,
)

simulation.run(max_time=2.0)

exported_bytes = simulation.export_state()
exported_file = simulation.export_state(filename="test_simulation_state.dill")

imported_bytes_sim = Simulation.import_state(data=exported_bytes)
imported_bytes_sim.run(max_time=10.0)

imported_file_sim = Simulation.import_state(filename=exported_file)
imported_file_sim.run(max_time=10.0)

# print("Original Simulation Order History:", simulation.orders[0].history)

passing = True
err_msg = ""
if simulation.orders[0].history[-1]["time"] > 2.0:
    passing = False
    err_msg = "Simulation.run max_time did not stop the simulation as expected."
if imported_bytes_sim.orders[0].history[-1]["status"] != "completed":
    passing = False
    err_msg = "Imported bytes simulation did not complete the order."
if imported_file_sim.orders[0].history[-1]["status"] != "completed":
    passing = False
    err_msg = "Imported file simulation did not complete the order."

import os

os.remove(exported_file)

print("02: Export/Import Test Passed:", passing)
if not passing:
    print("    -", err_msg)
