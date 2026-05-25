import unittest

from scripts.build_mem0_candidate_queue import blocker_for, queue_priority


class BuildMem0CandidateQueueTests(unittest.TestCase):
    def test_benchmarked_status_gets_promoted_queue_priority(self) -> None:
        candidate = {
            "id": "BAAI/bge-m3",
            "role": "embedder",
            "status": "benchmarked-cpu-mps-not-promoted",
        }

        self.assertEqual(queue_priority(candidate)[0], 2)
        self.assertEqual(blocker_for(candidate), "benchmarked but not promoted; keep separate collection or artifact")


if __name__ == "__main__":
    unittest.main()
