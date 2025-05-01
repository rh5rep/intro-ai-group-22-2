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
        if self.is_consistent(belief):
            self.beliefs.append((belief, entrenchment))
        else:
            raise ValueError(f"Contradiction detected: {belief}")

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

    def is_consistent(self, belief: str) -> bool:
        """Check if adding the belief causes any contradictions."""
        if not self.beliefs:
            return True
        all_beliefs = [b[0] for b in self.beliefs]
        combined = all_beliefs + [belief]
        return bool(satisfiable(to_cnf('&'.join(str(b) for b in combined), simplify=True)))

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