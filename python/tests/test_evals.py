import json
from pathlib import Path

import pytest

from evals import build_dataset, paraphrase, run_eval
from evals.metrics import score, table
from evals.sources import LANGS

DATA = Path(build_dataset.__file__).parent / "data"


def test_committed_data_matches_a_fresh_build() -> None:
    cases = build_dataset.build()
    for split in ("dev", "test"):
        assert (DATA / f"{split}.jsonl").read_text(encoding="utf-8") == build_dataset.dump(
            cases, split
        )


def test_build_is_deterministic() -> None:
    assert build_dataset.build() == build_dataset.build()


def test_splits_do_not_share_a_base_message() -> None:
    cases = build_dataset.build()
    dev = {c["base"] for c in cases if c["split"] == "dev"}
    test = {c["base"] for c in cases if c["split"] == "test"}
    assert dev.isdisjoint(test)


def test_languages_are_balanced_and_labels_are_consistent() -> None:
    cases = build_dataset.build()
    counts = {lang: sum(1 for c in cases if c["lang"] == lang) for lang in LANGS}
    assert len(set(counts.values())) == 1
    for case in cases:
        assert (case["label"] == "urgent") == (case["kind"] == "urgent")
    ids = [c["id"] for c in cases]
    assert len(ids) == len(set(ids))


def test_main_writes_both_files(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(build_dataset, "DATA_DIR", tmp_path / "data")
    build_dataset.main()
    assert (tmp_path / "data" / "dev.jsonl").read_text() == (DATA / "dev.jsonl").read_text()


@pytest.mark.parametrize(
    ("lang", "text"),
    [("ru", "saans nahi aa rahi"), ("ur", "سینے میں درد ہے"), ("en", "I can't breathe")],
)
def test_paraphrase_is_seeded(lang: str, text: str) -> None:
    assert paraphrase.paraphrase(text, lang, "s1") == paraphrase.paraphrase(text, lang, "s1")
    outs = {paraphrase.paraphrase(text, lang, f"s{i}") for i in range(40)}
    assert len(outs) > 1


def test_stretch_leaves_words_without_vowels() -> None:
    import random

    assert paraphrase._stretch("xyz", random.Random("a")) == "xyz"


def test_score_counts_and_table() -> None:
    cases = [
        {"id": "a", "lang": "en", "text": "u1", "label": "urgent", "kind": "urgent"},
        {"id": "b", "lang": "en", "text": "u2", "label": "urgent", "kind": "urgent"},
        {"id": "c", "lang": "en", "text": "r1", "label": "routine", "kind": "routine"},
        {"id": "d", "lang": "ru", "text": "h1", "label": "routine", "kind": "hard_negative"},
    ]
    result = score(cases, lambda t: t in {"u1", "h1"}, list_misses=True)
    assert result["en"]["confusion"] == {"tp": 1, "fn": 1, "fp": 0, "tn": 1}
    assert result["en"]["missed_ids"] == ["b"]
    assert result["ru"]["urgent_recall"] is None
    assert result["ru"]["false_urgent_on_hard_negatives"] == "1/1"
    assert result["ur"]["false_urgent_rate"] is None
    assert result["all"]["urgent_recall"] == 0.5
    assert "| en | 0.5 | 1 of 2 | 0.0 | 0/0 |" in table(result)


def test_smoke_run_finishes(capsys: pytest.CaptureFixture[str]) -> None:
    assert run_eval.main(["--smoke"]) == 0
    assert "smoke: engine flagged" in capsys.readouterr().out


def test_label_writes_results_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(run_eval, "RESULTS_DIR", tmp_path)
    assert run_eval.main(["--label", "T"]) == 0
    written = json.loads((tmp_path / "T.json").read_text())
    assert set(written) == {"seed", "dev", "test"}
    assert "missed_ids" in written["dev"]["en"]
    assert "missed_ids" not in written["test"]["en"]


def test_smoke_fails_when_nothing_is_flagged(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(run_eval, "predict", lambda _text: False)
    assert run_eval.main(["--smoke"]) == 1
