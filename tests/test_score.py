"""合成数据验证计算、证据边界与命令行错误；不模拟模型能力判断。"""

import copy
import json
import math
import os
import subprocess
import sys
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

from scripts.score import calculate_score, load_rubrics, parse_json


ROOT = Path(__file__).resolve().parents[1]
RUBRICS = load_rubrics()
USE_DEFAULT = object()


def make_input(interview_type="technical", level="Meets"):
    ids = [d["id"] for d in RUBRICS["interview_types"][interview_type]["dimensions"]]
    # 每个维度单独给出合成回答及依据，不依赖真实用户资料。
    return {
        "interview_type": interview_type,
        "critical_dimensions": [ids[0]],
        "answers": [
            {"id": f"A{i}", "question_id": f"Q{i}", "status": "answered",
             "text": f"合成回答 {i}：描述一次实现选择和验证过程。", "record_kind": "raw",
             "feedback_intervened": False}
            for i, _ in enumerate(ids, 1)
        ],
        "ratings": {
            key: {"level": level, "evidence_status": "sufficient",
                  "evidence": [{"answer_id": f"A{i}", "reason": f"合成依据：该回答支持维度 {key} 的观察点。"}]}
            for i, key in enumerate(ids, 1)
        },
    }


def mark_na(data, key, status="not_assessed"):
    data["ratings"][key] = {"level": "N/A", "evidence_status": status, "evidence": []}


class ScoreTests(unittest.TestCase):
    def setUp(self):
        self.data = make_input()
        self.ids = list(self.data["ratings"])

    def score(self, data=USE_DEFAULT):
        return calculate_score(self.data if data is USE_DEFAULT else data, RUBRICS)

    def test_source_weights_match_design(self):
        expected = {"technical": [25, 20, 20, 15, 15, 5],
                    "comprehensive": [20, 20, 20, 15, 15, 10],
                    "hr": [15, 20, 25, 15, 10, 15]}
        for kind, weights in expected.items():
            self.assertEqual([d["weight"] for d in RUBRICS["interview_types"][kind]["dimensions"]], weights)

    def test_uniform_levels_for_all_types(self):
        for kind in RUBRICS["interview_types"]:
            for level, expected in [("Meets", 75), ("Strong", 100), ("Below", 50), ("Weak", 25)]:
                with self.subTest(kind=kind, level=level):
                    result = self.score(make_input(kind, level))
                    self.assertEqual(result["score"], expected)
                    self.assertEqual(result["coverage_percent"], 100)

    def test_mixed_weighted_score(self):
        levels = ["Strong", "Meets", "Below", "Weak", "Strong", "Below"]
        for key, level in zip(self.ids, levels):
            self.data["ratings"][key]["level"] = level
        self.assertEqual(self.score()["score"], 71.25)

    def test_partial_na_renormalizes_and_reports_original_coverage(self):
        for key in self.ids[2:]:
            mark_na(self.data, key)
        self.data["ratings"][self.ids[0]]["level"] = "Strong"
        result = self.score()
        self.assertEqual(result["score"], 88.89)
        self.assertEqual(result["coverage_percent"], 45)

    def test_all_na_returns_null(self):
        for key in self.ids:
            mark_na(self.data, key)
        result = self.score()
        self.assertIsNone(result["score"])
        self.assertEqual(result["coverage_percent"], 0)
        self.assertEqual(result["judgment_status"], "reserved")
        self.assertIn("证据不足", " ".join(result["notes"]))

    def test_missing_critical_evidence_reserves_even_with_perfect_score(self):
        self.data = make_input(level="Strong")
        mark_na(self.data, self.ids[0], "insufficient")
        result = self.score()
        self.assertEqual(result["score"], 100)
        self.assertEqual(result["judgment_status"], "reserved")
        self.assertEqual(result["unassessed_critical_dimensions"], [self.ids[0]])

    def test_complete_evidence_still_requires_model_judgment(self):
        self.assertEqual(self.score()["judgment_status"], "requires_model_judgment")

    def test_undefined_critical_abilities_reserves(self):
        self.data["critical_dimensions"] = []
        self.assertEqual(self.score()["judgment_status"], "reserved")

    def test_custom_weights_and_decimal_precision(self):
        self.data["weights"] = dict(zip(self.ids, [Decimal("33.3"), Decimal("16.7"), 20, 15, 10, 5]))
        self.data["ratings"][self.ids[0]]["level"] = "Strong"
        self.assertEqual(self.score()["score"], 83.33)

    def test_zero_weight_is_allowed_but_does_not_increase_coverage(self):
        self.data["weights"] = dict(zip(self.ids, [100, 0, 0, 0, 0, 0]))
        mark_na(self.data, self.ids[0])
        result = self.score()
        self.assertIsNone(result["score"])
        self.assertEqual(result["coverage_percent"], 0)

    def test_illegal_weight_values(self):
        for value in [-1, 101, True, "25", None, [], {}, math.nan, math.inf, -math.inf, Decimal("NaN")]:
            with self.subTest(value=value):
                data = make_input()
                data["weights"] = {d["id"]: d["weight"] for d in RUBRICS["interview_types"]["technical"]["dimensions"]}
                data["weights"][self.ids[0]] = value
                with self.assertRaises(ValueError):
                    self.score(data)

    def test_wrong_weight_sum(self):
        self.data["weights"] = dict.fromkeys(self.ids, 10)
        with self.assertRaisesRegex(ValueError, "总和必须为 100"):
            self.score()

    def test_missing_or_extra_weights(self):
        for weights in [{}, dict.fromkeys(self.ids + ["unknown"], 10)]:
            self.data["weights"] = weights
            with self.assertRaises(ValueError):
                self.score()

    def test_invalid_levels(self):
        for value in ["Excellent", "meets", 3, None, [], {}]:
            self.data["ratings"][self.ids[0]]["level"] = value
            with self.assertRaisesRegex(ValueError, "非法等级"):
                self.score()

    def test_rated_dimension_needs_sufficient_evidence(self):
        for status in ["not_assessed", "insufficient"]:
            self.data["ratings"][self.ids[0]]["evidence_status"] = status
            with self.assertRaises(ValueError):
                self.score()

    def test_na_cannot_claim_sufficient_evidence(self):
        self.data["ratings"][self.ids[0]]["level"] = "N/A"
        with self.assertRaises(ValueError):
            self.score()

    def test_rated_dimension_needs_nonempty_evidence(self):
        self.data["ratings"][self.ids[0]]["evidence"] = []
        with self.assertRaisesRegex(ValueError, "评级必须有回答证据"):
            self.score()

    def test_unassessed_dimension_cannot_reference_answer(self):
        self.data["ratings"][self.ids[0]].update(level="N/A", evidence_status="not_assessed")
        with self.assertRaises(ValueError):
            self.score()

    def test_insufficient_evidence_may_retain_answer_without_scoring(self):
        self.data["ratings"][self.ids[0]].update(level="N/A", evidence_status="insufficient")
        self.assertEqual(self.score()["coverage_percent"], 75)

    def test_unknown_answer_reference(self):
        self.data["ratings"][self.ids[0]]["evidence"][0]["answer_id"] = "missing"
        with self.assertRaisesRegex(ValueError, "不存在的回答"):
            self.score()

    def test_reason_required_per_dimension(self):
        self.data["ratings"][self.ids[0]]["evidence"][0]["reason"] = " "
        with self.assertRaises(ValueError):
            self.score()

    def test_same_answer_can_support_multiple_dimensions_with_separate_reasons(self):
        self.data["ratings"][self.ids[1]]["evidence"][0]["answer_id"] = "A1"
        self.assertEqual(self.score()["coverage_percent"], 100)

    def test_duplicate_evidence_reference_is_invalid(self):
        evidence = self.data["ratings"][self.ids[0]]["evidence"]
        evidence.append(copy.deepcopy(evidence[0]))
        with self.assertRaises(ValueError):
            self.score()

    def test_skipped_answer_is_not_negative_ability_evidence(self):
        self.data["answers"][0]["status"] = "skipped"
        with self.assertRaisesRegex(ValueError, "主动跳过"):
            self.score()
        self.data["ratings"][self.ids[0]].update(level="N/A", evidence_status="insufficient")
        self.assertEqual(self.score()["coverage_percent"], 75)

    def test_unknown_or_incorrect_answer_can_be_evidence_but_is_not_auto_graded(self):
        for status in ["explicitly_unknown", "incorrect"]:
            self.data["answers"][0]["status"] = status
            self.data["ratings"][self.ids[0]]["level"] = "Below"
            self.assertEqual(self.score()["score"], 68.75)

    def test_guided_answer_cannot_replace_independent_answer(self):
        self.data["answers"][0]["feedback_intervened"] = True
        with self.assertRaisesRegex(ValueError, "指导后回答"):
            self.score()

    def test_summary_is_not_relabelled_as_raw(self):
        self.data["answers"][0]["record_kind"] = "summary"
        before = copy.deepcopy(self.data)
        self.score()
        self.assertEqual(self.data, before)

    def test_duplicate_answer_ids(self):
        self.data["answers"][1]["id"] = "A1"
        with self.assertRaises(ValueError):
            self.score()

    def test_invalid_answer_fields(self):
        for field, value in [("text", ""), ("question_id", None), ("status", "unknown"),
                             ("record_kind", "invented"), ("feedback_intervened", 1)]:
            with self.subTest(field=field):
                data = make_input()
                data["answers"][0][field] = value
                with self.assertRaises(ValueError):
                    self.score(data)

    def test_invalid_critical_dimensions(self):
        for value in [None, "technical_foundation", [self.ids[0], self.ids[0]], ["unknown"], [{}]]:
            self.data["critical_dimensions"] = value
            with self.assertRaises(ValueError):
                self.score()

    def test_structural_errors(self):
        cases = [[], None, {}, {**self.data, "interview_type": "other"},
                 {**self.data, "typo": 1}, {**self.data, "answers": {}},
                 {**self.data, "ratings": []}]
        for data in cases:
            with self.subTest(data=data):
                with self.assertRaises(ValueError):
                    self.score(data)

    def test_missing_dimension_is_not_silently_na(self):
        del self.data["ratings"][self.ids[0]]
        with self.assertRaises(ValueError):
            self.score()

    def test_pure_function_does_not_mutate_input_or_config(self):
        before, config_before = copy.deepcopy(self.data), copy.deepcopy(RUBRICS)
        result = self.score()
        result["dimensions"][0]["evidence"][0]["reason"] = "changed"
        self.assertEqual(self.data, before)
        self.assertEqual(RUBRICS, config_before)

    def test_strict_json(self):
        for text in ['{"a":1,"a":2}', '{"a":NaN}', '{"a":Infinity}', '{"a":-Infinity}', '{']:
            with self.assertRaises(ValueError):
                parse_json(text)


class CommandLineTests(unittest.TestCase):
    def run_cli(self, text=None, *args):
        return subprocess.run([sys.executable, "-B", str(ROOT / "scripts" / "score.py"), *args],
                              input=text, capture_output=True, encoding="utf-8",
                              env={**os.environ, "PYTHONIOENCODING": "utf-8"}, cwd=tempfile.gettempdir())

    def test_valid_stdin_from_unrelated_working_directory(self):
        result = self.run_cli(json.dumps(make_input()))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["score"], 75)
        self.assertEqual(result.stderr, "")

    def test_invalid_input_has_json_error_and_nonzero_exit(self):
        result = self.run_cli('{"interview_type":"technical"}')
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertIn("缺少字段", json.loads(result.stderr)["error"])

    def test_utf8_bom_file(self):
        with tempfile.TemporaryDirectory(prefix="interview-score-test-") as directory:
            path = Path(directory) / "input.json"
            path.write_text(json.dumps(make_input()), encoding="utf-8-sig")
            result = self.run_cli(None, str(path))
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_missing_file(self):
        result = self.run_cli(None, str(ROOT / "tests" / "nonexistent.json"))
        self.assertEqual(result.returncode, 2)
        self.assertIn("error", json.loads(result.stderr))


if __name__ == "__main__":
    unittest.main()
