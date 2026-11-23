# Fix loop log

Four rounds on a synthetic set of 342 messages (171 dev, 171 test), 114 per language, in English (en),
Roman Urdu (ru) and Urdu script (ur). I read only dev misses when deciding what to change. Numbers
below are on the test split unless stated. Dated 23 Nov 2026, run on one machine (see README).

Reproduce any round: check out the commit, then `cd python && uv run --frozen python -m evals.run_eval`
(the saved file is `python/evals/results/<round>.json`) and `make mutate` (saved as `mutation-<round>.json`).

| Round | Commit | Change |
|---|---|---|
| R0 | `731afef` | English-only lexicon. |
| R1 | `9734109` | Add Roman Urdu and Urdu script phrases (direct translations of the English rules). |
| R2 | `5bbffd1` | Fold spellings: repeated Latin letters, common Roman Urdu variants, Arabic letter forms, vowel marks, invisible joiners. |
| R3 | `d62c875` | Add proximity rules (a symptom word and a trouble word within a few words) and convulsion terms. |

Test split:

| Round | Mutants killed | Recall en | Recall ru | Recall ur | Missed urgent | False urgent rate |
|---|---|---|---|---|---|---|
| R0 | 112/115 (0.97) | 0.30 | 0.00 | 0.00 | 81 of 90 | 0.049 |
| R1 | 112/115 (0.97) | 0.30 | 0.43 | 0.33 | 58 of 90 | 0.074 |
| R2 | 164/169 (0.97) | 0.30 | 0.80 | 0.80 | 33 of 90 | 0.148 |
| R3 | 189/196 (0.96) | 0.90 | 1.00 | 1.00 | 3 of 90 | 0.148 |

Dev split urgent recall (en, ru, ur): R0 0.77, 0.00, 0.00. R1 0.77, 0.53, 0.37. R2 0.90, 0.90, 0.90. R3 1.00, 1.00, 1.00.

## What the loop shows

1. **A high mutation score beside no language coverage.** At R0 the score is 0.97 and two of three
   languages have recall 0.00. The tests were strong for the code that existed. The lexicon is data,
   and mutation testing does not mutate data. See ADR 0004.
2. **Dev and test disagree.** At R2, English recall is 0.90 on dev and 0.30 on test. I had fitted the
   lexicon to the dev sentences. Only a rule written from the idea (R3 proximity) closed the gap, not
   more phrases.
3. **Missed urgent goes down, false urgent goes up.** Missed urgent: 81 to 3 of 90. False urgent rate:
   0.049 to 0.148. The rise came at R2: once the engine matched noisy spellings, it also matched
   noisy copies of the hard negatives ("I do not have chest pain" and its misspellings). R3 did not
   raise it further on this set, but the hard negatives only probe negation, so this set cannot show
   whether proximity rules add false alarms of their own.
4. **I accept the false alarms.** ADR 0002: an urgent message is never downgraded, and the engine does not read
   negation.

## What failed

At R2, folding repeated letters ("need" becomes "ned") also changed the text the output check reads.
The output check patterns, written with normal spelling, stopped matching, and an unsafe model reply
("there is no need to see a doctor") passed through. A unit test caught it before the commit. The fix
splits normalisation into `normalise` (for rules) and `plain` (for the output check), with a test on each.

## Still wrong at R3

Three English urgent messages on the test split are still missed. I have not looked at which ones.
TODO(Muizz): decide whether to open the test split for error analysis. Doing so would end its use as unseen data.
