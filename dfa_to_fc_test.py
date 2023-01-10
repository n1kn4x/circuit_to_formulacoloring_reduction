from dfa_to_fc import *
from dfa import *
from sympy import *

def test_formulacoloring():
    # Create a simple DFA
    dfa = DFA(states={"q0", "q1"}, start_state="q0", accept_states={"q0"})
    dfa.add_transition("q0", "q0", "0")
    dfa.add_transition("q0", "q1", "1")
    dfa.add_transition("q1", "q0", "1")
    dfa.add_transition("q1", "q1", "0")
    # Obtain a labeled sample from the DFA
    samples = dfa.generate_random_sample(m=10, n=8)
    # Construct Formula Coloring problem instance from the sample
    formula = formulacoloring(samples)
    # Check whether the coloring obtained from the DFA solves the Formula Coloring instance
    coloring = dfa_to_coloring(samples, dfa, states_as_colors=False)
    variables = coloring.keys()
    f = lambdify(variables, formula)
    assert f(**coloring) == True

    # Create a more complex DFA
    dfa = DFA(states={"q0", "q1", "q2", "q3", "q4"}, start_state="q0", accept_states={"q2"})
    dfa.add_transition("q0", "q1", "0")
    dfa.add_transition("q0", "q3", "1")
    dfa.add_transition("q1", "q2", "1")
    dfa.add_transition("q1", "q4", "0")
    dfa.add_transition("q2", "q2", "0")
    dfa.add_transition("q2", "q2", "1")
    dfa.add_transition("q3", "q4", "1")
    dfa.add_transition("q3", "q4", "0")
    dfa.add_transition("q4", "q3", "1")
    dfa.add_transition("q4", "q0", "0")
    # Obtain a labeled sample from the DFA
    samples = dfa.generate_random_sample(m=150, n=15)
    # Construct Formula Coloring problem instance from the sample
    formula = formulacoloring(samples)
    # Check whether the coloring obtained from the DFA solves the Formula Coloring instance
    coloring = dfa_to_coloring(samples, dfa, states_as_colors=False)
    variables = coloring.keys()
    f = lambdify(variables, formula)
    assert f(**coloring) == True
