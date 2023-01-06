class DFA:
    def __init__(self, states, alphabet, start_state, accept_states, name):
        self.states = states
        self.alphabet = alphabet
        self.start_state = start_state
        self.accept_states = accept_states
        self.current_state = start_state
        self.transitions = {}

    def add_transition(self, from_state, input_symbol, to_state):
        self.transitions[(from_state, input_symbol)] = to_state

    def evaluate(self, input_string):
        self.current_state = self.start_state
        for i in input_string:
            self.current_state = self.transitions[(self.current_state, i)]
        return self.current_state in self.accept_states
