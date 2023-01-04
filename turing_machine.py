class TuringMachine:
    LEFT = 'L'
    RIGHT = 'R'
    NEUTRAL = 'N'

    def __init__(self, alphabet=set(['0','1'])):
        self.states = set()
        self.alphabet = alphabet
        self.transitions = {}
        self.initial_state = None
        self.accept_states = set()
        self.reject_states = set()

    def add_transition(self, from_state, to_state, read_value, write_value, direction):
        self.states.add(from_state)
        self.states.add(to_state)
        self.alphabet.add(read_value)
        self.alphabet.add(write_value)
        self.transitions[(from_state, read_value)] = (to_state, write_value, direction)

    def add_transition_any_symbol(self, from_state, to_state, direction):
        for symbol in self.alphabet:
            self.add_transition(from_state, to_state, symbol, symbol, direction)
    
    def set_initial_state(self, state):
        self.initial_state = state

    def add_accept_state(self, state):
        self.accept_states.add(state)

    def add_reject_state(self, state):
        self.reject_states.add(state)

    def run(self, tape):
        # Set the initial state and tape
        current_state = self.initial_state
        tape = list(tape)
        cursor = 0

        while True:
            # Check if the current state is an accept or reject state
            if current_state in self.accept_states:
                return True
            if current_state in self.reject_states:
                return False

            # Get the transition for the current state and tape value
            try:
                transition = self.transitions[(current_state, tape[cursor])]
            except KeyError:
                raise KeyError("No transition defined for the current state. Returning False.")
                return False

            # Update the current state, tape value, and cursor position
            current_state, tape[cursor], direction = transition
            if direction == self.LEFT:
                cursor -= 1
            if direction == self.RIGHT:
                cursor += 1
