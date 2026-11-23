# ADR 0002: Urgent is never downgraded, so the engine over-flags

Status: accepted, 23 Nov 2026

## Decision
Once any rule says urgent, nothing later can lower it: not consent, not the model, not output checks.
Property tests state that adding text to a message never lowers its level, and that an urgent
message never reaches the model, even when the model is hostile.

The engine does not understand negation. "I do not have chest pain" is flagged urgent.

## Why
A rule that tries to read negation can also read it wrong, and a missed urgent message costs more than a
false alarm. I chose to accept false alarms.

## Cost, measured
On the test split, false urgent rate went from 0.049 (R0) to 0.148 (R2) as the engine learned more
spellings. Hard negatives (negations and talk about a topic) are flagged urgent 12 of 27 times.
See `docs/fix_loop.md`.
