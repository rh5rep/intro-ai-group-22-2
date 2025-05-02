# Belief Revision Agent

A simple belief revision agent that manages a belief base and uses resolution-based logical entailment checking.

## Features

This implementation includes:

1. **Belief Base Management**
   - Add beliefs with entrenchment levels
   - Remove beliefs
   - Convert beliefs to Conjunctive Normal Form (CNF)

2. **Logical Entailment Checking**
   - Resolution-based algorithm for checking if a formula is entailed by the belief base
   - Support for basic propositional logic syntax

## Usage

Run the program:

```
python main.py
```

### Commands

- `add <formula> [<entrenchment>]` - Add a belief with optional entrenchment (default 50)
- `entails <formula>` - Check if belief base entails the formula
- `remove <formula>` - Remove a belief
- `show` - Display current belief base
- `help` - Show help message
- `exit` - Exit the program

### Formula Syntax

- `p`, `q`, `r`, etc. - Atomic propositions
- `~p` - Negation
- `p & q` - Conjunction (AND)
- `p | q` - Disjunction (OR)
- `p >> q` - Implication (IF-THEN)
- `p <<>> q` - Equivalence (IFF)

## Example Session

```
> add p
Added belief: p (entrenchment: 50)

> add p >> q 75
Added belief: ~p | q (entrenchment: 75)

> show
Current Belief Base:
  1. p (entrenchment: 50)
  2. ~p | q (entrenchment: 75)

> entails q
The belief base entails: q

> add ~q
Error: Contradiction detected

> remove p
Removed belief: p

> show
Current Belief Base:
  1. ~p | q (entrenchment: 75)

> entails q
The belief base does not entail: q
```

## Implementation Details

The implementation consists of three main components:

1. **belief_base.py** - Handles belief base management, including adding, removing, and converting formulas to CNF
2. **resolution.py** - Provides the resolution algorithm for checking logical entailment
3. **main.py** - Provides a command-line interface for interacting with the belief base

The resolution algorithm works by:
1. Negating the formula to be checked
2. Converting all formulas to CNF
3. Trying to derive a contradiction through resolution
4. If a contradiction is found, the original formula is entailed by the belief base

## Requirements

- Python 3.6+
- SymPy (for CNF conversion)
