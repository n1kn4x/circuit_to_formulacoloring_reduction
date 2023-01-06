class DFA:
    def __init__(self, states, alphabet, start_state, accept_states, name):
        self.states = states
        self.alphabet = alphabet
        self.start_state = start_state
        self.accept_states = accept_states
        self.current_state = start_state
        self.transitions = {}

    def add_transition(self, from_state, to_state, input_symbol):
        self.transitions[(from_state, input_symbol)] = to_state

    def add_transition_any_symbol(self, from_state, to_state):
        for symbol in self.alphabet:
            self.add_transition(from_state, to_state, symbol)

    def evaluate(self, input_string):
        self.current_state = self.start_state
        for i in input_string:
            self.current_state = self.transitions[(self.current_state, i)]
        return self.current_state in self.accept_states
