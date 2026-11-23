import pytest

from safetyrules.__main__ import main
from safetyrules.pipeline import URGENT_REPLY


def test_demo_urgent(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["I", "have", "chest", "pain"]) == 0
    assert capsys.readouterr().out == f"level: URGENT  rules: EN-CHEST\n{URGENT_REPLY}\n"


def test_demo_empty_goes_to_the_model_with_a_fixed_patient_code(
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert main([]) == 0
    assert capsys.readouterr().out == (
        "level: ROUTINE  rules: -\nThanks, P-0001. I noted your message.\n"
    )


def test_demo_lists_every_rule_that_fired(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["chest", "pain", "and", "a", "seizure"]) == 0
    assert capsys.readouterr().out.startswith("level: URGENT  rules: EN-CHEST, EN-SEIZURE\n")
