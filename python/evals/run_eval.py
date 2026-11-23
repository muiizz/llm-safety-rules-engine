"""Run the engine on the synthetic set and report the confusion matrix per language.

    python -m evals.run_eval                 print the tables
    python -m evals.run_eval --label R0      also write evals/results/R0.json
    python -m evals.run_eval --smoke         tiny run that must finish and find some urgent cases

No network, no model, no cost. Results are deterministic.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from evals.build_dataset import SEED, build
from evals.metrics import score, table
from safetyrules.rules import Level, classify

RESULTS_DIR = Path(__file__).parent / "results"


def predict(text: str) -> bool:
    return classify(text).level is Level.URGENT


def run(*, smoke: bool) -> dict[str, Any]:
    cases = [{k: str(v) for k, v in c.items()} for c in build()]
    if smoke:
        cases = cases[:30]
    by_split = {split: [c for c in cases if c["split"] == split] for split in ("dev", "test")}
    return {
        "seed": SEED,
        "dev": score(by_split["dev"], predict, list_misses=True),
        "test": score(by_split["test"], predict, list_misses=False),
    }


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--label", default="")
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args(argv)
    result = run(smoke=args.smoke)
    for split in ("dev", "test"):
        print(f"\n{split} split\n{table(result[split])}")
    if args.smoke:
        found = result["dev"]["all"]["confusion"]["tp"] + result["test"]["all"]["confusion"]["tp"]
        print(f"\nsmoke: engine flagged {found} urgent cases")
        return 0 if found > 0 else 1
    if args.label:
        RESULTS_DIR.mkdir(exist_ok=True)
        path = RESULTS_DIR / f"{args.label}.json"
        path.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
        print(f"\nwrote {path}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main(sys.argv[1:]))
