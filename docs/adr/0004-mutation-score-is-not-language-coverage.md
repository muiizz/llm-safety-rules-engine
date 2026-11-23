# ADR 0004: A mutation score does not measure language coverage

Status: accepted, 23 Nov 2026

## Context
mutmut changes the code and checks that a test fails. It mutates code, not data. The lexicon is data,
and the engine code does not care which language a phrase is in.

## Decision
Publish the mutation score next to per-language recall for every round. Gate on the mutation
score (0.90) and report recall, because recall depends on the data and cannot be a code gate.

## Evidence
At R0 the mutation score was 112 of 115 (0.97) while Roman Urdu and Urdu script recall was 0.00.
The score said the tests were strong. They were, for the code that existed. The product did not
work in two of three languages. See the table in the README.

## Equivalent mutants
Seven mutants survive at R3 and all seven are equivalent: they change code without changing behaviour.
Two replace `"PSZC"` with a longer string that still contains the same letters. Two change
`main()` in ways that cannot show in the output. Three change the loop bounds in `_near`, where
extra start positions only read shorter slices that cannot add a match.
