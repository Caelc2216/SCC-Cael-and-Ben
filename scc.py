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

def reverse_graph(g: Graph):
    newGraph = Graph()
    for node in g.get_nodes():
        newGraph.add_node(node, g.get_node_data(node))
        for child in g.get_children(node):
            newGraph.add_node(child, g.get_node_data(child))
            newGraph.add_edge(child, node, g.get_edge_data(node, child))
    return newGraph


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
            


def kosarajus(g: Graph):
    g_prime = dfs_finish_order(g).reverse()
    g_reversed = reverse_graph(g)
