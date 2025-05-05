"""Implementation of the resolution algorithm for propositional logic."""

def negate_formula(formula, belief_base):
    """Negate the formula and apply De Morgan's laws if needed."""
    if "&" in formula:
        # Apply De Morgan's law for conjunctions: ~(p&q) = ~p | ~q
        terms = formula.split("&")
        negated_terms = [f"~{term.strip()}" for term in terms]
        negated_formula = " | ".join(negated_terms)
    elif "|" in formula:
        # Apply De Morgan's law for disjunctions: ~(p|q) = ~p & ~q
        terms = formula.split("|")
        negated_terms = [f"~{term.strip()}" for term in terms]
        negated_formula = " & ".join(negated_terms)
    else:
        # Simple negation for atomic formulas
        negated_formula = f"~{formula}"
    
    # Convert to CNF
    negated_formula = belief_base.convert_to_cnf(negated_formula)
    print(f"Negated formula: {negated_formula}")
    return negated_formula


def resolve(clause1, clause2, belief_base):
    """Check complementary literals and return resolvent."""
    clause1 = belief_base.convert_to_cnf(clause1)
    clause2 = belief_base.convert_to_cnf(clause2)
    
    print(f"Resolving clauses: {clause1} and {clause2}")

    literals1 = set(literal.strip() for literal in clause1.split("|"))
    literals2 = set(literal.strip() for literal in clause2.split("|"))

    print(f"Literals in clause1: {literals1}, clause2: {literals2}")

    # Check for complementary literals
    for literal in literals1:
        print(f"Checking literal: {literal}")
        if literal.startswith('~'):
            # If literal is negated, check for positive form in literals2
            positive_form = literal[1:]
            if positive_form in literals2:
                resolvent = (literals1 - {literal}) | (literals2 - {positive_form})
                return " | ".join(resolvent) if resolvent else ""
        else:
            # If literal is positive, check for negated form in literals2
            if f"~{literal}" in literals2:
                resolvent = (literals1 - {literal}) | (literals2 - {f"~{literal}"})
                return " | ".join(resolvent) if resolvent else ""
    
    return None  # No resolvent found

def resolution(belief_base, negated_formula):
    """Apply resolution to the belief base and negated formula.
    Returns True if the negated formula is entailed (contradiction found), False otherwise."""

    # Convert initial clauses to a set to avoid duplicates
    clauses = set(belief[0] for belief in belief_base.beliefs)
    clauses.add(negated_formula)
    
    new_clauses = set() 

    # Iterate until no new clauses can be generated
    while True:
        # Store original size to check if new clauses were added
        original_size = len(clauses)
        
        # Try to resolve all pairs of clauses
        all_clauses = list(clauses)  # Convert to list for indexing
        for i in range(len(all_clauses)):
            for j in range(i + 1, len(all_clauses)):
                resolvent = resolve(all_clauses[i], all_clauses[j], belief_base)
                if resolvent is not None:
                    # Empty resolvent indicates a contradiction
                    if resolvent == "":
                        print("Empty clause (contradiction) found!")
                        return True  # Entailment found via contradiction
                    new_clauses.add(resolvent)
        
        # Add new clauses to the set
        clauses.update(new_clauses)
        
        # If no new clauses were added, stop
        if len(clauses) == original_size:
            print("No new clauses generated, resolution complete.")
            break

    # If no contradiction is found, the negated formula is not entailed
    print("No contradiction found.")
    return False


# Step 1: Negate the formula
# Step 2: Convert all formulas to CNF
# Step 3: Combine the negated formula with the belief base
# Step 4: Resolve pairs of clauses
