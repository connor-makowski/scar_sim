from scar.entity import Node, Arc
from scar.utils import IDGenerator
from scgraph import Graph as SCGraph
from typing import Literal

get_arc_id = IDGenerator()

class Graph:
    def __init__(self):
        self.time_graph = []
        self.cashflow_graph = []
        self.arc_obj_graph = []

    def update_graphs(self, obj: Arc | Node):
        if isinstance(obj, Arc):
            self.time_graph[obj.origin_node.outbound_id][obj.destination_node.id] = float(obj.processing_time_avg)
            self.cashflow_graph[obj.origin_node.outbound_id][obj.destination_node.id] = -float(obj.processing_cashflow_per_unit)
            self.arc_obj_graph[obj.origin_node.outbound_id][obj.destination_node.id] = obj
        elif isinstance(obj, Node):
            self.time_graph[obj.id] = {obj.outbound_id: float(obj.processing_time_avg)}
            self.cashflow_graph[obj.id] = {obj.outbound_id: float(obj.processing_cashflow_per_unit)}

    def add_object(self, obj: Node | Arc):
        if isinstance(obj, Arc):
            obj.id = get_arc_id()
            if obj.origin_node.id is None or obj.destination_node.id is None:
                raise ValueError("Both origin and destination nodes must be added to the graph before adding the arc")
        elif isinstance(obj, Node):
            obj.id = len(self.time_graph)
            obj.outbound_id = obj.id + 1
            self.time_graph += [dict(), dict()]
            self.cashflow_graph += [dict(), dict()]
            self.arc_obj_graph += [dict(), dict()]
        self.update_graphs(obj)
        return obj
    
    def get_path_weight(self, path: list[int], graph:Literal['cashflow', 'time']) -> float:
        graph_obj = self.cashflow_graph if graph == 'cashflow' else self.time_graph
        weight_sum = 0.0
        for i in range(len(path) - 1):
            origin = path[i]
            destination = path[i + 1]
            weight_sum += graph_obj[origin][destination]
        return weight_sum if graph == 'time' else -weight_sum
    
    def get_optimal_path(self, origin_node: Node, destination_node: Node, graph:Literal['cashflow', 'time']) -> dict:
        graph_obj = self.cashflow_graph if graph == 'cashflow' else self.time_graph
        return SCGraph.dijkstra_makowski(
            graph_obj,
            origin_node.id,
            destination_node.id
        )['path']
    
    def get_route_options(self, origin_node: Node, destination_node: Node) -> list[Arc]:
        min_time_path = self.get_optimal_path(origin_node, destination_node, 'time')
        min_cashflow_path = self.get_optimal_path(origin_node, destination_node, 'cashflow')
        return {
            "min_cashflow":{
                'path': min_cashflow_path,
                'time': self.get_path_weight(min_cashflow_path, 'time'),
                'cashflow': self.get_path_weight(min_cashflow_path, 'cashflow')
            },
            "min_time":{
                'path': min_time_path,
                'time': self.get_path_weight(min_time_path, 'time'),
                'cashflow': self.get_path_weight(min_time_path, 'cashflow')
            }
        }