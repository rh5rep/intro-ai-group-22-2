import re
from sympy.logic.boolalg import to_cnf, simplify_logic
from sympy.parsing.sympy_parser import parse_expr
from typing import Optional
from itertools import combinations
from resolution import negate_formula, resolution


class BeliefBase:
    """A class to represent a belief base for an agent with entrenchment."""

    def __init__(self):
        """Initialize an empty belief base."""
        self.beliefs = []  # list of tuples: (expr, entrenchment)

    def expand(self, belief: str, entrenchment: Optional[int] = 50):
        """Add a belief to the belief base with optional entrenchment, after simplification."""
        simplified = self.convert_to_cnf(belief)
        self.beliefs.append((simplified, entrenchment))

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
        """Convert a belief to simplified CNF form (handles <<>> and ~~)."""
        try:
            match = re.fullmatch(r"(.+?)\s*<<>>\s*(.+)", belief.strip())
            if match:
                left, right = match.groups()
                belief = f"({left} >> {right}) & ({right} >> {left})"

            # Parse and simplify logic
            expr = parse_expr(belief, evaluate=False)
            simplified_expr = simplify_logic(to_cnf(expr, simplify=True), form='cnf')
            return str(simplified_expr)
        except Exception as e:
            raise ValueError(f"Invalid formula or unsupported syntax: '{belief}' → {e}")


    def get_entrenchment(self, belief: str) -> int:
        """Return the entrenchment value of a belief."""
        for b in self.beliefs:
            if b[0] == belief:
                return b[1]
        raise ValueError(f"Belief not found: {belief}")


    def contract(self, formula: str):
        """Remove the least entrenched subset of beliefs so that the belief base no longer entails `formula`."""
        print(f"Attempting to contract: {formula}")

        # Step 1: Check if formula is entailed
        negated = negate_formula(formula, self)
        if not resolution(self, negated):
            print("Formula not entailed — no contraction needed.")
            return  # Nothing to contract

        original_beliefs = list(self.beliefs)
        successful_subsets = []

        # Step 2: Try all subsets of the belief base
        for r in range(1, len(original_beliefs) + 1):
            for subset in combinations(original_beliefs, r):
                # Build a temporary base excluding this subset
                temp_base = BeliefBase()
                for b in original_beliefs:
                    if b not in subset:
                        temp_base.expand(b[0], b[1])

                if not resolution(temp_base, negate_formula(formula, temp_base)):
                    # Store subset and its total entrenchment
                    total_entrenchment = sum(b[1] for b in subset)
                    successful_subsets.append((subset, total_entrenchment))

        if not successful_subsets:
            print("No suitable contraction found — base may be inconsistent or minimal.")
            return

        # Step 3: Pick the subset with the lowest total entrenchment
        best_subset, min_score = min(successful_subsets, key=lambda x: x[1])
        print(f"Removing {len(best_subset)} beliefs (lowest entrenchment: {min_score}) to break entailment of '{formula}':")
        for belief in best_subset:
            print(f" - {belief[0]} (entrenchment: {belief[1]})")
            self.remove_belief(belief[0])


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
