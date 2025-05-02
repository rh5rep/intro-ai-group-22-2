from belief_base import BeliefBase
from resolution import negate_formula, resolution

def main():
    """Main function to interact with the belief base using a simple CLI."""
    belief_base = BeliefBase()
    
    print("Belief Revision Agent")
    print("====================")
    print("Commands:")
    print("  add <formula> [<entrenchment>] - Add a belief with optional entrenchment (default 50)")
    print("  entails <formula> - Check if belief base entails the formula")
    print("  remove <formula> - Remove a belief")
    print("  show - Display current belief base")
    print("  help - Show this help message")
    print("  exit - Exit the program")
    print("\nFormula syntax:")
    print("  p, q, r - Atomic propositions")
    print("  ~p - Negation")
    print("  p & q - Conjunction (AND)")
    print("  p | q - Disjunction (OR)")
    print("  p >> q - Implication (IF-THEN)")
    print("  p <<>> q - Equivalence (IFF)")
    
    while True:
        try:
            command = input("\n> ").strip()
            
            if not command:
                continue
                
            if command.lower() == "exit":
                print("Goodbye!")
                break
                
            if command.lower() == "help":
                print("Commands:")
                print("  add <formula> [<entrenchment>] - Add a belief with optional entrenchment (default 50)")
                print("  entails <formula> - Check if belief base entails the formula")
                print("  remove <formula> - Remove a belief")
                print("  show - Display current belief base")
                print("  help - Show this help message")
                print("  exit - Exit the program")
                continue
                
            if command.lower() == "show":
                if not belief_base.beliefs:
                    print("Belief base is empty.")
                else:
                    print("Current Belief Base:")
                    for i, (belief, entrenchment) in enumerate(belief_base.beliefs):
                        print(f"  {i+1}. {belief} (entrenchment: {entrenchment})")
                continue
                
            if command.lower().startswith("add "):
                parts = command[4:].strip().split()
                if len(parts) >= 2 and parts[-1].isdigit():
                    formula = " ".join(parts[:-1])
                    entrenchment = int(parts[-1])
                else:
                    formula = " ".join(parts)
                    entrenchment = 50
                    
                try:
                    # Convert to CNF for consistency
                    cnf_formula = belief_base.convert_to_cnf(formula)
                    belief_base.add_belief(cnf_formula, entrenchment)
                    print(f"Added belief: {cnf_formula} (entrenchment: {entrenchment})")
                except ValueError as e:
                    print(f"Error: {e}")
                continue
                
            if command.lower().startswith("remove "):
                formula = command[7:].strip()
                try:
                    belief_base.remove_belief(formula)
                    print(f"Removed belief: {formula}")
                except ValueError as e:
                    print(f"Error: {e}")
                continue
                
            if command.lower().startswith("entails "):
                formula = command[8:].strip()
                try:
                    # Negate the formula for resolution
                    negated_formula = negate_formula(formula, belief_base)
                    
                    # Apply resolution
                    result = resolution(belief_base, negated_formula)
                    
                    if result:
                        print(f"The belief base entails: {formula}")
                    else:
                        print(f"The belief base does not entail: {formula}")
                except Exception as e:
                    print(f"Error during entailment check: {e}")
                continue
                
            print(f"Unknown command: {command}")
            
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
