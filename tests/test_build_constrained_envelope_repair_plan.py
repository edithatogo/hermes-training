from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.build_constrained_envelope_repair_plan import build_plan, classify_row


class BuildConstrainedEnvelopeRepairPlanTests(unittest.TestCase):
    def test_classify_exact_calls_with_extra_text(self) -> None:
        row = {
            "pass": False,
            "reason": "tool calls matched but extra text was present",
            "tool_calls": [{"name": "lookup_customer", "arguments": {"customer_id": "CUST-1007"}}],
            "parse_errors": [],
            "no_extra_text_ok": False,
        }

        self.assertEqual(classify_row(row), "matched_tool_calls_extra_text")

    def test_build_plan_ranks_extra_text_candidate_first(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            strong = root / "strong"
            weak = root / "weak"
            strong.mkdir()
            weak.mkdir()
            (strong / "summary.json").write_text("{}", encoding="utf-8")
            (strong / "responses.jsonl").write_text("{}\n", encoding="utf-8")
            (strong / "results.jsonl").write_text(
                json.dumps(
                    {
                        "id": "bfcl-simple",
                        "category": "tool_call",
                        "pass": False,
                        "reason": "tool calls matched but extra text was present",
                        "tool_calls": [{"name": "lookup_customer", "arguments": {}}],
                        "parse_errors": [],
                        "no_extra_text_ok": False,
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            (weak / "summary.json").write_text("{}", encoding="utf-8")
            (weak / "responses.jsonl").write_text("{}\n", encoding="utf-8")
            (weak / "results.jsonl").write_text(
                json.dumps(
                    {
                        "id": "bfcl-simple",
                        "category": "tool_call",
                        "pass": False,
                        "reason": "tool calls did not exactly match",
                        "tool_calls": [],
                        "parse_errors": [],
                        "no_extra_text_ok": False,
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            report = root / "results.json"
            report.write_text(
                json.dumps(
                    {
                        "results": [
                            {
                                "candidate": "Nanbeige/Nanbeige4.1-3B",
                                "variant": "strict",
                                "runner": "local",
                                "status": "completed-no-promotion",
                                "pass_rate": 0.0,
                                "passed": 0,
                                "cases": 3,
                                "result_report": "reports/benchmark/local-pilots/nanbeige41-3b-strict-suffix-copy-exact-repair-20260614.md",
                                "source_summary": str(strong / "summary.json"),
                            },
                            {
                                "candidate": "Other/Model",
                                "variant": "strict",
                                "runner": "local",
                                "status": "completed-no-promotion",
                                "pass_rate": 0.333,
                                "passed": 1,
                                "cases": 3,
                                "result_report": "reports/benchmark/local-pilots/qwen35-2b-qwen-no-think-prefill-repair-20260614.md",
                                "source_summary": str(weak / "summary.json"),
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )

            plan = build_plan(report)

        self.assertEqual(plan["candidates"][0]["candidate"], "Nanbeige/Nanbeige4.1-3B")
        self.assertEqual(plan["candidates"][0]["priority"], "high")
        self.assertIn("--require-no-extra-tool-text", plan["candidates"][0]["diagnostic_command"])

    def test_nanbeige_remains_top_when_later_high_priority_has_higher_pass_rate(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            nanbeige = root / "nanbeige"
            later = root / "later"
            nanbeige.mkdir()
            later.mkdir()
            for source in (nanbeige, later):
                (source / "summary.json").write_text("{}", encoding="utf-8")
                (source / "responses.jsonl").write_text("{}\n", encoding="utf-8")
            (nanbeige / "results.jsonl").write_text(
                json.dumps(
                    {
                        "id": "bfcl-simple",
                        "category": "tool_call",
                        "pass": False,
                        "reason": "tool calls matched but extra text was present",
                        "tool_calls": [{"name": "lookup_customer", "arguments": {}}],
                        "parse_errors": [],
                        "no_extra_text_ok": False,
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            (later / "results.jsonl").write_text(
                "\n".join(
                    json.dumps(
                        {
                            "id": f"bfcl-{index}",
                            "category": "tool_call",
                            "pass": False,
                            "reason": "tool calls matched but extra text was present",
                            "tool_calls": [{"name": "lookup_customer", "arguments": {}}],
                            "parse_errors": [],
                            "no_extra_text_ok": False,
                        }
                    )
                    for index in range(2)
                )
                + "\n",
                encoding="utf-8",
            )
            report = root / "results.json"
            report.write_text(
                json.dumps(
                    {
                        "results": [
                            {
                                "candidate": "Nanbeige/Nanbeige4.1-3B",
                                "variant": "strict",
                                "runner": "local",
                                "status": "completed-no-promotion",
                                "pass_rate": 0.0,
                                "passed": 0,
                                "cases": 3,
                                "result_report": "reports/benchmark/local-pilots/nanbeige41-3b-strict-suffix-copy-exact-repair-20260614.md",
                                "source_summary": str(nanbeige / "summary.json"),
                            },
                            {
                                "candidate": "Later/HighPriority",
                                "variant": "strict",
                                "runner": "endpoint",
                                "status": "completed-no-promotion",
                                "pass_rate": 0.333,
                                "passed": 1,
                                "cases": 3,
                                "result_report": "reports/benchmark/endpoint-pilots/maniaclabs-qwen36-35b-a3b-2bit-strict-suffix-copy-exact-repair-20260614.md",
                                "source_summary": str(later / "summary.json"),
                            },
                        ]
                    }
                ),
                encoding="utf-8",
            )

            plan = build_plan(report)

        self.assertEqual(plan["candidates"][0]["candidate"], "Nanbeige/Nanbeige4.1-3B")
        self.assertEqual(plan["candidates"][1]["candidate"], "Later/HighPriority")

    def test_endpoint_runner_gets_endpoint_diagnostic_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "endpoint"
            source.mkdir()
            (source / "summary.json").write_text("{}", encoding="utf-8")
            (source / "responses.jsonl").write_text("{}\n", encoding="utf-8")
            (source / "results.jsonl").write_text(
                json.dumps(
                    {
                        "id": "bfcl-simple",
                        "category": "tool_call",
                        "pass": False,
                        "reason": "tool calls did not exactly match",
                        "tool_calls": [],
                        "parse_errors": [],
                        "no_extra_text_ok": False,
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            report = root / "results.json"
            report.write_text(
                json.dumps(
                    {
                        "results": [
                            {
                                "candidate": "LGAI-EXAONE/EXAONE-4.0-1.2B",
                                "variant": "strict",
                                "runner": "endpoint",
                                "status": "completed-no-promotion",
                                "pass_rate": 0.0,
                                "passed": 0,
                                "cases": 3,
                                "result_report": "reports/benchmark/endpoint-pilots/exaone4-12b-strict-suffix-copy-exact-repair-20260614.md",
                                "source_summary": str(source / "summary.json"),
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )

            plan = build_plan(report)

        command = plan["candidates"][0]["diagnostic_command"]
        self.assertEqual(plan["candidates"][0]["best_runner"], "endpoint")
        self.assertIn("scripts/run_endpoint_pilot_benchmark.py", command)
        self.assertIn("--model 'LGAI-EXAONE/EXAONE-4.0-1.2B'", command)
        self.assertIn("--base-url 'http://127.0.0.1:<port>/v1'", command)
        self.assertNotIn("scripts/run_local_pilot_benchmark.py", command)


if __name__ == "__main__":
    unittest.main()
