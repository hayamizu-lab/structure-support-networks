import random
import networkx as nx

# generate random tree with n leaves
def generate_random_tree(n):
    G = nx.DiGraph()
    # start with 2 leaves
    G.add_edges_from([(0, 1), (0, 2)])
    num_leaves = 2
    max_idx = 2
    leaf_set = [1, 2]

    while num_leaves < n:
        # select one leaf
        leaf = random.choice(leaf_set)
        # add two leaves below the selected leaf
        G.add_edges_from([(leaf, max_idx + 1), (leaf, max_idx + 2)])
        
        leaf_set.remove(leaf)
        leaf_set.append(max_idx + 1)
        leaf_set.append(max_idx + 2)
        num_leaves = num_leaves + 1
        max_idx = max_idx + 2
    return G

# generate random network with n leaves, r reticulations
def generate_random_network(n, r):
    # start with tree with n leaves
    network = generate_random_tree(n)

    for i in range(r):
        # select distinct edges e1, e2 s.t. head(e1) is not a descendant of head(e2)
        while True:
            e1, e2 = random.sample(list(network.edges), 2)
            t1, h1 = e1
            t2, h2 = e2
            if not nx.has_path(network, h2, h1):
                break
        
        # subdivide e1 and e2 with new1 and new2, resp., and add edge (new1, new2)
        new1, new2 = max(network.nodes()) + 1, max(network.nodes()) + 2
        network.remove_edge(t1, h1)
        network.remove_edge(t2, h2)
        network.add_edges_from(
            [
                (t1, new1),
                (new1, h1),
                (t2, new2),
                (new2, h2),
                (new1, new2),
            ]
        )

    return network



# Input
input_str = input("Filename n r k: ")
inputs = input_str.split()
filename = inputs[0]
n = int(inputs[1])
r = float(inputs[2])
k = int(inputs[3])

for i in range(k):
    N = generate_random_network(n, r)
    with open(filename + f"_{i}.txt", "w") as f:            
        for u, v in N.edges:
            f.write(f"{u} {v}\n")
