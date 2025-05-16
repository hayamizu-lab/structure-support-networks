import networkx as nx 
import itertools
import time
from graphviz import Digraph

# ======================================
# Input
# ======================================
# input network from file
def read_edges_from_file(file_path):
    edges = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            tokens = line.split()
            if len(tokens) >= 2:
                source, target = tokens[0], tokens[1]
                edges.append((source, target))
            else:
                print(f"Warning: Invalid line: {line}")
    return edges


# ======================================
# Output
# ======================================
# draw
def draw_subnetwork(network, subnetwork, filename="network"):
    dot = Digraph()
    for u, v in network.edges():
        if (u, v) in subnetwork.edges():
            dot.edge(u, v)
        else:
            dot.edge(u, v, color="gray", style="dashed")
    dot.render(filename, format="pdf", cleanup=True)



# ======================================
# Maximal zig-zag trail decomposition and categorization
# ======================================
# Maximal zig-zag trail decomposition (Algorithm 5.1 in Hayamizu (2021))
def maximal_zigzag_trail_decomposition(network):
    # input edges from network 
    edges = list(network.edges())

    # initialize
    trails = []  # list of zig-zag trails
    edges_remaining = set(edges)

    while edges_remaining:
        # extract any edge s 
        e = edges_remaining.pop()
        # a zig-zag trail Z starts with [e]
        Z = [e]
        # Extend until there are no more edges that can be added to Z
        extended = True
        while extended:
            extended = False
            head_edge = Z[0] 
            tail_edge = Z[-1] 
            # search an edge that can be connected to Z
            for f in list(edges_remaining):
                # check whether the head or tail are shared
                if (f[0] == head_edge[0]) or (f[1] == head_edge[1]):
                    Z.insert(0, f)
                    edges_remaining.remove(f)
                    extended = True
                    break
                elif (f[0] == tail_edge[0]) or (f[1] == tail_edge[1]):
                    Z.append(f)
                    edges_remaining.remove(f)
                    extended = True
                    break
        # add maximal zig-zag trail Z to trails
        trails.append(Z)
    return trails

# categorize the maximal zig-zag trail to M-fence, N-fence, W-fence and crown
def type_of_zigzag_trail(trail):

    if len(trail) % 2 == 1:
        return "N-fence"
    else:
        if len(trail) >= 4 and (
            (trail[0][0] == trail[-1][0]) or (trail[0][1] == trail[-1][1])
        ):
            return "crown"
        elif trail[0][0] == trail[1][0]:
            return "M-fence"
        else:
            return "W-fence"

# --------------------------------------
# Generator of (B, C)-admissible subset
# --------------------------------------
# generate the family S_B(Z_i) of B-admissible subsets of E(Z_i), where Z_i is a fence (equation (5))
def generate_family_of_B_admissible_fence(trail):
    n = len(trail)
    sequences = []
    edgesets = []

    def backtrack(seq):
        if len(seq) == n:
            if seq[-1] == 1:
                sequences.append(seq.copy())
            return
        if len(seq) == n - 1:
            if len(seq) >= 2 and seq[-2] == 1 and seq[-1] == 1:
                return
            seq.append(1)
            sequences.append(seq.copy())
            seq.pop()
            return
        if seq[-1] != 0:
            seq.append(0)
            backtrack(seq)
            seq.pop()
        if len(seq) < 2 or not (seq[-2] == 1 and seq[-1] == 1):
            seq.append(1)
            backtrack(seq)
            seq.pop()
    backtrack([1])
    
    for p in sequences:
        edgeset = []
        for i in range(len(trail)):
            if p[i] == 1:
                edgeset.append(trail[i])
        edgesets.append(edgeset)

    return edgesets


# generate the family S_B(Z_i) of B-admissible subsets of E(Z_i), where Z_i is a crown (equation (5))
def generate_family_of_B_admissible_crown(trail):
    n = len(trail)
    sequences = []
    edgesets = []

    def backtrack(seq):
        if len(seq) == n:
            valid = True
            for i in range(n):
                if seq[i] == 0 and seq[(i + 1) % n] == 0:
                    valid = False
                    break
                if seq[i] == 1 and seq[(i + 1) % n] == 1 and seq[(i + 2) % n] == 1:
                    valid = False
                    break
            if valid:
                sequences.append(seq.copy())
            return
        for bit in [0, 1]:
            if seq:
                if seq[-1] == 0 and bit == 0:
                    continue
            if len(seq) >= 2:
                if seq[-2] == 1 and seq[-1] == 1 and bit == 1:
                    continue
            seq.append(bit)
            backtrack(seq)
            seq.pop()
    backtrack([])
    for p in sequences:
        edgeset = []
        for i in range(len(trail)):
            if p[i] == 1:
                edgeset.append(trail[i])
        edgesets.append(edgeset)


    return edgesets


# generate the family S_C(Z_i) of C-admissible subsets of E(Z_i) (equation (7))
def generate_family_of_C_admissible(trail):
    edgesets = []
    sequences = []
    type = type_of_zigzag_trail(trail)
    if type == "M-fence" or type == "W-fence":
        for p in range(0, int((len(trail)) / 2)):
            sequence = []
            q = int((len(trail) - 2) / 2) - p
            sequence.append(1)
            for j in range(p):
                sequence.append(0)
                sequence.append(1)
            for j in range(q):
                sequence.append(1)
                sequence.append(0)
            sequence.append(1)
            sequences.append(sequence)
    elif type == "N-fence":
        sequence = []
        for i in range(int(len(trail) / 2)):
            sequence.append(1)
            sequence.append(0)
        sequence.append(1)
        sequences.append(sequence)
    else:  # type == "crown"
        sequence = []
        for i in range(int(len(trail) / 2) + 1):
            sequence.append(1)
            sequence.append(0)
        sequences.append(sequence)
        sequence = []
        for i in range(int(len(trail) / 2) + 1):
            sequence.append(0)
            sequence.append(1)
        sequences.append(sequence)

    for p in sequences:
        edgeset = []
        for i in range(len(trail)):
            if p[i] == 1:
                edgeset.append(trail[i])
        edgesets.append(edgeset)

    return edgesets


# --------------------------------------
# Enumeration Algorithms for minimal and minimum support networks
# --------------------------------------
# enumerate minimal support networks 
def enumerate_all_minimal_support_networks(network):
    support_networks = []
    edge_sets_in_trail = []
    trails = maximal_zigzag_trail_decomposition(network)
    for trail in trails:
        if type_of_zigzag_trail(trail) == "crown":
            edge_sets = generate_family_of_B_admissible_crown(trail)
            edge_sets_in_trail.append(edge_sets)
        else: # "fence"
            edge_sets = generate_family_of_B_admissible_fence(trail)
            edge_sets_in_trail.append(edge_sets)

    # calculate the direct-product
    all_combinations = list(itertools.product(*edge_sets_in_trail))
    
    for combination in all_combinations:
        support_network = nx.DiGraph()
        for combo in combination:
            support_network.add_edges_from(combo)
        support_networks.append(support_network)
    return support_networks


# enumerate minimum support networks 
def enumerate_all_minimum_support_networks(network):
    support_networks = []
    trails = maximal_zigzag_trail_decomposition(network)
    edge_sets_in_trail = []
    for trail in trails:
        edge_sets = generate_family_of_C_admissible(trail)
        edge_sets_in_trail.append(edge_sets)

    # calculate the direct-product
    all_combinations = list(itertools.product(*edge_sets_in_trail))
    
    for combination in all_combinations:
        support_network = nx.DiGraph()
        for combo in combination:
            support_network.add_edges_from(combo)
        support_networks.append(support_network)
    return support_networks


# --------------------------------------
# level of the network
# --------------------------------------
# calculate the level of input network
def network_level(network):
    undirected = network.to_undirected()

    # decompose into biconnected components
    bcc = nx.biconnected_components(undirected)

    # calculate the number of reticulation for each biconnected component and take the maximum
    max_reticulations = 0
    for comp in bcc:
        reticulation_count = sum(1 for node in comp if network.in_degree(node) > 1)
        max_reticulations = max(max_reticulations, reticulation_count)

    return max_reticulations

# calculate the minimum level of input network set
def minimum_level(networks):
    level = network_level(networks[0])
    min_level_network = networks[0]

    for subnetwork in networks:
        if network_level(subnetwork) < level:
            level = network_level(subnetwork)
            min_level_network = subnetwork

    return level, min_level_network


# --------------------------------------
# Experiment algorithm
# --------------------------------------
# exact algorithm for solving LEVEL MINIMIZATION (Algorithm 1)
def exact_algorithm_min_lev(network):
    # enumerate the family of minimal support networks B_N
    support_networks = enumerate_all_minimal_support_networks(network)
    
    return minimum_level(support_networks)




################################ MAIN ################################
# Input
filename = input("File Name: ")

# input network
edges = read_edges_from_file(filename + ".txt")
network = nx.DiGraph(edges)

# measure runtime
start_time = time.perf_counter()
exact_min_lev, min_lev_network = exact_algorithm_min_lev(network)
end_time = time.perf_counter()
runtime = end_time - start_time

# output
print(f"Input: {filename}.txt")
print(f"Minimum level:{exact_min_lev}")
print(f"Runtime (sec):{runtime}")
draw_subnetwork(network, min_lev_network, filename + "-exact")