import sympy

# TODO Optimize! Now we are including many clauses two times, bc. we iterate over all combinations (i_1, i_2),
#  but e.g. clauses of (1,3) are the same as (3,1).
def formulacoloring(samples):
    # Create variables z_j_i for each i and j
    # z_j_i encodes the state that a DFA is in AFTER reading the j'th bit (starting from 1).
    # Hence z_0_i is the starting state.
    variables = {}
    for i, (w, b) in enumerate(samples):
        for j, bit in enumerate(w):
            variables[(i,j)] = sympy.symbols(f"z_{j}_{i}")
        variables[(i,j+1)] = sympy.symbols(f"z_{j+1}_{i}") # Need to add one more state, since j in z_j_i starts from 1.

    # Create formula F(S) as a conjunction of predicates
    formula = []
    for i_1, (w_1, b_1) in enumerate(samples):
        for i_2, (w_2, b_2) in enumerate(samples):
            # Clauses of (1,3) are the same as (3,1), so we can skip half of them
            if (i_2 < i_1):
                continue
            if not (b_1 == b_2):
                # Constraint that input strings in S that are accepted by M
                # must result in different final states than those strings
                # in S that are rejected by M
                formula.append(sympy.Ne(variables[(i_1, len(w_1))], variables[(i_2, len(w_2))]))
            for j_1, bit_1 in enumerate(w_1):
                # Need to convert to indexing starting from 1
                j_1 += 1
                for j_2, bit_2 in enumerate(w_2):
                    if bit_1 == bit_2:
                        # Need to convert to indexing starting from 1
                        j_2 += 1
                        # Skip adding clauses two times.
                        if (j_2 < j_1):
                            continue
                        # Constraint that if M is in the same state in two different
                        # computations on input strings from S, and the next input symbol
                        # is the same in both strings, then the next state in each computation
                        # must be the same
                        formula.append(sympy.Or(sympy.Ne(variables[(i_1, j_1-1)], variables[(i_2, j_2-1)]),
                                            sympy.Eq(variables[(i_1, j_1)], variables[(i_2, j_2)])))

    # Return the conjunction of all predicates as a single formula
    return sympy.And(*formula)

# This function is needed to test the formulacoloring function
def dfa_to_coloring(samples, dfa, states_as_colors=False):
    # Initialize data structure
    T = {state: set() for state in dfa.states}

    # Read w_i bit by bit, walk through the DFA and add fill the colors
    for i, (w, b) in enumerate(samples):
        # Begin by the starting state
        c = dfa.start_state
        T[c].add(f"z_0_{i}")
        for j, bit in enumerate(w):
            c = dfa.transitions[(c, bit)]
            T[c].add(f"z_{j+1}_{i}")

    # Convert T to a sympy.subs (substitution) friendly format
    subsitutions = {}
    for i, (state, variables) in enumerate(T.items()):
        for var in variables:
            subsitutions[var] = state if states_as_colors else i
    return subsitutions