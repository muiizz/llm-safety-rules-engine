# CLAUDE.md

This is Project 6, `llm-safety-rules-engine`, in Abdul Muizz's public engineering portfolio. Read `PORTFOLIO_BRIEF.md` in full at the start of every session. Muizz keeps it locally and it is not in this repo, because it names private systems. If this file and the brief differ, the brief wins.

## Non-negotiable rules
1. Synthetic data only. No real patient, student, staff or client data. No production code, lexicons, thresholds or prompts from any private system.
2. Permission before naming. Name no private company or system in any file here until Muizz confirms written permission.
3. No invented facts. If a fact about Muizz or his past work is needed, stop and ask. Leave a visible `TODO(Muizz): ...`.
4. Every number is reproducible. State date, commit SHA, dataset, machine, model and version, and the exact command. If something was not run, say so.
5. One command to run: `make setup`, then `make check`, `make demo`, `make eval`.
6. CI calls `make check` and nothing else. Gates were copied from quality-template (`.quality-template-version`).
7. Honest limits. The README ends with "What this does not show" and "What I would do next". This is a toy, not medical advice.
8. Small, meaningful commits. Record decisions as short ADRs in `docs/adr/`.
9. Muizz must understand every line. Explain each design decision in 2 or 3 plain sentences.
10. No em dashes. Short sentences, plain words. No filler such as "seamless", "robust", "cutting-edge" or "leverage".
11. Secrets come from environment variables only. Never print a key.
12. Any script that calls a paid model reads `MAX_USD_PER_RUN` and a monthly cap. This repo calls none.

Never weaken, skip or delete a gate, test or threshold to make a check pass.

## This repo
- Order of work in `safetyrules/pipeline.py` is the safety design: rules, then consent, then model, then output check. Do not reorder it.
- An urgent message is never downgraded (ADR 0002). Hypothesis tests in `python/tests/test_pipeline.py` state it.
- The lexicon is invented and unreviewed by a native reader. Keep the `TODO(Muizz)` until Muizz says otherwise.
- Use dev results to fix the engine. Report test results. Do not tune on the test split.
