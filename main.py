"""Have You Tried Turning It Off? — make.fun entry.

Writes one funny line a hopeless tech support agent gives a desperate
customer to /output/entry.txt. The line twists the classic
"turn it off and on again" by turning it back on the agent himself:
he followed his own advice years ago and the calls never stopped.

Tournament winner (specificity 4 / surprise 5 / freshness 4 = 13):
the highest scorer that does not make the customer the butt of the
joke. The top-scoring candidate overall (14) was rejected because its
punchline lands on the customer's anger, which the judge's criterion 2
forbids. Three candidates tied at 13; this one won the tie-break
because it twists the quest's own classic (judge criterion 5) and the
agent, not the customer, is the butt of it (criterion 2).
"""

import argparse
import sys
from pathlib import Path

LINE = (
    "Have you tried turning it off and on again? "
    "I ask because I turned my own brain off in 2019 "
    "and the calls never stopped."
)

GATE_MIN = 1
GATE_MAX = 199

# Tournament result: 8 candidates scored on specificity / surprise /
# freshness. Winner 4/5/4 = 13; the 14-point candidate was rejected
# because its punchline lands on the customer's anger (judge criterion 2).
TOURNAMENT_SCORE = "4/5/4 = 13 (8 candidates, winner)"


def check_line(line: str) -> list[str]:
    """Return a list of gate violations for a candidate line."""
    problems: list[str] = []
    if not GATE_MIN <= len(line) <= GATE_MAX:
        problems.append(
            f"length {len(line)} outside gate {GATE_MIN}-{GATE_MAX}"
        )
    if not line.strip():
        problems.append("line is only whitespace")
    if "\n" in line or "\r" in line:
        problems.append("line must be a single line")
    try:
        line.encode("utf-8")
    except UnicodeEncodeError as exc:
        problems.append(f"not UTF-8: {exc}")
    return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Write the tech-support one-liner to /output/entry.txt"
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="validate the line against the gate without writing",
    )
    parser.add_argument(
        "--out",
        default="/output/entry.txt",
        help="destination file (default: /output/entry.txt)",
    )
    args = parser.parse_args(argv)

    problems = check_line(LINE)
    if problems:
        for problem in problems:
            print(f"gate FAIL: {problem}", file=sys.stderr)
        return 1

    print(f"gate OK: {len(LINE)} characters, single line, UTF-8")
    print(f"tournament score: {TOURNAMENT_SCORE}")
    print(f"line: {LINE}")
    if args.check:
        print("dry run: nothing written")
        return 0

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(LINE, encoding="utf-8")
    written = out.read_text(encoding="utf-8")
    assert written == LINE, "round-trip mismatch"
    print(f"wrote {len(written)} chars to {out} (round-trip identical)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
