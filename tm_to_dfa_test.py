from turing_machine import *
from tm_to_dfa import *
from formula_to_tm import *

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
    input_copies = 1 + tm.get_num_L_and_N_transitions()
    input = '01 '
    dfa = tm_to_dfa(tm, len(input))
    assert dfa.evaluate(input*input_copies) == tm.run(input)
    input = '0011 '
    dfa = tm_to_dfa(tm, len(input))
    assert dfa.evaluate(input*input_copies) == tm.run(input)
    input = '000111 '
    dfa = tm_to_dfa(tm, len(input))
    assert dfa.evaluate(input*input_copies) == tm.run(input)
    input = '00001111 '
    dfa = tm_to_dfa(tm, len(input))
    assert dfa.evaluate(input*input_copies) == tm.run(input)

    input = '011 '
    dfa = tm_to_dfa(tm, len(input))
    assert dfa.evaluate(input*input_copies) == tm.run(input)
    input = '0010 '
    dfa = tm_to_dfa(tm, len(input))
    assert dfa.evaluate(input*input_copies) == tm.run(input)


    # Set up a boolean circuit and reduce it to a TM
    tm = formula_to_turingmachine("NOT ((A OR B) AND C)")
    input_len = 3
    input_copies = 1 + tm.get_num_L_and_N_transitions()
    dfa = tm_to_dfa(tm, input_len)
    for x in range(2**input_len):
        input = format(x, f'0{input_len}b')
        try:
            assert dfa.evaluate(input*input_copies) == tm.run(input)
        except AssertionError:
            print("Error for %s" % input)

    # Set up a boolean circuit and reduce it to a TM
    tm = formula_to_turingmachine("((A OR B) AND (A OR C)) OR (NOT C)")
    input_len = 5
    input_copies = 1 + tm.get_num_L_and_N_transitions()
    dfa = tm_to_dfa(tm, input_len)
    for x in range(2**input_len):
        input = format(x, f'0{input_len}b')
        try:
            assert dfa.evaluate(input*input_copies) == tm.run(input)
        except AssertionError:
            print("Error for %s" % input)

    # Set up a boolean circuit and reduce it to a TM
    tm = formula_to_turingmachine("((A AND B) OR (A OR C)) OR NOT ((NOT C) AND (NOT (D OR E) AND (J AND D)))")
    input_len = 9
    input_copies = 1 + tm.get_num_L_and_N_transitions()
    dfa = tm_to_dfa(tm, input_len)
    for x in range(2**input_len):
        input = format(x, f'0{input_len}b')
        try:
            assert dfa.evaluate(input*input_copies) == tm.run(input)
        except AssertionError:
            print("Error for %s" % input)

#tm.draw_transition_diagram()
#dfa.draw_transition_diagram()