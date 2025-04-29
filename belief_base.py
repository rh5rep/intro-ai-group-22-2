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

