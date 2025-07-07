from utils.schema import KnowledgeGraph
from pyvis.network import Network

def create_graph(graph_data: KnowledgeGraph) -> Network:
    net = Network(height="800px", width="100%", notebook=True, cdn_resources='in_line', directed=True)
    
    degrees = {}
    for edge in graph_data.edges:
        if edge.source_id in degrees:
            degrees[edge.source_id] += 1
        else:
            degrees[edge.source_id] = 1
        
        if edge.target_id in degrees:
            degrees[edge.target_id] += 1
        else:
            degrees[edge.target_id] = 1
        
    max_degree = max(degrees.values()) if degrees else 1

    color_start = (108, 216, 158)
    color_end = (243, 104, 153)
    alpha = 0.9 

    for node in graph_data.nodes:
        degree = degrees.get(node.id, 0)
        
        factor = min(degree / max_degree, 1.0)
        r = int(color_start[0] * (1 - factor) + color_end[0] * factor)
        g = int(color_start[1] * (1 - factor) + color_end[1] * factor)
        b = int(color_start[2] * (1 - factor) + color_end[2] * factor)
        node_color_bg = f'rgba({r},{g},{b},{alpha})'
        node_color_border = "#000000"

        title = f"Name: {node.name}\nType: {node.type}\nDesc: {node.description}"
        
        net.add_node(
            node.id, 
            label=node.name, 
            title=title, 
            color={
                'background': node_color_bg,
                'border': node_color_border,
                'highlight': {
                    'background': node_color_bg,
                    'border': "#000000"
                }
            },
            shape='ellipse'
        )

    for edge in graph_data.edges:
        title = f"Type: {edge.type}\nDesc: {edge.description}"
        net.add_edge(
            edge.source_id, 
            edge.target_id, 
            title=title, 
            label=edge.type
        )
    return net