from belief_base import BeliefBase
from resolution import negate_formula, resolution


def line(title=""):
    print("\n" + "=" * 50)
    if title:
        print(title)
        print("=" * 50)


def demonstrate_task1():
    line("TASK 1: Belief Base Representation")

    bb = BeliefBase()
    bb.expand("p", entrenchment=10)
    bb.expand("q", entrenchment=80)
    bb.expand("p >> q", entrenchment=60)

    print("Beliefs in base (after expansion):")
    for belief, ent in bb.beliefs:
        print(f"  - {belief} (entrenchment: {ent})")

    print("Updating belief 'q' to '~q'")
    bb.update_belief("q", "~q", entrenchment=40)

    print("Removing belief '~q'")
    bb.remove_belief("~q")

    print("Beliefs after updates:")
    for belief, ent in bb.beliefs:
        print(f"  - {belief} (entrenchment: {ent})")

    entrenchment = bb.get_entrenchment("p")
    print(f"Entrenchment of 'p': {entrenchment}")

    cnf = bb.convert_to_cnf("p >> r")
    print(f"CNF of 'p >> r': {cnf}")


def demonstrate_task2():
    line("TASK 2: Logical Entailment (Resolution)")

    bb = BeliefBase()
    bb.expand("p")
    bb.expand("p >> q")

    query = "q"
    print(f"Checking entailment: does base entail '{query}'?")

    negated = negate_formula(query, bb)
    result = resolution(bb, negated)

    print("Result:", "Entailed ✅" if result else "Not entailed ❌")


def demonstrate_task3():
    line("TASK 3: Contraction")

    bb = BeliefBase()
    bb.expand("p", entrenchment=20)
    bb.expand("p >> q", entrenchment=40)
    bb.expand("q", entrenchment=60)

    print("Initial Beliefs:")
    for b, e in bb.beliefs:
        print(f"  - {b} (entrenchment: {e})")

    print("Contracting 'q' (removes enough beliefs to break entailment)")
    bb.contract("q")

    print("Beliefs after contraction:")
    for b, e in bb.beliefs:
        print(f"  - {b} (entrenchment: {e})")


def demonstrate_task4():
    line("TASK 4: Expansion")

    bb = BeliefBase()
    print("Expanding belief base with contradictory beliefs:")
    bb.expand("p")
    bb.expand("~p")

    print("Beliefs now:")
    for b, e in bb.beliefs:
        print(f"  - {b} (entrenchment: {e})")

    print("Note: Expansion does not check for consistency.")


def demonstrate_revision():
    line("FULL REVISION (CONTRACTION + EXPANSION)")

    bb = BeliefBase()
    bb.expand("p", entrenchment=30)
    bb.expand("p >> q", entrenchment=50)

    print("Initial beliefs:")
    for b, e in bb.beliefs:
        print(f"  - {b} (entrenchment: {e})")

    print("Revising with '~q' (should contract q-supporting beliefs, then add ~q)")
    bb.revise("~q", entrenchment=40)

    print("Beliefs after revision:")
    for b, e in bb.beliefs:
        print(f"  - {b} (entrenchment: {e})")


if __name__ == "__main__":
    demonstrate_task1()
    demonstrate_task2()
    demonstrate_task3()
    demonstrate_task4()
    demonstrate_revision()
