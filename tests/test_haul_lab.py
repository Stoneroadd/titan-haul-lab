import unittest

from haul_lab import simulate, summarize


class HaulLabTest(unittest.TestCase):
    def test_reproducible_paired_scenarios(self):
        rows = simulate(42, 10, 0.3)
        self.assertEqual(rows, simulate(42, 10, 0.3))
        self.assertEqual(len(rows), 10)
        self.assertTrue(all(row["alternative_cycle_min"] <= row["baseline_cycle_min"] for row in rows))

    def test_no_change_when_queue_reduction_is_zero(self):
        rows = simulate(1, 5, 0)
        summary = summarize(rows, 0, 1)
        self.assertEqual(summary["mean_difference"], 0)

    def test_invalid_inputs(self):
        for cycles, reduction in [(0, 0.3), (10, -0.1), (10, 1.1)]:
            with self.assertRaises(ValueError):
                simulate(1, cycles, reduction)


if __name__ == "__main__":
    unittest.main()
