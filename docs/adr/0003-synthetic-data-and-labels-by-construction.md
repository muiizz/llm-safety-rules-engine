# ADR 0003: Synthetic data, labels by construction

Status: accepted, 23 Nov 2026

## Decision
- Every message is invented. No patient data and no phrasing copied from any real system.
- The label comes from how a message was built (an urgent phrasing, an ordinary sentence, a
  near miss). No human labelled them, so none of the numbers are "hand checked".
- Messages are split into dev and test by base sentence. I used dev to fix the engine and report
  test.
- A seeded generator adds spelling and script noise. The same seed gives the same files, and a
  test fails if the committed files go stale.

## Limits
- The author of the lexicon also wrote the test sentences, so the test split is not blind.
- The Roman Urdu and Urdu script text has not been read by a native reader.
  TODO(Muizz): review it before anyone calls these numbers hand checked.
