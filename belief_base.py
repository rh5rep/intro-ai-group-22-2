from sympy import satisfiable
from sympy.logic.boolalg import to_cnf
from typing import Optional


class BeliefBase:
    """A class to represent a belief base for an agent with entrenchment."""

    def __init__(self):
        """Initialize an empty belief base."""
        self.beliefs = []  # list of tuples: (expr, entrenchment)

    def add_belief(self, belief: str, entrenchment: Optional[int] = 50):
        """Add a belief to the belief base with optional entrenchment."""
        # TODO: Use Rami's check for contradiction (resolution) 
        self.beliefs.append((belief, entrenchment))
        # if self.is_consistent(belief):
        #     self.beliefs.append((belief, entrenchment))
        # else:
        #     raise ValueError(f"Contradiction detected: {belief}")

    def remove_belief(self, belief: str):
        """Remove a belief from the belief base."""
        for b in self.beliefs:
            if b[0] == belief:
                self.beliefs.remove(b)
                return
        raise ValueError(f"Belief not found: {belief}")

    def update_belief(self, old_belief: str, new_belief: str, entrenchment: Optional[int] = 50):
        """Update an existing belief in the belief base."""
        self.remove_belief(old_belief)
        self.add_belief(new_belief, entrenchment)

    # def is_consistent(self, belief: str) -> bool:
    #     """Check if adding the belief causes any contradictions."""
    #     if not self.beliefs:
    #         return True
    #     all_beliefs = [b[0] for b in self.beliefs]
    #     combined = all_beliefs + [belief]
    #     return bool(satisfiable(to_cnf('&'.join(str(b) for b in combined), simplify=True)))

    def convert_to_cnf(self, belief: str) -> str:
        """Convert a belief to CNF (Conjunctive Normal Form)."""
        try:
            cnf_expr = to_cnf(belief, simplify=True)
            return str(cnf_expr)
        except Exception as e:
            raise ValueError(f"Failed to convert belief to CNF: {e}")

    def get_entrenchment(self, belief: str) -> int:
        """Return the entrenchment value of a belief."""
        for b in self.beliefs:
            if b[0] == belief:
                return b[1]
        raise ValueError(f"Belief not found: {belief}")
    def _parse_belief(self, belief: str):
        """Parse the belief string into a sympy expression."""
        try:
            # Replace custom operators with sympy's
            for op_str, op_func in self._operator_mapping.items():
                belief = belief.replace(op_str, f' {op_func.__name__} ')
            return parse_mathematica(belief)
        except Exception as e:
            raise ValueError(f"Failed to parse belief '{belief}': {e}")

    def _entails(self, belief: str, base: Optional[List[Tuple[str, Optional[int]]]] = None) -> bool:
        """Check if the belief base (or a given base) entails a belief."""
        expressions = []
        check_base = base if base is not None else self.beliefs
        for b, _ in check_base:
            try:
                expressions.append(self._parse_belief(b))
            except ValueError as e:
                print(f"Warning: Skipping unparseable belief in entailment check: {e}")
                continue

        if not expressions:
            return False

        try:
            negation_of_belief = Not(self._parse_belief(belief))
            combined_expr = And(*expressions, negation_of_belief)
            return not satisfiable(combined_expr)
        except ValueError as e:
            print(f"Warning: Could not parse belief '{belief}' for entailment check: {e}")
            return False

    def contraction(self, belief_to_remove: str):
        """Perform contraction on the belief base based on entrenchment."""
        if not any(b[0] == belief_to_remove for b in self.beliefs):
            raise ValueError(f"Belief not found: {belief_to_remove}")

        # If the belief base does not entail the belief to remove, simply remove it.
        if not self._entails(belief_to_remove):
            self.remove_belief(belief_to_remove)
            return

        # If the belief base entails the belief to remove, we need to remove
        # less entrenched beliefs until the entailment no longer holds.

        entrenchment_to_remove = self.get_entrenchment(belief_to_remove)
        sorted_beliefs = sorted(self.beliefs, key=lambda b: b[1] if b[1] is not None else float('inf'))

        beliefs_to_keep = list(self.beliefs)

        # Iteratively remove beliefs with entrenchment less than or equal to
        # the belief to be removed, checking if the entailment still holds.
        for b, ent in sorted_beliefs:
            if b == belief_to_remove:
                continue
            if ent is not None and ent <= entrenchment_to_remove:
                temp_base = [item for item in beliefs_to_keep if item[0] != b]
                if self._entails(belief_to_remove, temp_base):
                    beliefs_to_keep.remove((b, ent))
                else:
                    # Removing this belief broke the entailment, so we keep it and remove the target
                    self.beliefs = beliefs_to_keep
                    self.remove_belief(belief_to_remove)
                    return

        # If we reach here, it means even after removing all less or equally entrenched
        # beliefs, the entailment might still hold (or there were no such beliefs).
        # In a more sophisticated system, further strategies might be needed.
        self.beliefs = beliefs_to_keep
        self.remove_belief(belief_to_remove)
        print(f"Warning: Basic contraction of '{belief_to_remove}' performed.")

# vocabulary
# ~ is ¬
# & is ∧
# | is ∨
# >> is →
# <<>> is ↔


if __name__ == "__main__":
    belief_base = BeliefBase()

    # Test 1: Add consistent beliefs
    try:
        belief_base.add_belief("p", entrenchment=10)
        belief_base.add_belief("q", entrenchment=80)
        print("Test 1 Passed: Added 'p' (10) and 'q' (80)")
    except Exception as e:
        print("Test 1 Failed:", e)

    # Test 2: Try adding a contradictory belief
    try:
        belief_base.add_belief("~p", entrenchment=20)
        print("Test 2 Failed: Contradiction not detected")
    except ValueError as e:
        print("Test 2 Passed:", e)

    # Test 3: Update a belief
    try:
        belief_base.update_belief("q", "~q", entrenchment=60)
        print("Test 3 Passed: Updated 'q' → '~q'")
    except Exception as e:
        print("Test 3 Failed:", e)

    # Test 4: Remove a belief
    try:
        belief_base.remove_belief("~q")
        print("Test 4 Passed: Removed '~q'")
    except Exception as e:
        print("Test 4 Failed:", e)

    # Test 5: Convert implication to CNF
    try:
        cnf = belief_base.convert_to_cnf("p >> q")
        print(f"Test 5 Passed: CNF of 'p >> q' is '{cnf}'")
    except Exception as e:
        print("Test 5 Failed:", e)

    # Test 6: Check entrenchment of 'p'
    try:
        entrenchment = belief_base.get_entrenchment("p")
        assert entrenchment == 10
        print(f"Test 6 Passed: Entrenchment of 'p' is {entrenchment}")
    except Exception as e:
        print("Test 6 Failed:", e)