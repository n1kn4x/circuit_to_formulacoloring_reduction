from turing_machine import *
from dfa import *

"""
# The basic idea is to encode the work tape contents of the Turing machine as the states of the DFA,
# and to use the instance transformation G(a) to replicate the input string many times in order to simulate
# the Turing machine's ability to move its read-only input head left or right.

# Here are the detailed steps:

# 1. Create a directed graph G_T based on the description of the Turing machine T.
#    Each node of G_T is labeled with a tuple (s, sigma, i) where s is a state of the finite control of T,
#    sigma is a binary string representing the work tape contents of T, and i is an index indicating the head
#    position of T on the input tape.

# 2. Draw a directed edge, labeled with the input symbol b, from the node (s, sigma, i) to the node (s', sigma', i + 1)
#    if and only if T, when in state s with work tape contents sigma and input head position i,
#    on reading a b from the input would move the input head right and go to state s' with work tape contents sigma'.
#    Label this edge with an R to indicate a move to the right on the input.

# 3. Similarly, draw an edge from a node with input head index i to a node with input head index i - 1
#    and label it with an L to indicate a move to the left on the input. Also do so for N transitions.

# 4. Replace each N transition by a DFA that simply reads through the next n input bits of G(a),
#    and each L transition by a DFA that reads through the next n - 1 bits of G(a) and each R transition reads the next input bit.

# 5. The resulting graph is a DFA whose behavior on G(a) is the same as T on a.
#    The size of this DFA is polynomial in n and the number of states in the finite control of T.

"""

def insert_immediate_states(dfa, from_state, to_state, read_value, num_symbol_reads):
    assert num_symbol_reads >= 2
    name_prefix = from_state + '_to_' + to_state
    dfa.add_transition(from_state, name_prefix + '_1', read_value)
    for i in range(2, num_symbol_reads):
        next_state = name_prefix + '_%d'%d
        dfa.add_transition_any_symbol(from_state, next_state)
        from_state = next_state
    dfa.add_transition_any_symbol(from_state, to_state)


def tm_to_dfa(tm, input_size):
    # Create the DFA
    dfa = DFA(
        states=set(),
        alphabet=tm.alphabet,
        accept_states=set()
    )
    n = input_size

    # Add transitions for the DFA
    # TODO: treat the write value, right now I'm ignoring this because we dont need if for tm's that compute a boolean formula.
    for from_state, read_value in tm.transitions:
        to_state, write_value, direction = tm.transitions[(from_state, read_value)]
        if direction == TuringMachine.LEFT:
            insert_immediate_states(dfa, from_state, to_state, read_value, n-1)
        elif direction == TuringMachine.RIGHT:
            dfa.add_transition(from_state, to_state, read_value)
        elif direction == TuringMachine.NEUTRAL:
            insert_immediate_states(dfa, from_state, to_state, read_value, n)

    # Add accept (and reject) states for the DFA
    # Once we reached the accept/reject states of the tm, read any symbol and stay in those states
    for acc_state in tm.accept_states:
        dfa.add_accept_state(acc_state)
        dfa.add_transition_any_symbol(acc_state, acc_state)
    for rej_state in tm.reject_states:
        dfa.add_transition_any_symbol(rej_state, rej_state)

    # Set the initial state for the DFA
    dfa.set_start_state(tm.initial_state)

    return dfa
