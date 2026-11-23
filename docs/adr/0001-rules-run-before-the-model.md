# ADR 0001: Rules run before the model

Status: accepted, 23 Nov 2026

## Decision
`pipeline.handle` runs in this order: normalise, rules, consent, model, output check.

- An urgent message gets a fixed reply. The model is never called for it.
- Consent is checked after the rules, because an urgent message must get the urgent reply even
  from a patient who has not consented yet.
- The model is called only for a routine message from a consented patient.
- The model gets a patient code and the text cut to 2000 characters. It never gets a name.

## Why
A model can be talked out of a rule. Code cannot. The model is the second net, not the first.

## Consequence
Two Hypothesis tests state this for any input: the model is never called without consent, and it
is called only for routine, consented messages.
