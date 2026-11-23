"""The order of work. The order is the safety design:

1. Rules run first, on the normalised text.
2. An urgent message gets a fixed reply. The model is never called.
3. Without consent, the model is never called.
4. Only then does the model run, and its output is checked.
"""

from dataclasses import dataclass
from typing import Protocol

from safetyrules.output_check import check_output
from safetyrules.rules import Level, classify

MAX_MODEL_INPUT_CHARS = 2000

URGENT_REPLY = (
    "This may be urgent. Contact your local emergency services or go to the nearest "
    "emergency room now.\n"
    "Yeh zaroori ho sakta hai. Abhi apni emergency service se rabta karein.\n"
    "یہ ضروری ہو سکتا ہے۔ ابھی ہنگامی مدد سے رابطہ کریں۔"
)
CONSENT_REPLY = "Before we chat, please reply YES to agree to the terms."


class Model(Protocol):
    def reply(self, patient_code: str, text: str) -> str: ...


@dataclass(frozen=True)
class Reply:
    text: str
    level: Level
    rule_ids: tuple[str, ...]
    model_called: bool


def handle(text: str, *, patient_code: str, consented: bool, model: Model) -> Reply:
    result = classify(text)
    if result.level is Level.URGENT:
        return Reply(URGENT_REPLY, Level.URGENT, result.rule_ids, model_called=False)
    if not consented:
        return Reply(CONSENT_REPLY, Level.ROUTINE, result.rule_ids, model_called=False)
    raw = model.reply(patient_code, text[:MAX_MODEL_INPUT_CHARS])
    return Reply(check_output(raw), Level.ROUTINE, result.rule_ids, model_called=True)
