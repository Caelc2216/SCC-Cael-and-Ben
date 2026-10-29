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

def reverse_graph(g):
    pass

def dfs_finish_order(g):
    pass

def kosarajus(g):
    pass
