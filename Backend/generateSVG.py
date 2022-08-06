# Setup for Prefix Tree (Trie) generation and graph visualization 
import pydot

# Function to return a new dict template
def struct():
    struct = {
        'iw': 'False'
    }
    return struct

# Make Trie out of words
# Sorted by length, then 10 shortest valid regex outputs chosen
def make_trie(words):
    tmp_s = struct()
    root = tmp_s
    words = list(words)
    words.sort(key=len)
    words = words[0:10]
    for word in words:
        for c in word:
            if c not in tmp_s:
                tmp_s[c] = struct()
            tmp_s = tmp_s[c]
        tmp_s['iw'] = 'True'
        tmp_s = root
        cur_word = []
    return root

# Code borrowed from: https://github.com/ahmednooor/trie_graph with minor modifications
counter = 0
def genTree(words):
    global counter
    rt = {'root': make_trie(words)}
    counter = 0
    def draw(parent_name, child_name):
        global counter
        counter += 1
        p_n = parent_name
        c_n = child_name
        graph.add_node(pydot.Node(p_n, label=parent_name.split('_')[0]))
        graph.add_node(pydot.Node(c_n, label=child_name.split('_')[0]))
        edge = pydot.Edge(p_n, c_n)
        graph.add_edge(edge)

    def visit(node, parent=None):
        global counter
        for k,v in node.items():
            if isinstance(v, dict):
                # We start with the root node whose parent is None
                # we don't want to graph the None node
                k = k + '_' + str(counter)
                if parent:
                    draw(parent, k)
                visit(v, k)
            else:
                # drawing the label using a distinct name
                v = v + '_' + str(counter)
                draw(parent, v)

    graph = pydot.Dot(graph_type='digraph')
    visit(rt)
    # plt = graph.create_svg()
    # print(plt)
    return graph