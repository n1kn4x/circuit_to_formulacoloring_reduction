from turing_machine import TuringMachine
from tm_to_dfa import *

def test_tm_to_dfa():
    # Set up a Turing machine to recognize the language {0^n + 1^n + ' '|0 <= n >= 4}
    tm = TuringMachine()
    tm.alphabet = {'0', '1', ' '}
    tm.add_transition('q00', 'q01', '0', '0', TuringMachine.RIGHT)
    tm.add_transition('q01', 'q02', '0', '0', TuringMachine.RIGHT)
    tm.add_transition('q02', 'q03', '0', '0', TuringMachine.RIGHT)
    tm.add_transition('q03', 'q04', '0', '0', TuringMachine.RIGHT)
    tm.add_transition('q04', 'REJECT', '0', '0', TuringMachine.RIGHT)
    tm.add_transition('q00', 'REJECT', '1', '1', TuringMachine.RIGHT)
    tm.add_transition('q01', 'q14', '1', '1', TuringMachine.RIGHT)
    tm.add_transition('q02', 'q13', '1', '1', TuringMachine.RIGHT)
    tm.add_transition('q03', 'q12', '1', '1', TuringMachine.RIGHT)
    tm.add_transition('q04', 'q11', '1', '1', TuringMachine.RIGHT)
    tm.add_transition('q11', 'q12', '1', '1', TuringMachine.RIGHT)
    tm.add_transition('q12', 'q13', '1', '1', TuringMachine.RIGHT)
    tm.add_transition('q13', 'q14', '1', '1', TuringMachine.RIGHT)
    tm.add_transition('q14', 'ACCEPT', ' ', ' ', TuringMachine.RIGHT)
    tm.add_transition('q14', 'REJECT', '1', '1', TuringMachine.RIGHT)
    tm.add_transition('q11', 'REJECT', '0', '0', TuringMachine.RIGHT)
    tm.add_transition('q12', 'REJECT', '0', '0', TuringMachine.RIGHT)
    tm.add_transition('q13', 'REJECT', '0', '0', TuringMachine.RIGHT)
    tm.add_transition('q14', 'REJECT', '0', '0', TuringMachine.RIGHT)

    # Reading whitespace too early is rejected
    tm.add_transition('q01', 'REJECT', ' ', ' ', TuringMachine.RIGHT)
    tm.add_transition('q02', 'REJECT', ' ', ' ', TuringMachine.RIGHT)
    tm.add_transition('q03', 'REJECT', ' ', ' ', TuringMachine.RIGHT)
    tm.add_transition('q04', 'REJECT', ' ', ' ', TuringMachine.RIGHT)
    tm.add_transition('q11', 'REJECT', ' ', ' ', TuringMachine.RIGHT)
    tm.add_transition('q12', 'REJECT', ' ', ' ', TuringMachine.RIGHT)
    tm.add_transition('q13', 'REJECT', ' ', ' ', TuringMachine.RIGHT)

    tm.set_initial_state('q00')
    tm.add_reject_state('REJECT')
    tm.add_accept_state('ACCEPT')


    # Test input strings in the language
    assert tm.run('01 ') == True
    dfa = tm_to_dfa(tm, 3)
    assert dfa.evaluate('01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 01 ') == True
    # TODO MORE TESTS!
    


"""
    assert tm.run('0011 ') == True
    assert tm.run('000111 ') == True
    assert tm.run('00001111 ') == True

    # Test input strings not in the language
    assert tm.run('1 ') == False
    assert tm.run('10 ') == False
    assert tm.run('1010 ') == False
    assert tm.run('001011 ') == False
    assert tm.run('0001110 ') == False
    assert tm.run('00 0111 ') == False
"""
