### Domain: Comments

Rules:
1. Diff Code MUST NOT contain excessive comments that explain obvious or self-documenting code.
2. Comments are allowed — and encouraged — only for genuinely complex sections where the *why* or the theoretical side is non-obvious to a reader.
3. **Comment accuracy** — any comment or docstring must match what the code actually does. A comment that says "first batch of Job pods" when the function operates on generic Workloads is wrong and must be updated. Inaccurate comments are worse than no comments.
4. **TODO comments** — if Diff Code keeps temporary or deprecated code for compatibility reasons, a TODO comment is *required*, not optional. The TODO must specify the exact version when it can be removed (e.g. `// TODO: drop in 0.18`) and reference a tracking issue.
5. Comments MUST NOT contain typos and obvious errors

Full marks if comments are absent or appropriately targeted. Deduct for over-commenting, comments that describe *what* rather than *why*, or inaccurate comments. Deduct for missing required TODOs on compatibility shims.