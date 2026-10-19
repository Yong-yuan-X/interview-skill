"""Replay archived scoring with verified public repository resources."""

from pathlib import Path
import sys

RUN = Path(__file__).resolve().parent
sys.path.insert(0, str(RUN.parent))
from review_support import score_main


if __name__ == "__main__":
    raise SystemExit(score_main(RUN))
