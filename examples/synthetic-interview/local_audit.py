"""Optional original-machine preservation audit; never a public verification pass."""

import argparse
import json
import os
from pathlib import Path
import sys

from review_support import REPO, digest, read_json


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("language", choices=("zh-CN", "en-US"))
    args = parser.parse_args()
    run = Path(__file__).resolve().parent / args.language
    baseline_path = run / "evidence/preexisting-file-hashes.json"
    result = {"scope": "local_workspace_preservation_only", "public_verification": False}
    if not baseline_path.exists():
        result.update({"status": "not_executed", "reason": "Original local baseline is not published"})
        print(json.dumps(result))
        return 2
    baseline = read_json(baseline_path)
    allowed = read_json(run / "run-metadata.json").get("allowed_modifications", [])
    changed = [name for name, value in baseline.items()
               if name not in allowed and
               (not (REPO / name).is_file() or digest(REPO / name) != value)]
    outside = set()
    collection = Path(__file__).resolve().parent
    for directory, dirs, files in os.walk(REPO):
        here = Path(directory)
        dirs[:] = [name for name in dirs if name != ".git" and here / name != collection]
        outside.update((here / name).relative_to(REPO).as_posix() for name in files)
    new_files = sorted(outside - set(baseline) - set(allowed))
    result.update({"status": "changed" if changed or new_files else "unchanged",
                   "baseline_files": len(baseline), "changed": changed,
                   "new_files_outside_test_collection": new_files,
                   "note": "Historical workspace baseline; later authorized maintenance can cause differences. Not a public test result."})
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if changed or new_files else 0


if __name__ == "__main__":
    sys.exit(main())
