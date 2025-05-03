class BeliefBase:
    """A class to represent a belief base for an agent."""

    def __init__(self):
        """Initialize an empty belief base."""
        self.beliefs = []

    def add_belief(self, belief: str):
        """Add a belief to the belief base."""
        if self.is_consistent(belief):
            self.beliefs.append(belief)
        else:
            raise ValueError(f"Contradiction detected: {belief}")

    def remove_belief(self, belief: str):
        """Remove a belief from the belief base."""
        if belief in self.beliefs:
            self.beliefs.remove(belief)
        else:
            raise ValueError(f"Belief not found: {belief}")

    def update_belief(self, old_belief: str, new_belief: str):
        """Update an existing belief in the belief base."""
        try:
            self.remove_belief(old_belief)
            self.add_belief(new_belief)
        except ValueError as e:
            raise e

    def is_consistent(self, belief: str) -> bool:
        """Check if adding the belief causes any contradictions."""
        for existing_belief in self.beliefs:
            if self._is_contradiction(existing_belief, belief):
                return False
        return True

    def _is_contradiction(self, belief1: str, belief2: str) -> bool:
        """Check if two beliefs contradict each other."""
        # First, check for direct negations like ¬p and p
        if belief1 == f"~{belief2}" or belief2 == f"~{belief1}":
            return True

        # conjunctions (e.g., p ∧ q contradicts ¬p)
        if "∧" in belief1 and "~" in belief2:
            literals = belief1.split("∧")
            for lit in literals:
                if f"~{lit.strip()}" in belief2 or lit.strip() in belief2:
                    return True

        # implications (e.g., p -> q contradicts ¬q when p is true)
        if "->" in belief1 and "~" in belief2:
            # Decompose implication into ¬p ∨ q
            left, right = belief1.split("->")
            if left.strip() == belief2:
                return True
            if right.strip() == belief2:
                return True
        
        # More complex logical operations can be added here as needed
        return False

    def convert_to_cnf(self, belief: str) -> str:
        """Convert a belief to CNF (Conjunctive Normal Form)."""
        # todo: this is a placeholder for the actual CNF conversion.
        if "->" in belief:
            belief = belief.replace("->", "∨")
        return belief
    

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
        

# ~ is ¬
# Example usage:
if __name__ == "__main__":
    belief_base = BeliefBase()

    # Add beliefs
    belief_base.add_belief("p")
    belief_base.add_belief("q")
    
    # Try to add a contradictory belief
    try:
        belief_base.add_belief("~p")  # Should raise an exception
    except ValueError as e:
        print(e)
    
    # Update a belief
    belief_base.update_belief("q", "~q")
    
    # Remove a belief
    belief_base.remove_belief("~q")

    # Convert belief to CNF
    cnf_belief = belief_base.convert_to_cnf("p -> q")
    print(f"CNF form: {cnf_belief}")

