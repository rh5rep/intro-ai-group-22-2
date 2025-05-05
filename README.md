# Belief Revision Agent

A belief revision system built in Python, implementing the **AGM belief revision framework** with logical entailment via **resolution**. It allows expansion, contraction, and revision of a propositional belief base with entrenchment levels for each belief.

## Features

### 1. Belief Base Management
- Beliefs are stored as propositional logic formulas.
- Each belief has an associated **entrenchment level** (default: 50).
- Operations:
  - **Expand** (task 4): add a belief without checking for consistency.
  - **Remove**: delete a belief.
  - **Revise** (task 3): contract the base to remove contradiction, then expand with the new belief.

### 2. Logical Entailment (Task 2)
- Uses a **custom resolution algorithm** (not imported from external logic libraries).
- Checks whether a belief is entailed by the belief base.
- Formulas are automatically converted to **CNF** using SymPy.

### 3. Syntax Support
Supports propositional logic with:
- `~p` – negation
- `p & q` – conjunction (AND)
- `p | q` – disjunction (OR)
- `p >> q` – implication
- `p <<>> q` – equivalence (converted internally to `(p >> q) & (q >> p)`)
- Parentheses for grouping: `(p & q) >> (r | ~s)`

### 4. CLI Interface (via `cmd` module)
- Interactive shell to explore belief operations
- Includes help, command parsing, and graceful exit handling (e.g. `Ctrl+D`).

---

## Requirements

```bash
pip install -r requirements.txt
```

---

## Running

launch interactive CLI
```bash
python run.py
```

run test suite
```bash
python test.py
```

run automated demonstrations
```bash
python demonstrate.py
```

---

## CLI Commands

| Command | Description |
|--------|-------------|
| `expand <formula> [entrenchment]` | Adds a belief to the base without checking for consistency. |
| `revise <formula> [entrenchment]` | Performs full AGM revision: contracts ¬φ then expands φ. |
| `remove <formula>` | Removes a belief from the base. |
| `entails <formula>` | Checks whether the belief base entails a given formula. |
| `show` | Displays all current beliefs in the base. |
| `help` | Shows available commands. |
| `exit` | Exits the CLI. |

---

## Example Session

```bash
> expand p
Expanded belief base with: p (entrenchment: 50)

> expand p >> q 75
Expanded belief base with: q | ~p (entrenchment: 75)

> entails q
The belief base entails: q

> expand ~q
Expanded belief base with: ~q (entrenchment: 50)

> revise ~q 40
Revising belief base with: ~q
Attempting to contract: q
Removing 1 beliefs to break entailment of 'q':
 - p (entrenchment: 50)
Expanded belief base with: ~q (entrenchment: 40)

> show
Current Belief Base:
  1. q | ~p (entrenchment: 75)
  2. ~q (entrenchment: 40)
```

---

## Project Structure

```
├── belief_base.py      # Core belief base logic (tasks 1, 3, 4)
├── resolution.py       # Custom resolution-based entailment checker (task 2)
├── cli.py              # Interactive shell interface (via cmd module)
├── run.py              # Entry point to CLI
├── demonstrate.py      # Demonstration of all core tasks with logging
├── test.py             # Unit tests covering all functionality
└── README.md           # You are here
```

---

## Test Coverage

The `test.py` module tests:

- Belief expansion, update, removal
- Entrenchment values and edge cases
- CNF conversion (including nested equivalences and implications)
- Contraction (removal of beliefs to break entailment)
- Revision (contract + expand)
- Logical entailment resolution

---

## Notes

- Expansion does **not** check consistency — by design (aligned with AGM theory).
- `revise` is the proper way to add beliefs if consistency is required.
- Logical formulas must follow the syntax and use correct parentheses for grouping.