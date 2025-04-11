from pyvis.network import Network
import streamlit.components.v1 as components
from graph_queries import get_graph_insights

def draw_graph(data):
    net = Network(height="600px", width="100%")
    for item in data:
        net.add_node(item["symptom"], color="red")
        net.add_node(item["condition"], color="blue")
        net.add_node(item["medicine"], color="green")
        net.add_edge(item["symptom"], item["condition"])
        net.add_edge(item["condition"], item["medicine"])
    net.save_graph("graph.html")
    components.html(open("graph.html").read(), height=600)
