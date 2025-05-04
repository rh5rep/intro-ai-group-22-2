import unittest
from belief_base import BeliefBase


class TestBeliefBase(unittest.TestCase):

    def setUp(self):
        self.base = BeliefBase()

    def test_basic_expansion(self):
        self.base.expand("p", 10)
        self.base.expand("q", 20)
        self.assertEqual(len(self.base.beliefs), 2)

    def test_cnf_conversion(self):
        cnf = self.base.convert_to_cnf("p >> q")
        self.assertEqual(cnf, "q | ~p")

        cnf_equiv = self.base.convert_to_cnf("p <<>> q")
        self.assertIn("|", cnf_equiv)  # It expands to conjunction of implications

    def test_entrenchment(self):
        self.base.expand("r", 35)
        self.assertEqual(self.base.get_entrenchment("r"), 35)

    def test_remove_existing_belief(self):
        self.base.expand("s", 15)
        self.base.remove_belief("s")
        self.assertEqual(len(self.base.beliefs), 0)

    def test_remove_nonexistent_belief(self):
        with self.assertRaises(ValueError):
            self.base.remove_belief("not_in_base")

    def test_update_belief(self):
        self.base.expand("a", 10)
        self.base.update_belief("a", "~a", 50)
        self.assertEqual(len(self.base.beliefs), 1)
        self.assertEqual(self.base.beliefs[0][0], "~a")

    def test_get_entrenchment_nonexistent(self):
        with self.assertRaises(ValueError):
            self.base.get_entrenchment("x")

    def test_add_contradictory_beliefs(self):
        self.base.expand("p", 20)
        self.base.expand("~p", 30)
        self.assertEqual(len(self.base.beliefs), 2)
        # both exist even if contradictory (expansion does not check consistency)

    def test_complex_formula(self):
        formula = "(p & q) >> (r | ~s)"
        cnf = self.base.convert_to_cnf(formula)
        self.assertTrue(isinstance(cnf, str))
        self.assertIn("|", cnf)

    def test_nested_equivalence(self):
        formula = "((p & q) <<>> (r | s))"
        cnf = self.base.convert_to_cnf(formula)
        self.assertTrue(cnf)
        self.assertIn("|", cnf)
        self.assertIn("&", cnf)

    def test_contract_simple(self):
        self.base.expand("p", 20)
        self.base.expand("p >> q", 40)
        self.base.expand("q", 60)

        # 'q' should be entailed → after contraction, it shouldn't be anymore
        self.base.contract("q")
        remaining = [b[0] for b in self.base.beliefs]
        self.assertNotIn("q", remaining)
        self.assertFalse("p" in remaining and "p >> q" in remaining)  # At least one should be gone

    def test_contract_non_entailed(self):
        self.base.expand("p", 30)
        self.base.contract("z")  # 'z' is not entailed; nothing should be removed
        self.assertEqual(len(self.base.beliefs), 1)

    def test_revision_adds_and_removes(self):
        self.base.expand("p", 30)
        self.base.expand("p >> q", 50)

        # Belief base now entails 'q'. If we revise with '~q', it should remove something.
        self.base.revise("~q", 40)

        beliefs = [b[0] for b in self.base.beliefs]
        self.assertIn("~q", beliefs)
        self.assertNotIn("q", beliefs)  # Ensure contradiction resolved



if __name__ == "__main__":
    unittest.main()
