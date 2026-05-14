### Domain: Code Style 

Rules:
1. **Naming precision** — every new identifier must accurately describe what it contains. A reader should not be able to mistake it for something broader or narrower.
   - Builder/wrapper methods: follow the existing pattern. If the codebase uses `Label(k, v)` not `AddLabel(k, v)`, new methods must match.
   - Variable names must reflect actual content. If a set called `noMoreBorrowingCohorts` might actually contain cohorts that are already borrowing, the name is wrong.
   - Feature gate names must match what they actually gate. A gate named `SkipFinalizersForServingWorkloads` that guards a different condition is a hard naming violation.
   - New API fields that mirror existing ones should be symmetric (e.g. if `excludeResourcePrefixes` exists, the complement should be `includeResourcePrefixes`).
2. **Naming conventions** — Diff Code MUST abide by existing naming conventions in the file and package.
3. **Util function reuse** — Diff Code SHOULD reuse existing util/helper functions. Reimplementing logic that already exists elsewhere is a style violation.
4. **Log verbosity levels** — per-reconciliation-cycle log lines must use `V(4)` or higher. `V(2)` is for coarse-grained lifecycle events only. A `V(2)` log inside a reconcile loop is a recurring-style violation.
5. **Test function naming** — unit/integration test function names must align with the names of the functions they test.
6. Diff Code MUST NOT have any typos

Deduct points proportionally to the severity and frequency of violations. Naming precision issues that introduce semantic ambiguity are more severe than minor wording choices.