### Domain: Buggy Behavior

Rules:
1. **Logical correctness** — Diff Code MUST NOT contain logical errors, off-by-one errors, incorrect conditionals, unhandled edge cases, race conditions, or other behavioral defects.
2. **Backwards compatibility** — if Diff Code deletes or moves code that manages cluster state (finalizers, annotations, ownership, CRD fields), consider what happens during a rolling upgrade. Objects created by the old version must still be handled correctly by the new version. Deleting finalizer-removal code means pre-existing objects will be stuck. This is a **hard blocker** — deleted compatibility code is a serious bug.
3. **Feature gate interaction** — if Diff Code adds conditional behavior gated by a feature flag, verify the behavior is correct both when the gate is enabled and disabled. Untested gate-off paths are a latent correctness risk.
4. **Unnecessary guard conditions** — extra conditions that are logically unreachable at the call site add noise and can mask future bugs. They are a mild correctness concern.

Deduct points proportionally based on severity: a missing backwards-compatibility guard or logic error on the hot path is more severe than a minor edge-case miss.