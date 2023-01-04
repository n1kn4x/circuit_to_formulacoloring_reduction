from boolean_circuit import *
from turing_machine import *
from formula_to_tm import *

def test_formula_to_turingmachine():
    # Test AND and OR operators
    formula = "A AND (B OR C)"
    tm = formula_to_turingmachine(formula)
    assert tm.run('000') == False
    assert tm.run('001') == False
    assert tm.run('010') == False
    assert tm.run('011') == False
    assert tm.run('100') == False
    assert tm.run('101') == True
    assert tm.run('110') == True
    assert tm.run('111') == True

    # Test NOT operator
    formula = "NOT A"
    tm = formula_to_turingmachine(formula)
    assert tm.run('0') == True
    assert tm.run('1') == False

    # Test nested NOT operator
    formula = "NOT (NOT A)"
    tm = formula_to_turingmachine(formula)
    assert tm.run('0') == False
    assert tm.run('1') == True
    
    # Test combination of NOT, AND and OR operators
    formula = "NOT (A AND (B OR C))"
    tm = formula_to_turingmachine(formula)
    assert tm.run('000') == True
    assert tm.run('001') == True
    assert tm.run('010') == True
    assert tm.run('011') == True
    assert tm.run('100') == True
    assert tm.run('101') == False
    assert tm.run('110') == False
    assert tm.run('111') == False

    # Test a complex formula
    formula = "(NOT (A AND B)) OR ((C AND D) OR (NOT E))"
    tm = formula_to_turingmachine(formula)
    assert tm.run('00000') == True
    assert tm.run('00001') == True
    assert tm.run('00010') == True
    assert tm.run('00011') == True
    assert tm.run('00100') == True
    assert tm.run('00101') == True
    assert tm.run('00110') == True
    assert tm.run('00111') == True
    assert tm.run('01000') == True
    assert tm.run('01001') == True
    assert tm.run('01010') == True
    assert tm.run('01011') == True
    assert tm.run('01100') == True
    assert tm.run('01101') == True
    assert tm.run('01110') == True
    assert tm.run('01111') == True
    assert tm.run('10000') == True
    assert tm.run('10001') == True
    assert tm.run('10010') == True
    assert tm.run('10011') == True
    assert tm.run('10100') == True
    assert tm.run('10101') == True
    assert tm.run('10110') == True
    assert tm.run('10111') == True
    assert tm.run('11000') == True
    assert tm.run('11001') == False
    assert tm.run('11010') == True
    assert tm.run('11011') == False
    assert tm.run('11100') == True
    assert tm.run('11101') == False
    assert tm.run('11110') == True
    assert tm.run('11111') == True

test_formula_to_turingmachine()
