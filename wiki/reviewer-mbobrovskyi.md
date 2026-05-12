
# Reviewer: mbobrovskyi

**Summary**: Profile of Kueue reviewer @mbobrovskyi — review philosophy, domain focus, and approval patterns. Specializes in test infrastructure, API consolidation, controller-runtime patterns, and code-reuse hygiene.

**Sources**: `raw/github/kubernetes-sigs__kueue/` — analysis of PRs where @mbobrovskyi left substantive feedback. Representative examples: pr-10244, pr-10294, pr-10323, pr-10388, pr-10595.

**Last updated**: 2026-05-12

---

## Identity and role

GitHub handle: [@mbobrovskyi](https://github.com/mbobrovskyi)

Role: Listed in `OWNERS_ALIASES` as a `kueue-reviewer`, and additionally in `dependency-approvers` (go.mod, vendor, package.json) and `test-approvers` (`*_test.go`, lint configs, test Makefiles). This makes mbobrovskyi the default approver for dependency bumps and test-infrastructure changes — most PRs touching those paths route to him.

**Primary domain expertise**:

- Test infrastructure: integration/e2e ginkgo conventions, CI performance, flake reduction
- Server-Side Apply (SSA) migration and controller-runtime API patterns
- Code consolidation / duplication removal across [[integrations|integrations]]
- [[metrics|Metrics]] and observability code
- Dependency management

---

## Review philosophy

### Ask "do we need this?" before approving

mbobrovskyi's most frequent review move is a short, direct question that puts the burden of justification on the author. From pr-10294:

> "Do we need this?"

(about apparently-redundant APIVersion/Kind fields)

And pr-10323:

> "Is it possible?"

(questioning whether negative durations can actually occur in production code)

These are not rhetorical — a vague answer means the code comes out.

### Eliminate duplication and over-doing functions

When the same logic appears across multiple places, mbobrovskyi proposes consolidation. From pr-10323:

> "It looks like we're duplicating logic. Can we reuse `pendingWorkloadInfos()` instead? In that case we don't need `pendingActive()` and `pendingInadmissible()`."

And on a single function doing too much:

> "I think this function does too much. It would be helpful to add a `workload.WorkloadClusterQueue(oldWl)` helper and use it outside this function."

### Don't mix concerns in a PR

Test optimization bundled with directory reorganization gets sent back. From pr-10595:

> "Can we move these changes into a separate PR to avoid mixing concerns?"

This aligns with the project-wide preference (also held by [[reviewer-mimowo|mimowo]]) to keep PRs cherry-pick-clean.

### Pragmatic Go idioms

Flags Go style improvements with concrete `suggestion:` blocks. From pr-10323:

```suggestion
maxD = max(d, maxD)
```

(instead of an `if`/assignment pair)

These are framed as improvements, not blockers — but the suggestion blocks make accepting them one click.

---

## Code review patterns

### Consistency across code paths

mbobrovskyi looks for places where the same field is handled inconsistently across two code paths. From pr-10244 (admissionFairSharing consolidation), they flagged a subtle bug: one cache path correctly fell back to the deprecated `AdmissionScope`, the other silently ignored it — so the same ClusterQueue behaved differently depending on which path read it.

> "Existing ClusterQueues using only admissionScope will lose AFS functionality in the queue cache path while still appearing to work in the scheduler cache path. This should use the same fallback logic."

This is the kind of bug that integration tests don't always catch; mbobrovskyi finds it by reading both paths side-by-side.

### Tests are a soft requirement

Integration tests are expected but framed as a gap to fill, not a hard block (unlike [[reviewer-mimowo|mimowo]]):

> "Could you please add integration tests?" (pr-10323)

For timing-sensitive code, he asks about clock skew and edge cases explicitly: "Yeah, but is it possible for LastTransitionTime to be later than clock.Now()?" — and accepts the answer once the negative-duration handling is justified.

### Naming and small simplifications

```suggestion
func pendingWaitStats(infos []*workload.Info, cl clock.Clock) (float64, float64) {
```

(prefers positional returns to named returns when only two simple values come back)

And flags redundant locals: "Looks like redundant variable" when `cl := m.clock` is extracted but used only once.

---

## Approval workflow

### Standard approval

```
/ok-to-test
/lgtm
/approve
```

`/ok-to-test` is a common opener for external contributors — mbobrovskyi gates Prow CI.

### Conditional approval — pass to top approvers

mbobrovskyi often `/lgtm`s for code quality but routes architecture or release-impact decisions upward. From pr-10244:

```
/lgtm
/assign @mimowo @tenzen-y
```

Read as: "code is clean, but the design decision needs a top-level approver."

### Cherry-picks

```
/cherrypick release-0.17
/cherrypick release-0.16
```

mbobrovskyi tracks which fixes belong on release branches and will request cherry-picks himself, especially for test-infrastructure or dependency fixes that don't carry feature risk.

---

## Communication style

### Tone

Direct, pragmatic, never preachy. Questions are short ("Do we need this?", "Why this change?", "Is it possible?") and expect a real answer. Suggestions are paired with code blocks so the author can accept them in one click.

### Shorthand

- `/ok-to-test` — unblock Prow CI for external PRs
- `/assign @top-approver` — delegate the architecture decision
- `suggestion:` blocks — preferred medium for style/idiom changes
- Direct questions over `nit:` — when mbobrovskyi flags something, they want an answer

---

## What triggers concern

1. **Duplication across code paths** — same logic in two places asks for a helper
2. **Inconsistent handling of deprecated/backward-compat fields** — same field treated differently in different paths
3. **Multi-concern PRs** — test reorganization mixed with logic changes
4. **Missing integration tests** for observation/metrics code
5. **Edge cases not addressed** — clock skew, nil/empty inputs in timing-sensitive paths
6. **Unjustified additions** — fields, conditions, or variables whose purpose isn't obvious

---

## Patterns to copy when reviewing as mbobrovskyi

**Code consolidation**
- Read related code paths side-by-side; flag inconsistent treatment of the same field
- When a function does multiple things, propose a named helper that captures one of them

**PR hygiene**
- If a PR mixes concerns, ask for it to be split before approval
- Use `suggestion:` blocks for Go-idiom improvements

**Tests for observation code**
- Ask for integration tests when adding metrics, status fields, or anything observable
- Probe clock-skew and nil/empty edge cases explicitly

**Delegation**
- For non-trivial design decisions, `/lgtm` for code and `/assign @mimowo @tenzen-y` for the design call
- For external contributors, gate CI with `/ok-to-test`

---

## Related pages

- [[reviewer-mimowo]]
- [[reviewer-tenzen-y]]
- [[reviewer-pbundyra]]
- [[reviewers]]
- [[code-quality]]
- [[testing]]
- [[testing-integration]]
- [[metrics]]
