
belief_base = {
    "P → Q": {"entrenchment": 5},
    "Q → R": {"entrenchment": 3},
    "¬R": {"entrenchment": 2}
}

def to_cnf(belief):
    """Convert a belief to CNF (Conjunctive Normal Form)."""

    cnf_belief = f"CNF({belief})"
    print(f"Converted '{belief}' to CNF: {cnf_belief}")
    return cnf_belief

def remove_implication(belief):
    """Remove implication from a belief."""
    if "→" in belief:
        premise, conclusion = belief.split("→")
        new_belief = f"¬{premise} ∨ {conclusion}"
        print(f"Removed implication from '{belief}': {new_belief}")
        return new_belief
    return belief

# def demorgan(belief):
#     """Apply De Morgan's laws to a belief."""
#     if "¬" in belief:
#         negated_belief = belief.replace("¬", "")
#         new_belief = f"¬({negated_belief})"
#         print(f"Applied De Morgan's law to '{belief}': {new_belief}")
#         return new_belief
#     return belief


remove_implication("P → Q")
# demorgan("¬(P ∧ Q)")