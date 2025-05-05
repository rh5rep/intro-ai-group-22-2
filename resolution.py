import sympy
from sympy.logic.boolalg import to_cnf

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

def get_literals(clause):
    """Extract literals from a clause."""
    if isinstance(clause, sympy.Symbol):
        return {clause}
    elif isinstance(clause, sympy.Not) and isinstance(clause.args[0], sympy.Symbol):
        return {clause}
    elif isinstance(clause, sympy.Or):
        literals = set()
        for arg in clause.args:
            literals.update(get_literals(arg))
        return literals
    elif isinstance(clause, sympy.And):
        # For conjunctions, each conjunct should be treated as a separate clause
        # We don't combine AND clauses in resolution
        return {clause}  # Return the entire conjunction as a single unit
    return {clause}

def resolve(clause1, clause2, belief_base):
    """Check complementary literals and return resolvent."""
    # Convert to SymPy CNF objects
    clause1_expr = to_cnf(clause1, simplify=True)
    clause2_expr = to_cnf(clause2, simplify=True)
    
    print(f"Clause1: {clause1_expr}")
    print(f"Clause2: {clause2_expr}")
    
    print(f"Resolving clauses: {clause1_expr} and {clause2_expr}")
    
    # Handle AND expressions - in CNF, we treat each conjunct separately
    if isinstance(clause1_expr, sympy.And):
        for arg in clause1_expr.args:
            result = resolve(arg, clause2_expr, belief_base)
            if result == "":  # Empty clause found
                return ""
            if result is not None:
                return result
        return None
    
    if isinstance(clause2_expr, sympy.And):
        for arg in clause2_expr.args:
            result = resolve(clause1_expr, arg, belief_base)
            if result == "":  # Empty clause found
                return ""
            if result is not None:
                return result
        return None
    
    # Now we're dealing with disjunctions (OR) or literals
    literals1 = get_literals(clause1_expr)
    literals2 = get_literals(clause2_expr)
    
    print(f"Literals in clause1: {literals1}, clause2: {literals2}")
    
    # Check for complementary literals
    for literal in literals1:
        print(f"Checking literal: {literal}")
        if isinstance(literal, sympy.Not) and isinstance(literal.args[0], sympy.Symbol):
            # If literal is negated, check for positive form in literals2
            positive_form = literal.args[0]
            for lit2 in literals2:
                if lit2 == positive_form:
                    # Complementary literals found, compute resolvent
                    resolvent_literals1 = literals1 - {literal}
                    resolvent_literals2 = literals2 - {lit2}
                    resolvent = resolvent_literals1.union(resolvent_literals2)
                    
                    if not resolvent:
                        return ""  # Empty clause - contradiction found
                    
                    if len(resolvent) == 1:
                        return next(iter(resolvent))
                    else:
                        return sympy.Or(*resolvent)
        elif isinstance(literal, sympy.Symbol):
            # If literal is positive, check for negated form in literals2
            for lit2 in literals2:
                if isinstance(lit2, sympy.Not) and lit2.args[0] == literal:
                    # Complementary literals found, compute resolvent
                    resolvent_literals1 = literals1 - {literal}
                    resolvent_literals2 = literals2 - {lit2}
                    resolvent = resolvent_literals1.union(resolvent_literals2)
                    
                    if not resolvent:
                        return ""  # Empty clause - contradiction found
                    
                    if len(resolvent) == 1:
                        return next(iter(resolvent))
                    else:
                        return sympy.Or(*resolvent)
    
    # No complementary literals found
    return None
def resolution(belief_base, negated_formula):
    """Apply resolution to the belief base and negated formula.
    Returns True if the negated formula is entailed (contradiction found), False otherwise."""

    try:
        # Convert initial clauses to a set to avoid duplicates
        clauses = set(belief[0] for belief in belief_base.beliefs)
        clauses.add(negated_formula)
        
        # Iterate until no new clauses can be generated
        while True:
            new_clauses = set()
            
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
            original_size = len(clauses)
            clauses.update(new_clauses)
            
            # If no new clauses were added, stop
            if len(clauses) == original_size:
                print("No new clauses generated, resolution complete.")
                break

        # If no contradiction is found, the negated formula is not entailed
        print("No contradiction found.")
        return False
    except Exception as e:
        print(f"Error during entailment check: {str(e)}")
        return False
