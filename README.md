# Boolean Circuit to Formula Coloring
This repository contains the code for constructing advantage-bearing formula coloring instances as described in the paper: "A super-polynomial quantum advantage for combinatorial optimization problems" (https://arxiv.org/abs/2212.08678)

## Overview
The modules included in this repository are:
- `turing_machine.py`: A module for defining Turing machines and their transition functions.
- `dfa.py`: A module for defining Deterministic Finite Automata (DFA) and their transition functions.
- `boolean_circuit.py` : A module for defining Boolean circuits.

A well as the reductions among them:
- `formula_to_tm.py`: A module for reducing a Boolean Formula, as obtained from a Boolean Circuit, to a Turing machine.
- `tm_to_dfa.py`: A module for reducing a Turing Machine to a DFA.
- `dfa_to_fc.py`: A module for reducing a DFA to a formula coloring instance.

## Usage
We provide some tests as an example on how to use the modules.
