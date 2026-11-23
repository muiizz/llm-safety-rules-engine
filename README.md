# llm-safety-rules-engine

[![check](https://github.com/muiizz/llm-safety-rules-engine/actions/workflows/check.yml/badge.svg)](https://github.com/muiizz/llm-safety-rules-engine/actions/workflows/check.yml)

A toy safety rules engine for an imaginary health chat assistant, in English, Roman Urdu and Urdu script.
The rules run before the model, and an urgent message is never downgraded. **This is a teaching example
on invented data. It is not medical advice and not a medical device.**

## What it shows

- A pipeline whose order is the safety design: normalise, rules, consent, model, output check (`python/safetyrules/pipeline.py`, ADR 0001).
- Hypothesis properties that hold for any input text:
  - an urgent message never reaches the model, even a hostile one, with or without consent
  - the model is never called without consent
  - adding text to a message never lowers its level
  - normalisation is idempotent
- A mutation score published next to per-language recall, to show they measure different things (ADR 0004).
- A fix loop with real before and after numbers (`docs/fix_loop.md`).

## Run it

```bash
make setup                                   # installs from lockfiles (needs uv, git, curl)
make check                                   # every gate, including mutation testing
make demo MSG="seene mein dard hai"          # classify one message with a fake model
make eval LABEL=R3                           # rebuild results, deterministic, no network, USD 0
make eval-smoke                              # tiny run
```

No model is called anywhere. The "model" is a deterministic stub, so there is no spend to cap.

## How it works

```
text -> normalise -> rules -> urgent?  yes -> fixed urgent reply (model never called)
                                       no  -> consented? no  -> consent request (model never called)
                                                          yes -> model (text cut to 2000 chars) -> output check -> reply
```

- `normalise.py` folds case, width, Roman Urdu spellings, Arabic letter forms, vowel marks and invisible joiners.
- `lexicon.py` holds invented phrases and proximity rules for five symptom groups in three languages.
- `output_check.py` replaces model replies that give a dose or tell the patient to skip care.

## Results

Dated 23 Nov 2026. `make check` on commit `6dd2f27`: exit 0, 22 s, 131 tests, coverage 98.70%, mutation 189 of 196. Machine: AMD Ryzen 5 7535HS, 11 GB RAM, WSL2. Python 3.12.16, mutmut 3.8.1,
Hypothesis 6.170.17. Data: 342 synthetic messages (seed `portfolio-v1`), 171 dev and 171 test, 114 per language.
No model. Each round was committed with its result files (commits in `docs/fix_loop.md`). Test split:

| Round | Mutants killed | Recall en | Recall ru | Recall ur | Missed urgent | False urgent rate |
|---|---|---|---|---|---|---|
| R0 | 112/115 (0.97) | 0.30 | 0.00 | 0.00 | 81 of 90 | 0.049 |
| R1 | 112/115 (0.97) | 0.30 | 0.43 | 0.33 | 58 of 90 | 0.074 |
| R2 | 164/169 (0.97) | 0.30 | 0.80 | 0.80 | 33 of 90 | 0.148 |
| R3 | 189/196 (0.96) | 0.90 | 1.00 | 1.00 | 3 of 90 | 0.148 |

Command for the table: `cd python && uv run --frozen python -m evals.summarise`. Reproduce one round by checking out its
commit, then `make eval LABEL=<round>` and `make mutate`.

The lesson in the table: at R0 the mutation score is 0.97 and two of three languages have recall 0.00.
A high mutation score says the tests would notice a change to the code. It says nothing about inputs the
data never covers.

### What failed

Folding repeated letters in R2 (so "chestt" matches "chest") also changed the text the output check reads.
"need" became "ned", the check patterns stopped matching, and an unsafe model reply passed. A unit test
caught it before the commit, and normalisation is now split in two (`normalise` for rules, `plain` for the output check).
More in `docs/fix_loop.md`.

## What this does not show

- It does not show clinical safety. The phrases are invented and no clinician has reviewed them.
- The Roman Urdu and Urdu script text has not been read by a native reader. TODO(Muizz): review it.
- The test split is not blind: one author wrote the lexicon and the test sentences. English recall was 0.90 on dev and 0.30 on test at R2, and I only closed that gap with a rule written from the idea, not more phrases.
- Labels come from how the messages were built. No human labelled them, so none of these numbers are hand checked.
- The engine does not read negation, so "I do not have chest pain" is flagged urgent. 12 of 27 hard negatives are flagged on the test split.
- The hard negatives mostly probe negation, so this set cannot tell whether the proximity rules add false alarms of their own.
- Three English urgent test messages are still missed. I have not looked at which.
- Mutation testing covers `safetyrules/` only. Seven mutants survive and all are equivalent (ADR 0004).
- No model is called, so nothing here tests a real model or a spend cap.
- The gates were copied from quality-template and trimmed. This repo has no proofs of its own that each gate blocks a fault. GitHub CI ran once on `6dd2f27` and passed (`check`, 23 Nov 2026).
- One machine, one run per number. I have not measured run-to-run spread, and mutation results can vary with timing.

## What I would do next

- Have a native reader of Roman Urdu and Urdu script review the lexicon and relabel the set.
- Build a blind test set written by someone who has not seen the lexicon.
- Add negation handling as a second pass that can only raise the level, never lower it, with a property test for that.
- Add near-miss cases aimed at each proximity rule, to measure its false alarms.
- Put a real model behind the stub, with `MAX_USD_PER_RUN` and a monthly cap, and add the injection and leakage set from the eval-gate project.
- Add a blind error analysis of the three remaining misses.

## Repo settings

`main` requires the `check` status check, an up-to-date branch, applies to admins and blocks force pushes and deletion (`docs/branch-protection.json`, same setting as quality-template, where the proof that it blocks a failing PR is recorded). I did not repeat that proof here. Private vulnerability reporting is on.

## Docs

`docs/adr/` (decisions), `docs/fix_loop.md` (every round), `GATES.md`, `INTERVIEW.md`, `SECURITY.md`.
