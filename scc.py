class Graph:
    def __init__(self):
        self.nodes = {}
        self.edges = {}
        self.parents = {}
        self.edge_list = []
    def add_node(self, node, data=None):
        self.nodes[node] = data

    def add_edge(self, parent, child, data=None):
        if parent not in self.edges:
            self.edges[parent] = {}
        self.edges[parent][child] = data 
        if child not in self.parents:
            self.parents[child] = []
        self.parents[child].append(parent)
        self.edge_list.append((parent, child))

    def add_undirected_edge(self, node1, node2, data=None):
        self.add_edge(node1, node2, data)
        self.add_edge(node2, node1, data)

    def get_node_data(self, node):
        return self.nodes[node]
    
    def get_edge_data(self, parent, child):
        return self.edges[parent][child]

    def get_children(self, parent):
        if parent not in self.edges:
            return []
        return self.edges[parent].keys()

    def get_parents(self, node):
        if node not in self.parents:
            return []
        return self.parents[node]

    def contains_node(self, node):
        if node in self.nodes:
            return True
        else:
            return False

    def contains_edge(self, parent, child):
        if parent in self.edges:
            if child in self.edges[parent]:
                return True
        return False

    def get_nodes(self):
        return self.nodes.keys()

    def get_edges(self):
        return self.edge_list


# Part 1: Reverse the graph
def reverse_graph(g: Graph):
    newGraph = Graph()
    for node in g.get_nodes():
        newGraph.add_node(node, g.get_node_data(node))
        for child in g.get_children(node):
            newGraph.add_node(child, g.get_node_data(child))
            newGraph.add_edge(child, node, g.get_edge_data(node, child))
    return newGraph

# Part 2: DFS Finish Order
def dfs_finish_order(g: Graph):
    visited = set()
    finish_order = []
    for node in g.get_nodes():
        if node not in visited:
            def dfs_recursive(node):
                visited.add(node)
                for child in g.get_children(node):
                    if child not in visited:
                        dfs_recursive(child)
                finish_order.append(node)
            dfs_recursive(node)
    return finish_order

# Part 3: Kosaraju's Algorithm
def kosarajus(g: Graph):
    postorder_reversed = dfs_finish_order(g)[::-1] # reversed
    reversed_edge_directions = reverse_graph(g)
    
    visited = set()
    groups = []
    for node in postorder_reversed:
        
        if node not in visited:
            current_group = []
            def dfs_recursive(node):
                visited.add(node)
                for child in reversed_edge_directions.get_children(node):
                    if child not in visited:
                        dfs_recursive(child)
                current_group.append(node)
            dfs_recursive(node)
            groups.append(current_group)

    g_prime = Graph()

    node_to_group = {}
    for group in groups:
        current_added_frozen_group = frozenset(group)
        g_prime.add_node(current_added_frozen_group)
        for node in group:
            node_to_group[node] = current_added_frozen_group

    for parent, child in g.get_edges():
        parent_group = node_to_group[parent]
        child_group = node_to_group[child]

        if parent_group != child_group and not g_prime.contains_edge(parent_group, child_group):
            g_prime.add_edge(parent_group, child_group)

    return g_prime



####=====================================================================================================
####========================================== TESTS ====================================================
####=====================================================================================================

def build_graph(nodes, edges):
    g = Graph()
    for node in nodes:
        g.add_node(node)
    for parent, child in edges:
        g.add_edge(parent, child)
    return g

# Part 1 tests
def test_reverse_graph():
    # every edge flips direction
    g = build_graph("ABC", [("A", "B"), ("B", "C")])
    r = reverse_graph(g)
    assert r.contains_edge("B", "A")
    assert r.contains_edge("C", "B")
    assert not r.contains_edge("A", "B")
    assert not r.contains_edge("B", "C")
    assert len(r.get_edges()) == 2

    # nodes with no edges are kept
    g = build_graph("ABZ", [("A", "B")])
    r = reverse_graph(g)
    assert set(r.get_nodes()) == {"A", "B", "Z"}

    # a cycle reversed is still a cycle, just the other way
    g = build_graph("ABC", [("A", "B"), ("B", "C"), ("C", "A")])
    r = reverse_graph(g)
    assert r.contains_edge("B", "A")
    assert r.contains_edge("C", "B")
    assert r.contains_edge("A", "C")

    # edge data comes along
    g = Graph()
    g.add_node("A")
    g.add_node("B")
    g.add_edge("A", "B", 5)
    r = reverse_graph(g)
    assert r.get_edge_data("B", "A") == 5

    # original graph is not changed
    g = build_graph("AB", [("A", "B")])
    reverse_graph(g)
    assert g.contains_edge("A", "B")
    assert not g.contains_edge("B", "A")
    print("Part 1 tests passed")

# Part 2 tests
def test_dfs_finish_order():
    # a chain finishes from the end back to the start
    g = build_graph("ABC", [("A", "B"), ("B", "C")])
    assert dfs_finish_order(g) == ["C", "B", "A"]

    # every node shows up exactly once, even with cycles
    g = build_graph("ABCD", [("A", "B"), ("B", "A"), ("B", "C"), ("C", "D"), ("D", "C")])
    order = dfs_finish_order(g)
    assert sorted(order) == ["A", "B", "C", "D"]

    # disconnected nodes are still included
    g = build_graph("ABXY", [("A", "B"), ("X", "Y")])
    order = dfs_finish_order(g)
    assert sorted(order) == ["A", "B", "X", "Y"]

    # in a DAG, a parent always finishes after its children
    g = build_graph("ABCDE", [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D"), ("D", "E")])
    order = dfs_finish_order(g)
    for parent, child in g.get_edges():
        assert order.index(parent) > order.index(child)
    print("Part 2 tests passed")

# Part 3 tests
def check_topological(g_prime):
    order = list(g_prime.get_nodes())
    for parent, child in g_prime.get_edges():
        assert order.index(parent) < order.index(child)

def test_kosarajus():
    # two cycles joined by one edge
    g = build_graph("ABCD", [("A", "B"), ("B", "A"), ("B", "C"), ("C", "D"), ("D", "C")])
    g_prime = kosarajus(g)
    ab = frozenset("AB")
    cd = frozenset("CD")
    assert set(g_prime.get_nodes()) == {ab, cd}
    assert g_prime.contains_edge(ab, cd)
    assert not g_prime.contains_edge(cd, ab)
    assert len(g_prime.get_edges()) == 1
    check_topological(g_prime)

    # bigger graph, with several edges between the same two SCCs
    g = build_graph("ABCDEFG", [("A", "B"), ("B", "C"), ("C", "A"), ("C", "D"), ("D", "E"),
                                ("E", "D"), ("E", "F"), ("G", "F"), ("A", "D"), ("B", "E")])
    g_prime = kosarajus(g)
    abc = frozenset("ABC")
    de = frozenset("DE")
    f = frozenset("F")
    gg = frozenset("G")
    assert set(g_prime.get_nodes()) == {abc, de, f, gg}
    assert g_prime.contains_edge(abc, de)
    assert g_prime.contains_edge(de, f)
    assert g_prime.contains_edge(gg, f)
    assert len(g_prime.get_edges()) == 3  # no duplicate abc -> de edges
    check_topological(g_prime)

    # a DAG: every node is its own SCC
    g = build_graph("ABCD", [("A", "B"), ("B", "C"), ("A", "D")])
    g_prime = kosarajus(g)
    assert set(g_prime.get_nodes()) == {frozenset(n) for n in "ABCD"}
    assert len(g_prime.get_edges()) == 3
    check_topological(g_prime)

    # one big cycle collapses into one node
    g = build_graph("ABCD", [("A", "B"), ("B", "C"), ("C", "D"), ("D", "A")])
    g_prime = kosarajus(g)
    assert list(g_prime.get_nodes()) == [frozenset("ABCD")]
    assert len(g_prime.get_edges()) == 0

    # no edges: every node is alone
    g = build_graph("XYZ", [])
    g_prime = kosarajus(g)
    assert set(g_prime.get_nodes()) == {frozenset("X"), frozenset("Y"), frozenset("Z")}
    assert len(g_prime.get_edges()) == 0

    # every node id is a frozenset
    for node in g_prime.get_nodes():
        assert isinstance(node, frozenset)
    print("Part 3 tests passed")

if __name__ == "__main__":
    test_reverse_graph()
    test_dfs_finish_order()
    test_kosarajus()
    print("All tests passed")






