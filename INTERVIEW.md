# Interview questions for llm-safety-rules-engine

The 12 hardest questions a reviewer could ask about this repo. The notes come from the repo. Write your own answer under each one, in your own words. Answers are left empty on purpose.

## 1. Why do the rules run before the model, and what is the model for?

Repo notes: ADR 0001. A model can be talked out of a rule, code cannot. The model is the second net.

My answer:

## 2. Why does an urgent message get a reply even when the patient has not consented?

Repo notes: ADR 0001. The pipeline checks the rules first, then consent, then calls the model.

My answer:

## 3. What do your three Hypothesis properties prove, and what do they not prove?

Repo notes: `tests/test_pipeline.py`. They hold for any input text. They do not say the lexicon finds real emergencies.

My answer:

## 4. Your mutation score was 0.97 and Urdu recall was 0.00. How is that possible?

Repo notes: ADR 0004 and the README table. Mutation testing changes code, not data.

My answer:

## 5. Which mutants survived, and why are they equivalent?

Repo notes: ADR 0004 lists all 7. Be ready to show one in `mutmut show`.

My answer:

## 6. English recall was 0.90 on dev and 0.30 on test. What went wrong?

Repo notes: `docs/fix_loop.md`. The lexicon was fitted to dev phrasings. The test split is also not blind.

My answer:

## 7. Missed urgent fell and false urgent rose. Why accept that?

Repo notes: ADR 0002. The engine does not read negation on purpose.

My answer:

## 8. How would you handle negation without ever downgrading a real emergency?

Repo notes: not built. A design question.

My answer:

## 9. Why were the labels built by construction, and what are the limits?

Repo notes: ADR 0003. No human labelled them, the author wrote lexicon and test sentences, and nobody who reads Urdu has checked them.

My answer:

## 10. Explain the output check bug you found at R2.

Repo notes: `docs/fix_loop.md`, "What failed". Folding repeated letters changed "need" to "ned".

My answer:

## 11. How does the engine handle a 200,000 word message?

Repo notes: `test_huge_message_is_scanned_quickly_and_fully`. The scan is linear in length times window size, and the model gets only the first 2000 characters.

My answer:

## 12. What would you change before this touched a real patient?

Repo notes: the README "What I would do next". Think clinical review, a blind test set, a real language review and a regulatory view.

My answer:
