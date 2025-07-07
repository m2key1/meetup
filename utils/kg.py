from utils.schema import KnowledgeGraph
from pyvis.network import Network

def create_networkx_graph(graph_data: KnowledgeGraph) -> Network:
    net = Network(height="800px", width="100%", notebook=True, cdn_resources='in_line', directed=True)
    
    for node in graph_data.nodes:
        net.add_node(node.id, name=node.name, type=node.type, description=node.description)

    for edge in graph_data.edges:
        net.add_edge(edge.source_id, edge.target_id, type=edge.type, description=edge.description)
        
    return net