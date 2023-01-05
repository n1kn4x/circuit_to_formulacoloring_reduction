from dfa import *

def test_dfa():
    # Test DFA that recognizes strings with an even number of a's
    dfa = DFA(
        states=['q1', 'q2'],
        alphabet=['a', 'b'],
        start_state='q1',
        accept_states=['q1']
    )
    dfa.add_transition('q1', 'a', 'q2')
    dfa.add_transition('q1', 'b', 'q1')
    dfa.add_transition('q2', 'a', 'q1')
    dfa.add_transition('q2', 'b', 'q2')

    assert dfa.evaluate('a') == False
    assert dfa.evaluate('aa') == True
    assert dfa.evaluate('baa') == True
    assert dfa.evaluate('baaa') == False

    # Test DFA that recognizes strings that end in 01
    dfa = DFA(
        states=['q1', 'q2', 'q3'],
        alphabet=['0', '1'],
        start_state='q1',
        accept_states=['q3']
    )
    dfa.add_transition('q1', '0', 'q2')
    dfa.add_transition('q1', '1', 'q1')
    dfa.add_transition('q2', '1', 'q3')
    dfa.add_transition('q2', '0', 'q1')
    dfa.add_transition('q3', '0', 'q1')
    dfa.add_transition('q3', '1', 'q1')

    assert dfa.evaluate('0') == False
    assert dfa.evaluate('01') == True
    assert dfa.evaluate('010') == False
    assert dfa.evaluate('0101') == False
    assert dfa.evaluate('0101111100101') == True

test_dfa()
