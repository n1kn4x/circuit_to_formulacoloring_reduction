class BooleanCircuit:
    def __init__(self, value=None, left=None, right=None, op=None, parent=None):
        if value in ['True', 'False']:
            self.value = value == 'True'
        else:
            self.value = value
        self.left = left
        self.right = right
        self.op = op
        self.parent = parent
    
    def evaluate(self):
        if self.op == 'AND':
            return self.left.evaluate() and self.right.evaluate()
        elif self.op == 'OR':
            return self.left.evaluate() or self.right.evaluate()
        elif self.op == 'NOT':
            return not self.left.evaluate()
        else:
            return self.value
    
    def to_formula(self):
        if self.op == 'AND':
            return '(' + self.left.to_formula() + ' AND ' + self.right.to_formula() + ')'
        elif self.op == 'OR':
            return '(' + self.left.to_formula() + ' OR ' + self.right.to_formula() + ')'
        elif self.op == 'NOT':
            return '(NOT ' + self.left.to_formula() + ')'
        else:
            return str(self.value)


def formula_to_tokenlist(formula):
    # Initialize the result list
    result = []
    # Iterate through the formula and extract the tokens
    i = 0
    while i < len(formula):
        # Get the current character
        c = formula[i]
        # If the character is a letter or digit, extract the whole word or number
        if c.isalpha() or c.isdigit():
            start = i
            while i < len(formula) and (formula[i].isalpha() or formula[i].isdigit()):
                i += 1
            result.append(formula[start:i])
        # Ignore whitespace characters
        elif c.isspace():
            i += 1
        # Otherwise, add the character to the result list
        else:
            result.append(c)
            i += 1
    return result


def tokenlist_to_circuit(tokenlist, parent=None):
    # Base case: the formula consists of a single variable
    if (len(tokenlist) == 1):
        return BooleanCircuit(value=tokenlist[0], parent=parent)
    # Find the outmost operator or variable
    # Recursively call this function for the children of the outmost node. Pass the correct parent of the children down the recursion.
    open_parantheses = 0
    for i in range(len(tokenlist)):
        token = tokenlist[i]
        if (open_parantheses == 0):
            if (token == "NOT"):
                node = BooleanCircuit(op="NOT", parent=parent)
                node.left = tokenlist_to_circuit(tokenlist[i+1:], parent=node)
                return node
            if (token in ["AND", "OR"]):
                node = BooleanCircuit(op=token, parent=parent)
                node.left = tokenlist_to_circuit(tokenlist[:i], parent=node)
                node.right = tokenlist_to_circuit(tokenlist[i+1:], parent=node)
                return node

        if (token == '('):
            open_parantheses += 1
        if (token == ')'):
            open_parantheses -= 1
    # No outmost operators has been found. 
    # Remove parantheses that might be the first and last tokens and try again
    if (tokenlist[0] == '(' and tokenlist[-1] == ')'):
        tokenlist = tokenlist[1:-1]
        return tokenlist_to_circuit(tokenlist, parent=parent)
