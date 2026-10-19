"""Public archive replay and failure controls, without private data or Git history."""

import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

from review_support import REPO, RUNTIME_FILES


COLLECTION = Path(__file__).resolve().parent


class PublicReviewTests(unittest.TestCase):
    def fixture(self, language="en-US"):
        temporary = tempfile.TemporaryDirectory(prefix="interview-review-test-")
        self.addCleanup(temporary.cleanup)
        repo = Path(temporary.name)
        collection = repo / "examples/synthetic-interview"
        run = collection / language
        source = COLLECTION / language
        manifest = json.loads((source / "evidence/public-evidence-manifest.json").read_text(encoding="utf-8"))
        for name in RUNTIME_FILES:
            target = repo / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(REPO / name, target)
        for name in [*manifest["files"], "evidence/public-evidence-manifest.json", "audit_run.py", "run_score.py"]:
            target = run / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source / name, target)
        for name in ["review_support.py", "local_audit.py"]:
            shutil.copyfile(COLLECTION / name, collection / name)
        return repo, run

    def call(self, repo, script, *arguments):
        return subprocess.run([sys.executable, "-B", "-X", "utf8", str(script), *arguments],
                              cwd=repo, capture_output=True, text=True, encoding="utf-8")

    def test_both_archives_replay_without_git_installation_or_local_baseline(self):
        for language, score in [("zh-CN", 63.75), ("en-US", 76.25)]:
            with self.subTest(language=language):
                repo, run = self.fixture(language)
                self.assertFalse((repo / ".git").exists())
                self.assertFalse((run / "installed-skills").exists())
                self.assertFalse((run / "evidence/preexisting-file-hashes.json").exists())
                audit = self.call(repo, run / "audit_run.py")
                self.assertEqual(audit.returncode, 0, audit.stderr + audit.stdout)
                summary = json.loads(audit.stdout)
                self.assertTrue(summary["passed"])
                self.assertEqual(summary["not_executed"][0]["status"], "not_executed")
                result = self.call(repo, run / "run_score.py", "evidence/interviewer-score-001.input.json", "--label", "public")
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(json.loads(result.stdout)["score"], score)
                local = self.call(repo, run.parent / "local_audit.py", language)
                self.assertEqual(local.returncode, 2)
                self.assertFalse(json.loads(local.stdout)["public_verification"])

    def test_changed_runtime_is_refused_before_execution(self):
        repo, run = self.fixture()
        path = repo / "assets/rubrics.json"
        path.write_bytes(path.read_bytes() + b"\n")
        result = self.call(repo, run / "run_score.py", "evidence/interviewer-score-001.input.json")
        self.assertEqual(result.returncode, 2)
        self.assertIn("differs from tested version", result.stderr)
        self.assertFalse((run / "review-output").exists())

    def test_changed_original_answer_fails_exact_integrity(self):
        repo, run = self.fixture()
        path = run / "exchanges/candidate-001.md"
        path.write_bytes(path.read_bytes() + b"changed")
        result = self.call(repo, run / "audit_run.py")
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("transcript_matches_original_messages", json.loads(result.stdout)["failed"])

    def test_invalid_citation_is_rejected(self):
        repo, run = self.fixture()
        path = run / "evidence/interviewer-score-001.input.json"
        data = json.loads(path.read_text(encoding="utf-8-sig"))
        next(iter(data["ratings"].values()))["evidence"][0]["answer_id"] = "NONEXISTENT"
        path.write_text(json.dumps(data), encoding="utf-8")
        result = self.call(repo, run / "audit_run.py")
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("rating_references_exist", json.loads(result.stdout)["failed"])

    def test_wrong_tested_version_is_rejected(self):
        repo, run = self.fixture()
        path = run / "run-metadata.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["skill_commit_sha"] = "0" * 40
        path.write_text(json.dumps(data), encoding="utf-8")
        result = self.call(repo, run / "run_score.py", "evidence/interviewer-score-001.input.json")
        self.assertEqual(result.returncode, 2)
        self.assertIn("pinned SHA", result.stderr)

    def test_output_cannot_overwrite_original_evidence(self):
        repo, run = self.fixture()
        path = run / "transcript.jsonl"
        before = hashlib.sha256(path.read_bytes()).hexdigest()
        result = self.call(repo, run / "audit_run.py", "--output", "transcript.jsonl")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), before)


if __name__ == "__main__":
    unittest.main()
