from turing_machine import TuringMachine
from boolean_circuit import *

# Add intermediate transitions between going from from_state to to_state that move the cursor in some direction for num_moves times.
# We use these transitions when we skip an entire subcircuit/subtree because e.g. we encountered a left child that is 1 of an OR node, thus we need
# to move the cursor over all the bits/leafnode of tape/circuit that can be skipped.
def add_cursor_moves_before_state(tm, num_moves, from_state, to_state, direction='R'):
    assert(num_moves >= 1)
    intermediate_statename = from_state + '_to_' + to_state + '_%s_%d'%(direction, num_moves)
    tm.add_transition_any_symbol(from_state, intermediate_statename+'/1', direction)
    for i in range(1, num_moves):
        tm.add_transition_any_symbol(intermediate_statename+'/%d'%i, intermediate_statename+'/%d'%(i+1), direction)
    tm.add_transition_any_symbol(intermediate_statename+'/%d'%num_moves, to_state, 'N')

# Get the number of leafs in a subcircuit
def get_leaf_amount(node):
    if (node.left == None):
        return 1
    num_leafs = 0
    if (node.left != None):
        num_leafs += get_leaf_amount(node.left)
    if (node.right != None):
        num_leafs += get_leaf_amount(node.right)
    return num_leafs

# Get the leftmost leaf of a subcircuit
def get_leftmost_leaf(node):
    if (node.left == None):
        return node
    return get_leftmost_leaf(node.left)


# The turing machine works as follows.
# For each node in the circuit tree, we introduce 2 states (node.name+'_0' and node.name+'_1').
# The turing machine will be in state "..._0" if the node in the circuit evaluates to 0, otherwise
# the tm will be in state "..._1".
# The tm will start by reading the first bit on the tape and transition to the leftmost leaf node state
# of the circuit. If '0' has been read it will transition to leftmost_leaf(circuit.root).name+'_0' and "..._1" otherwise.
# From there we have transitions to further nodes based on the operation of the parent node.
# In the following code we add the transitions for every node based on the parent op, which determines how
# to proceed in evaluating the circuit tree.
def add_transitions_for_node(tm, node):
    if (node.parent.op == "NOT"):
        # Invert the saved value and go one up
        tm.add_transition_any_symbol(node.name+'_1', node.parent.name+'_0', 'N')
        tm.add_transition_any_symbol(node.name+'_0', node.parent.name+'_1', 'N')
    if (node.parent.op == "AND"):
        # The current node is the left child of parent
        if (node == node.parent.left):
            # If the current node evaluates to 1 ('..._1'), we can explore the right child of parent (Start at the leftmost leaf of the right subtree)
            # We read the leaf value and transition to the corresponding state
            tm.add_transition(node.name+'_1', get_leftmost_leaf(node.parent.right).name+'_0', '0', '0', 'R')
            tm.add_transition(node.name+'_1', get_leftmost_leaf(node.parent.right).name+'_1', '1', '1', 'R')
            # If the current node evaluates to 0, the parent node evaluates to 0. We can skip evaluating the entire right subcircuit of parent.
            # We also need to move the cursor to the right by the amount (+1) of leaf nodes in the right subtree of parent 
            add_cursor_moves_before_state(tm, get_leaf_amount(node.parent.right), node.name+'_0', node.parent.name+'_0', 'R')
        # The current node is the right child of parent
        if (node == node.parent.right):
            # If the current node evaluates to 1, the parent node also evaluates to 1. (We know that the left child of parent must have evaluated to 1.)
            tm.add_transition_any_symbol(node.name+'_1', node.parent.name+'_1', 'N')
            # If the current node evaluates to 0, the parent node also evaluates to 0
            tm.add_transition_any_symbol(node.name+'_0', node.parent.name+'_0', 'N')
    if (node.parent.op == "OR"):
        # The current node is the left child of parent
        if (node == node.parent.left):
            # If the current node evaluates to 1, the parent node also evaluates to 1. We can skip evaluating the entire right subcircuit of parent.
            add_cursor_moves_before_state(tm, get_leaf_amount(node.parent.right), node.name+'_1', node.parent.name+'_1', 'R')
            # If the current node evaluates to 0, we continue by the leftmost leaf of parent. (We read the leaf value and transition to the corresponding state)
            tm.add_transition(node.name+'_0', get_leftmost_leaf(node.parent.right).name+'_0', '0', '0', 'R')
            tm.add_transition(node.name+'_0', get_leftmost_leaf(node.parent.right).name+'_1', '1', '1', 'R')
        # The current node is the right child of parent
        if (node == node.parent.right):
            # If the current node evaluates to 1, the parent node also evaluates to 1.
            tm.add_transition_any_symbol(node.name+'_1', node.parent.name+'_1', 'N')
            # If the current node evaluates to 0, the parent node also evaluates to 0. (Since we know that the left child of parent must have been 0.)
            tm.add_transition_any_symbol(node.name+'_0', node.parent.name+'_0', 'N')

# Add all transitions for a circuit, by recursively adding the transistions for it's nodes
def add_transitions_for_circuit(tm, circuit):
    add_transitions_for_node(tm, circuit)
    if (circuit.left != None):
        add_transitions_for_circuit(tm, circuit.left)
    if (circuit.right != None):
        add_transitions_for_circuit(tm, circuit.right)

# Build a turing machine that computes a boolean function on inputs given on the tape
def formula_to_turingmachine(formula):
    circuit = tokenlist_to_circuit(formula_to_tokenlist(formula))
    tm = TuringMachine()
    tm.set_initial_state("START")
    tm.add_accept_state("ACCEPT")
    tm.add_reject_state("REJECT")
    # Add the first transition from the starting state to the first bit read
    startnode = get_leftmost_leaf(circuit)
    tm.add_transition("START", startnode.name+'_0', '0', '0', 'R')
    tm.add_transition("START", startnode.name+'_1', '1', '1', 'R')
    # Add the final transition, when the root node is evaluated we transition to either ACCEPT or REJECT
    endnode = circuit
    tm.add_transition_any_symbol(endnode.name+'_0', "REJECT", 'N')
    tm.add_transition_any_symbol(endnode.name+'_1', "ACCEPT", 'N')
    # Add all remaining transistions for all other nodes in the circuit
    if (circuit.left != None):
        add_transitions_for_circuit(tm, circuit.left)
    if (circuit.right != None):
        add_transitions_for_circuit(tm, circuit.right)
    return tm



            
