import random
import matplotlib.pyplot as plt
from graphviz import Digraph

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

    def draw_transition_diagram(self):
        # Create a new graph
        graph = Digraph()

        # Add states to the graph
        for state in self.states:
            if state in self.accept_states:
                shape = 'doublecircle'
            else:
                shape = 'circle'
            graph.node(state, shape=shape)

        # Add transitions to the graph
        for (from_state, input_symbol), to_state in self.transitions.items():
            label = f'{input_symbol}'
            graph.edge(from_state, to_state, label=label)

        # Render and return the graph
        return graph.render("out/dfa")

        import random

    def generate_sample(self, m, n):
        sample = []
        for i in range(m):
            # Generate a random n-bit string
            w = "".join(random.choices(["0", "1"], k=n))
            # Check if the string is accepted by the DFA
            b = self.evaluate(w)
            sample.append((w, b))
        return sample
