"""`python -m safetyrules "message"` classifies one message with the stub model."""

import sys

from safetyrules.model_stub import StubModel
from safetyrules.pipeline import handle


def main(argv: list[str]) -> int:
    text = " ".join(argv) if argv else ""
    reply = handle(text, patient_code="P-0001", consented=True, model=StubModel())
    print(f"level: {reply.level.name}  rules: {', '.join(reply.rule_ids) or '-'}")
    print(reply.text)
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main(sys.argv[1:]))
