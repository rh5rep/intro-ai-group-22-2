import re
from sympy.logic.boolalg import to_cnf
from typing import Optional
from itertools import combinations
from resolution import negate_formula, resolution


class BeliefBase:
    """A class to represent a belief base for an agent with entrenchment."""

    def __init__(self):
        """Initialize an empty belief base."""
        self.beliefs = []  # list of tuples: (expr, entrenchment)

    def expand(self, belief: str, entrenchment: Optional[int] = 50):
        """Add a belief to the belief base with optional entrenchment."""
        self.beliefs.append((belief, entrenchment))

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
        self.expand(new_belief, entrenchment)

    def convert_to_cnf(self, belief: str) -> str:
        """Convert a belief to CNF (Conjunctive Normal Form)."""
        try:
            # Replace equivalence manually: p <<>> q  ->  (p >> q) & (q >> p)
            pattern = r"(.+?)\s*<<>>\s*(.+)"
            match = re.fullmatch(pattern, belief.strip())
            if match:
                left, right = match.groups()
                belief = f"({left} >> {right}) & ({right} >> {left})"
            
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

    def contract(self, formula: str):
        """Remove beliefs from the base so that it no longer entails `formula`."""
        print(f"Attempting to contract: {formula}")

        # Step 1: Check if formula is entailed
        negated = negate_formula(formula, self)
        if not resolution(self, negated):
            print("Formula not entailed — no contraction needed.")
            return  # Nothing to contract

        # Step 2: Try all subsets of the belief base
        original_beliefs = list(self.beliefs)
        for r in range(1, len(original_beliefs) + 1):
            for subset in combinations(original_beliefs, r):
                # build a temporary base excluding these beliefs
                temp_belief_base = BeliefBase()
                for b in original_beliefs:
                    if b not in subset:
                        temp_belief_base.expand(b[0], b[1])

                # check if the formula is still entailed
                if not resolution(temp_belief_base, negate_formula(formula, temp_belief_base)):
                    # choose this subset to remove (lowest entrenchment subset)
                    print(
                        f"Removing {len(subset)} beliefs to break entailment of '{formula}':")
                    for belief in subset:
                        print(f" - {belief[0]} (entrenchment: {belief[1]})")
                        self.remove_belief(belief[0])
                    return

        print("No suitable contraction found — base may be inconsistent or minimal.")

    def revise(self, formula: str, entrenchment: int = 50):
        """Revise the belief base with a new belief `formula`, ensuring consistency."""
        print(f"Revising belief base with: {formula}")
        negated = negate_formula(formula, self)

        # Step 1: Contract the negation of the formula
        self.contract(negated)

        # Step 2: Expand the belief
        self.expand(formula, entrenchment)


# vocabulary
# ~ is ¬
# & is ∧
# | is ∨
# >> is →
# <<>> is ↔
