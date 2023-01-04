# Boolean Circuit Transformer

This project contains code that transforms a boolean circuit into a boolean formula, a Turing machine that computes the boolean formula, and a deterministic finite automaton (DFA) that accepts the input if the Turing machine outputs 1 and rejects if the Turing machine outputs 0.

## Boolean Circuit to Boolean Formula

The `boolean_formula` function takes in a boolean circuit as input and returns a boolean formula as output. The boolean circuit is represented using a data structure such as a dictionary, where the keys represent the nodes in the circuit and the values represent the operations performed at each node. The function traverses the boolean circuit using a depth-first search (DFS) algorithm, constructing the boolean formula as it goes. When it reaches a leaf node (i.e. a node with no children), it appends the value of the node to the boolean formula. When it reaches the end of the DFS, it returns the boolean formula as the output of the function.

## Boolean Formula to Turing Machine

The `boolean_formula_to_turing_machine` function takes in a boolean formula as a string and returns a Turing machine as output. It parses the boolean formula to determine the structure and operations being performed, using a stack-based algorithm to push and pop elements from the stack as it encounters parentheses and boolean operations. As it parses the formula, it constructs the corresponding Turing machine by defining the transition function and the start and accept states. When it reaches a leaf node (i.e. a boolean value such as "True" or "False"), it adds a transition to the Turing machine that causes it to halt and accept if the value is "True", or reject if the value is "False". When it has finished parsing the boolean formula, it returns the Turing machine as the output of the function.

## Turing Machine to DFA

The `turing_machine_to_dfa` function takes in a Turing machine as input and returns a deterministic finite automaton (DFA) as output. It converts the Turing machine's transition function into a set of states and transitions for the DFA, using the tape head position and the value on the tape as the input alphabet. The start state of the DFA is set to the start state of the Turing machine, and the accept and reject states of the DFA are set based on the accept and reject states of the Turing machine. The function then adds transitions between the states of the DFA based on the actions specified in the transition function of the Turing machine, such as moving the tape head left or right, or changing the value on the tape. When it has finished constructing the DFA, it returns it as the output of the function.

## Chaining the Transformations

To chain the transformations together and perform all three transformations in a single step, you can call the `boolean_circuit_to_dfa` function, which combines the code for all three transformations into a single function. The `boolean_circuit_to_dfa` function takes in a boolean circuit as input and returns a DFA as output. It first transforms the boolean circuit into a boolean formula using the `boolean_formula` function, and then transforms the boolean formula into a Turing machine using the `boolean_formula_to_turing_machine` function. Finally, it transforms the Turing machine into a DFA using the `turing_machine_to_dfa` function, and returns the resulting DFA as the output of the `boolean_circuit_to_dfa` function.

Here is an example of how to use the `boolean_circuit_to_dfa` function:

```python
from boolean_circuit_transformer import boolean_circuit_to_dfa

# Define the boolean circuit as a dictionary
boolean_circuit = {
    "root": Node("AND", [Node("True"), Node("False")])
}

# Transform the boolean circuit into a DFA
dfa = boolean_circuit_to_dfa(boolean_circuit)

# Use the DFA to decide whether to accept or reject the input
result = dfa.run()
if result == "accept":
    print("Accepted")
else:
    print("Rejected")
```

This will transform the boolean circuit into a DFA, and use the DFA to decide whether to accept or reject the input based on the output of the Turing machine.

## Contributing
To contribute to this project, please fork the repository and create a pull request with your changes. All contributions are welcome and appreciated!
