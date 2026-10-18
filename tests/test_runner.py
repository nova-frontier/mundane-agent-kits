import unittest
from bounded_runner import run


class RunnerTests(unittest.TestCase):
    def test_fallback_respects_total_budget(self):
        r = run(
            [{"status": "timeout"}] * 50,
            3,
            {"status": "ok", "payload": {"label": "example"}},
        )
        self.assertEqual(r["attempts"], 3)
        self.assertEqual(r["trace"][-1]["source"], "fallback")
        self.assertEqual(r["status"], "accepted")
        self.assertIsNone(r["reported_cost_total"])

    def test_failure_does_not_invent_a_result(self):
        r = run([{"status": "error"}] * 10, 2)
        self.assertEqual(r["attempts"], 2)
        self.assertIsNone(r["result"])
        self.assertEqual(r["status"], "needs_review")

    def test_invalid_payload_preserved(self):
        r = run([{"status": "ok", "payload": {}}])
        self.assertEqual(r["trace"][0]["status"], "invalid")

    def test_cost_and_early_stop(self):
        r = run(
            [
                {"status": "ok", "payload": {"a": 1}, "reported_cost": 0.2},
                {"status": "error", "reported_cost": 10},
            ]
        )
        self.assertEqual(r["attempts"], 1)
        self.assertAlmostEqual(r["reported_cost_total"], 0.2)

    def test_bad_input(self):
        with self.assertRaises(ValueError):
            run([], 0)


if __name__ == "__main__":
    unittest.main()
