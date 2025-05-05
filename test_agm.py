import unittest
from belief_base import BeliefBase
from resolution import negate_formula, resolution


def is_consistent(belief_base):
    """Check if belief base does not entail False (i.e., is consistent)."""
    return not resolution(belief_base, "False")


class TestAGMPostulates(unittest.TestCase):
    """Test the AGM postulates for belief revision."""

    def test_success(self):
        """Success Postulate: After revision with φ, φ is in the belief base."""
        bb = BeliefBase()
        bb.expand("p", 30)
        bb.revise("q", 50)
        beliefs = [b[0] for b in bb.beliefs]
        self.assertIn("q", beliefs)

    def test_inclusion(self):
        """Inclusion Postulate: Original beliefs should be retained if they don't contradict φ."""
        bb = BeliefBase()
        bb.expand("p", 30)
        bb.expand("r", 30)
        bb.revise("q", 50)
        beliefs = [b[0] for b in bb.beliefs]
        self.assertIn("p", beliefs)
        self.assertIn("r", beliefs)

    def test_vacuity(self):
        """Vacuity Postulate: If ¬φ not in base, revise behaves like expand."""
        bb1 = BeliefBase()
        bb2 = BeliefBase()
        bb1.expand("p", 30)
        bb2.expand("p", 30)

        bb1.expand("q", 50)
        bb2.revise("q", 50)

        beliefs1 = set(b[0] for b in bb1.beliefs)
        beliefs2 = set(b[0] for b in bb2.beliefs)
        self.assertEqual(beliefs1, beliefs2)

    def test_consistency(self):
        """Consistency Postulate: Revising with consistent φ should not lead to contradiction."""
        bb = BeliefBase()
        bb.expand("p", 30)
        bb.revise("q", 40)
        self.assertTrue(is_consistent(bb))

    def test_extensionality(self):
        """Extensionality Postulate: Revising with φ or logically equivalent ψ gives same result."""
        bb1 = BeliefBase()
        bb2 = BeliefBase()

        bb1.expand("p", 30)
        bb2.expand("p", 30)

        bb1.revise("q", 50)
        bb2.revise("~~q", 50)

        b1 = set(b[0] for b in bb1.beliefs)
        b2 = set(b[0] for b in bb2.beliefs)
        self.assertEqual(b1, b2)


if __name__ == "__main__":
    unittest.main()
