from graphviz import Digraph

class Tape:
    def __init__(self, values=None, blank_symbol='0'):
        self.blank_symbol = blank_symbol
        if values is not None:
            self.values = {i: v for i, v in enumerate(values)}
        else:
            self.values = {}
        self.cursor = 0

    def move_left(self):
        self.cursor -= 1

    def move_right(self):
        self.cursor += 1

    def read(self):
        if self.cursor in self.values:
            return self.values[self.cursor]
        else:
            return self.blank_symbol

    def write(self, value):
        self.values[self.cursor] = value

class TuringMachine:
    LEFT = 'L'
    RIGHT = 'R'
    NEUTRAL = 'N'

    def __init__(self, alphabet=set(['0','1']), blank_symbol='0'):
        self.states = set()
        self.alphabet = alphabet
        self.transitions = {}
        self.initial_state = None
        self.accept_states = set()
        self.reject_states = set()
        self.blank_symbol = blank_symbol
        assert self.blank_symbol in self.alphabet

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
        tape = Tape(tape, blank_symbol=self.blank_symbol)

        while True:
            # Check if the current state is an accept or reject state
            if current_state in self.accept_states:
                return True
            if current_state in self.reject_states:
                return False

            # Get the transition for the current state and tape value
            try:
                transition = self.transitions[(current_state, tape.read())]
            except KeyError:
                raise KeyError("No transition defined for the current state. Returning False.")
                return False

            # Update the current state, tape value, and cursor position
            current_state = transition[0]
            tape.write(transition[1])
            if transition[2] == self.LEFT:
                tape.move_left()
            if transition[2] == self.RIGHT:
                tape.move_right()

    def get_num_L_and_N_transitions(self):
        return len([t for t in self.transitions.values() if (t[2] == 'L' or t[2] == 'N')])

    def draw_transition_diagram(self):
        # Create a new graph
        graph = Digraph()

        # Add states to the graph
        for state in self.states:
            if state in self.accept_states:
                shape = 'doublecircle'
            elif state in self.reject_states:
                shape = 'circle'
            else:
                shape = 'circle'
            graph.node(state, shape=shape)

        # Add transitions to the graph
        for (from_state, read_value), (to_state, write_value, direction) in self.transitions.items():
            label = f'{read_value}/{write_value}, {direction}'
            graph.edge(from_state, to_state, label=label)

        # Render and return the graph
        return graph.render("out/turingmachine")

    def step_through_computation(self, tape):
        # Set the initial state and tape
        current_state = self.initial_state
        tape = Tape(tape, blank_symbol=self.blank_symbol)

        while True:
            # Print the current state, tape value, and cursor position
            print(f'State: {current_state}')
            print(f'Tape: {tape.values}')
            print(f'Cursor: {tape.cursor}')
            print()

            # Check if the current state is an accept or reject state
            if current_state in self.accept_states:
                print('Accepted!')
                return True
            if current_state in self.reject_states:
                print('Rejected!')
                return False

            # Get the transition for the current state and tape value
            try:
                transition = self.transitions[(current_state, tape.read())]
            except KeyError:
                print("No transition defined for the current state. Returning False.")
                return False

            # Update the current state, tape value, and cursor position
            current_state = transition[0]
            tape.write(transition[1])
            if transition[2] == self.LEFT:
                tape.move_left()
            if transition[2] == self.RIGHT:
                tape.move_right()
