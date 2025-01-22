import networkx as nx
import matplotlib.pyplot as plt

# Load the edgelist from the file
filename = "../graphs/karate.edgelist"
G = nx.read_edgelist(filename, nodetype=int)  # Change `nodetype` as needed (e.g., `str` for string nodes)

# Draw the graph
plt.figure(figsize=(8, 6))
nx.draw(
    G,
    with_labels=True,
    node_color="lightblue",
    node_size=700,
    font_size=12,
    font_weight="bold",
    edge_color="gray"
)
plt.title("Graph Visualization from File")
plt.show()
