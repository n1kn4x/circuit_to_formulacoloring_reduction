import networkx as nx
import matplotlib.pyplot as plt

class DFA:
    def __init__(self, states=set(), alphabet=set({'0','1'}), start_state=None, accept_states=set()):
        self.states = set(states)
        self.alphabet = set(alphabet)
        self.start_state = start_state
        self.accept_states = set(accept_states)
        self.current_state = start_state
        self.transitions = {}
        assert self.start_state is None or self.start_state in self.states
        assert self.accept_states.issubset(self.states)

    def add_transition(self, from_state, to_state, input_symbol):
        self.states.add(from_state)
        self.states.add(to_state)
        self.transitions[(from_state, input_symbol)] = to_state

    def add_transition_any_symbol(self, from_state, to_state):
        for symbol in self.alphabet:
            self.add_transition(from_state, to_state, symbol)
    
    def add_accept_state(self, accept_state):
        self.states.add(accept_state)
        self.accept_states.add(accept_state)
    
    def set_start_state(self, start_state):
        self.states.add(start_state)
        self.start_state = start_state

    def evaluate(self, input_string):
        self.current_state = self.start_state
        for i in input_string:
            self.current_state = self.transitions[(self.current_state, i)]
        return self.current_state in self.accept_states

def plot_dfa(dfa):
    # Create the directed graph
    G = nx.DiGraph()

    # Add the nodes
    for state in dfa.states:
        if (state == dfa.start_state):
            G.add_node(state, Type='START')
        elif (state in dfa.accept_states):
            G.add_node(state, Type='ACCEPT')
        else:
            G.add_node(state, Type='NORMAL')

    # Add the edges
    for transition, to_state in dfa.transitions.items():
        from_state, input_symbol = transition
        G.add_edge(from_state, to_state, label=input_symbol)

    # extract nodes with specific setting of the attribute
    start_nodes = [n for (n,ty) in \
        nx.get_node_attributes(G,'Type').items() if ty == 'START']
    accept_nodes = [n for (n,ty) in \
        nx.get_node_attributes(G,'Type').items() if ty == 'ACCEPT']
    normal_nodes = [n for (n,ty) in \
        nx.get_node_attributes(G,'Type').items() if ty == 'NORMAL']

    # Draw the graph
    pos = nx.drawing.nx_agraph.graphviz_layout(G, prog='dot')
    nx.draw_networkx_edges(G, pos=pos)
    nx.draw_networkx_nodes(G, pos, nodelist=start_nodes,
        node_color='orange', node_shape='o', edgecolors='black', node_size=1000)
    nx.draw_networkx_nodes(G, pos, nodelist=accept_nodes,
        node_color='green', node_shape='o', edgecolors='black', node_size=1000)
    nx.draw_networkx_nodes(G, pos, nodelist=normal_nodes,
        node_color='grey', node_shape='o', edgecolors='black', node_size=1000)
    nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=nx.get_edge_attributes(G, 'label'))
    nx.draw_networkx_labels(G, pos)
    plt.show()
