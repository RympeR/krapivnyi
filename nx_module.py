import networkx as nx
import matplotlib.pyplot as plt

G=nx.DiGraph()
R=[('S0','S1'),('S1','S2'),('S1','S7'),('S0','S7')] 

G.add_edges_from(R)

# Calculate layout and get all positions
pos = nx.circular_layout(G)

# Draw everything
nx.draw_networkx_nodes(G, pos)
nx.draw_networkx_edges(G, pos)
nx.draw_networkx_labels(G, pos)
nx.draw_networkx_edge_labels(G, pos, 
    {
        ('S0', 'S1'): 'edge1',
        ('S1', 'S2'): 'edge2',
        ('S1', 'S7'): 'edge3',
        ('S0', 'S7'): 'edge4'
    }
)

plt.axis('off')
plt.savefig("path.png");
plt.show()