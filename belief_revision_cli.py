import cmd
import re
from belief_base import BeliefBase
from resolution import negate_formula, resolution


class BeliefRevisionCLI(cmd.Cmd):
    """Interactive CLI for Belief Revision Agent using cmd module."""
    intro = "Welcome to the Belief Revision Agent. Type help or ? to list commands.\n"
    prompt = "> "

    def __init__(self):
        super().__init__()
        self.belief_base = BeliefBase()

    def do_expand(self, arg):
        """expand <formula> [<entrenchment>]: Add a belief to the belief base (expansion)."""
        formula, entrenchment = self._parse_formula_arg(arg)
        try:
            if "<<" in formula and ">>" in formula:
                parts = formula.split("<<>>")
                if len(parts) == 2:
                    left = parts[0].strip()
                    right = parts[1].strip()
                    formula = f"({left} >> {right}) & ({right} >> {left})"
            cnf = self.belief_base.convert_to_cnf(formula)
            self.belief_base.expand(cnf, entrenchment)
            print(
                f"Expanded belief base with: {cnf} (entrenchment: {entrenchment})")
        except Exception as e:
            print(f"Error: {e}")

    def do_revise(self, arg):
        """revise <formula> [<entrenchment>]: Revise belief base using contraction and expansion."""
        formula, entrenchment = self._parse_formula_arg(arg)
        try:
            if "<<" in formula and ">>" in formula:
                parts = formula.split("<<>>")
                if len(parts) == 2:
                    left = parts[0].strip()
                    right = parts[1].strip()
                    formula = f"({left} >> {right}) & ({right} >> {left})"
            cnf = self.belief_base.convert_to_cnf(formula)
            self.belief_base.revise(cnf, entrenchment)
            print(
                f"Revised belief base with: {cnf} (entrenchment: {entrenchment})")
        except Exception as e:
            print(f"Error during revision: {e}")

    def do_entails(self, arg):
        """entails <formula>: Check if belief base logically entails the given formula."""
        formula = arg.strip()
        if "<<" in formula and ">>" in formula:
            parts = formula.split("<<>>")
            if len(parts) == 2:
                left = parts[0].strip()
                right = parts[1].strip()
                formula = f"({left} >> {right}) & ({right} >> {left})"
        try:
            negated = negate_formula(formula, self.belief_base)
            if resolution(self.belief_base, negated):
                print(f"The belief base entails: {formula}")
            else:
                print(f"The belief base does not entail: {formula}")
        except Exception as e:
            print(f"Error during entailment check: {e}")

    def do_remove(self, arg):
        """remove <formula>: Remove a belief from the belief base."""
        formula = arg.strip()
        try:
            self.belief_base.remove_belief(formula)
            print(f"Removed belief: {formula}")
        except ValueError as e:
            print(f"Error: {e}")

    def do_show(self, _):
        """show: Display all current beliefs in the belief base."""
        if not self.belief_base.beliefs:
            print("Belief base is empty.")
        else:
            print("Current Belief Base:")
            for i, (belief, entrenchment) in enumerate(self.belief_base.beliefs):
                print(f"  {i+1:2}. {belief:<30} [entrenchment: {entrenchment}]")

    def do_exit(self, _):
        """exit: Exit the CLI."""
        print("Goodbye!")
        return True

    def do_EOF(self, _):
        """Handles Ctrl+D for exit."""
        print()
        return self.do_exit(_)

    def _parse_formula_arg(self, arg):
        """Helper: Parses 'formula [entrenchment]' and returns (formula, entrenchment)."""
        match = re.match(r"(.+?)(?:\s+(\d+))?$", arg.strip())
        if not match:
            raise ValueError("Invalid input format.")
        formula, entrenchment = match.groups()
        entrenchment = int(entrenchment) if entrenchment else 50
        return formula.strip(), entrenchment

    def do_help(self, arg):
        """Show list of available commands or help for a specific command."""
        commands = {
            "expand": "expand <formula> [<entrenchment>] - Add a belief to the base",
            "revise": "revise <formula> [<entrenchment>] - Revise base via contraction + expansion",
            "entails": "entails <formula> - Check if belief base entails the formula",
            "remove": "remove <formula> - Remove a belief from the base",
            "show": "show - Display current belief base",
            "exit": "exit - Exit the CLI",
            "help": "help [command] - Show help message",
        }

        if arg:
            cmd_help = commands.get(arg.strip())
            if cmd_help:
                print(cmd_help)
            else:
                print(f"No help available for '{arg.strip()}'")
        else:
            print("Available commands:")
            for name, desc in commands.items():
                print(f"  {desc}")
