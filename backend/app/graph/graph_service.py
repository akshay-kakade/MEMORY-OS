import networkx as nx
import io
import base64

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
except Exception:
    plt = None

class GraphService:
    def __init__(self):
        self.G = nx.Graph()

    def add_memory_node(self, memory_id: int, content: str, category: str):
        self.G.add_node(memory_id, content=content, category=category)

    def add_relationship(self, source_id: int, target_id: int, relation_type: str):
        self.G.add_edge(source_id, target_id, relation=relation_type)

    def get_graph_data(self):
        # This could return data suitable for a frontend graph library
        return nx.node_link_data(self.G)

    def visualize_graph(self):
        if plt is None:
            raise RuntimeError(
                'matplotlib is required for graph visualization. Install it with `pip install matplotlib`.'
            )

        plt.figure(figsize=(10, 8))
        pos = nx.spring_layout(self.G)
        nx.draw(self.G, pos, with_labels=True, node_color='skyblue', node_size=1500, edge_color='gray', font_size=10)
        
        labels = nx.get_edge_attributes(self.G, 'relation')
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels=labels)
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        img_str = base64.b64encode(buf.read()).decode('utf-8')
        plt.close()
        return img_str

graph_service = GraphService()
