from pyvis.network import Network
import streamlit.components.v1 as components


def generate_graph(records):

    net = Network(height="600px", width="100%", directed=True)

    added_nodes = set()

    for record in records:

        for key, value in record.items():

            if isinstance(value, str):

                if value not in added_nodes:
                    net.add_node(value, label=value)
                    added_nodes.add(value)

    values = []

    for record in records:
        for _, value in record.items():
            values.append(value)

    if len(values) >= 2:
        for i in range(len(values) - 1):
            if isinstance(values[i], str) and isinstance(values[i + 1], str):
                net.add_edge(values[i], values[i + 1])

    net.save_graph("graph.html")

    with open("graph.html", "r", encoding="utf-8") as file:
        html = file.read()

    components.html(html, height=650)
