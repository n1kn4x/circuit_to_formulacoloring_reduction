from boolean_circuit import BooleanCircuit, formula_to_tokenlist, tokenlist_to_circuit

def test_formula_to_tokenlist():
    assert formula_to_tokenlist('(A AND B) OR NOT C') == ['(', 'A', 'AND', 'B', ')', 'OR', 'NOT', 'C']
    assert formula_to_tokenlist('A AND (B OR C)') == ['A', 'AND', '(', 'B', 'OR', 'C', ')']
    assert formula_to_tokenlist('A AND B OR C') == ['A', 'AND', 'B', 'OR', 'C']
    assert formula_to_tokenlist('NOT A') == ['NOT', 'A']
    assert formula_to_tokenlist('A') == ['A']
    assert formula_to_tokenlist('1') == ['1']
    assert formula_to_tokenlist('FOO123') == ['FOO123']
    assert formula_to_tokenlist('(A AND B) OR (C AND D)') == ['(', 'A', 'AND', 'B', ')', 'OR', '(', 'C', 'AND', 'D', ')']
    assert formula_to_tokenlist('((A AND B) OR (C AND D)) OR True') == ['(', '(', 'A', 'AND', 'B', ')', 'OR', '(', 'C', 'AND', 'D', ')', ')', 'OR', 'True']
    formula = '((True OR (False AND (NOT True))) AND (True AND (False OR (NOT False))))'
    tokens = ['(', '(', 'True', 'OR', '(', 'False', 'AND', '(', 'NOT', 'True', ')', ')', ')', 'AND', '(', 'True', 'AND', '(', 'False', 'OR', '(', 'NOT', 'False', ')', ')', ')', ')']
    assert formula_to_tokenlist(formula) == tokens

def test_tokenlist_to_circuit():
    # Test a simple AND function
    tokens = ['A', 'AND', 'B']
    circuit = tokenlist_to_circuit(tokens)
    assert circuit.to_formula() == '(A AND B)'
    # Test a simple OR function
    tokens = ['A', 'OR', 'B']
    circuit = tokenlist_to_circuit(tokens)
    assert circuit.to_formula() == '(A OR B)'
    # Test a more complex function
    tokens = ['(', 'A', 'AND', 'B', ')', 'OR', 'NOT', 'C']
    circuit = tokenlist_to_circuit(tokens)
    assert circuit.to_formula() == '((A AND B) OR (NOT C))'
    # Test a function with multiple levels of nesting
    tokens = ['(', '(', 'A', 'AND', 'B', ')', 'OR', 'C', ')', 'AND', 'D']
    circuit = tokenlist_to_circuit(tokens)
    assert circuit.to_formula() == '(((A AND B) OR C) AND D)'
    # Test a more complex circuit
    tokens = ['(', '(', 'True', 'OR', '(', 'False', 'AND', '(', 'NOT', 'True', ')', ')', ')', 'AND', '(', 'True', 'AND', '(', 'False', 'OR', '(', 'NOT', 'False', ')', ')', ')', ')']
    circuit = tokenlist_to_circuit(tokens)
    assert circuit.op == 'AND'
    assert circuit.left.op == 'OR'
    assert circuit.left.left.value == True
    assert circuit.left.right.op == 'AND'
    assert circuit.left.right.left.value == False
    assert circuit.left.right.right.op == 'NOT'
    assert circuit.left.right.right.left.value == True
    assert circuit.right.op == 'AND'
    assert circuit.right.left.value == True
    assert circuit.right.right.op == 'OR'
    assert circuit.right.right.left.value == False
    assert circuit.right.right.right.op == 'NOT'
    assert circuit.right.right.right.left.value == False
    

# Test the evaluate method
def test_evaluate():
    # Test a more complex AND circuit
    a = BooleanCircuit(value=True)
    b = BooleanCircuit(value=False)
    c = BooleanCircuit(value=True)
    and1 = BooleanCircuit(left=a, right=b, op='AND')
    and2 = BooleanCircuit(left=and1, right=c, op='AND')
    assert and2.evaluate() == False

    # Test a more complex OR circuit
    or1 = BooleanCircuit(left=a, right=b, op='OR')
    or2 = BooleanCircuit(left=or1, right=c, op='OR')
    assert or2.evaluate() == True

    # Test a NOT circuit with a more complex child
    not_circuit = BooleanCircuit(left=and2, op='NOT')
    assert not_circuit.evaluate() == True

# Test the to_formula method
def test_to_formula():
    # Test a more complex AND circuit
    a = BooleanCircuit(value=True)
    b = BooleanCircuit(value=False)
    c = BooleanCircuit(value=True)
    and1 = BooleanCircuit(left=a, right=b, op='AND')
    and2 = BooleanCircuit(left=and1, right=c, op='AND')
    assert and2.to_formula() == '((True AND False) AND True)'

    # Test a more complex OR circuit
    or1 = BooleanCircuit(left=a, right=b, op='OR')
    or2 = BooleanCircuit(left=or1, right=c, op='OR')
    assert or2.to_formula() == '((True OR False) OR True)'

    # Test a NOT circuit with a more complex child
    not_circuit = BooleanCircuit(left=and2, op='NOT')
    assert not_circuit.to_formula() == '(NOT ((True AND False) AND True))'

    
test_evaluate()
test_to_formula()
test_formula_to_tokenlist()
test_tokenlist_to_circuit()
