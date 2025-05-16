import networkx as nx 

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
# Sequence
# --------------------------------------
# Lucas number
# L_1 = 2, L_2 = 1, L_n = L_{n-1} + L_{n-2} (n >= 3)
def Lucas_number(n):
    if n == 0:
        return 2
    elif n == 1:
        return 1
    else:
        return Lucas_number(n - 1) + Lucas_number(n - 2)

# Fibonacci number
# F_1 = 1, F_2 = 1, F_n = F_{n-1} + F_{n-2} (n >= 3)
def Fibonacci_number(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return Fibonacci_number(n - 1) + Fibonacci_number(n - 2)
    
# Padovan number
# P_1 = 1, P_2 = 1, P_3 = 1, P_n = P_{n-2} + P_{n-3} (n >= 4)
def Padovan_number(n):
    if n == 1:
        return 1
    elif n == 2:
        return 1
    elif n == 3:
        return 1
    else:
        return Padovan_number(n - 2) + Padovan_number(n - 3)

# Perrin number
# Q_1 = 0, Q_2 = 2, Q_3 = 3, Q_n = Q_{n-2} + Q_{n-3} (n >= 4)
def Perrin_number(n):
    if n == 1:
        return 0
    elif n == 2:
        return 2
    elif n == 3:
        return 3
    else:
        return Perrin_number(n - 2) + Perrin_number(n - 3)



# --------------------------------------
# Counting algorithms
# --------------------------------------
# count the number |\mathcal{A}(N)| of support network in N by equation (4) in Theorem 8
def count_all_support_networks(network):
    trails = maximal_zigzag_trail_decomposition(network)
    count = 1
    for trail in trails:
        if type_of_zigzag_trail(trail) == "crown":
            count = count * Lucas_number(len(trail))
        else:
            count = count * Fibonacci_number(len(trail))

    return count

# count the number |\mathcal{B}(N)| of minimal support network in N by equation (6) in Theorem 10
def count_minimal_support_networks(network):
    trails = maximal_zigzag_trail_decomposition(network)
    count = 1
    for trail in trails:
        if type_of_zigzag_trail(trail) == "crown":
            count *= Perrin_number(len(trail))
        else:
            count *= Padovan_number(len(trail))
    return count

# count the number |\mathcal{C}(N)| of minimum support network in N in Theorem 12
def count_minimum_support_networks(network):
    trails = maximal_zigzag_trail_decomposition(network)
    count = 1
    for trail in trails:
        type = type_of_zigzag_trail(trail)
        if type == "crown":
            count *= 2
        elif type == "N-fence":
            count *= 1 
        else:  # type == "W-fence" or type == "M-fence":
            count *= len(trail) // 2
    return count



# Input
filename = input("File Name: ")

edges = read_edges_from_file(filename + ".txt")
network = nx.DiGraph(edges)

print(f"The number |A_N| of support networks: {count_all_support_networks(network)}")
print(f"The number |B_N| of support networks: {count_minimal_support_networks(network)}")
print(f"The number |C_N| of support networks: {count_minimum_support_networks(network)}")



