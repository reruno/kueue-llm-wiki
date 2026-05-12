
# Reviewer: pbundyra

**Summary**: Profile of Kueue reviewer @PBundyra — review philosophy, architectural focus, and approval patterns. Specializes in API design, Kubernetes-versioning practices, [[concurrent-admission]], and KEP-driven design discussion.

**Sources**: `raw/github/kubernetes-sigs__kueue/` — analysis of PRs where @PBundyra participated. Representative examples: pr-8861, pr-10244, pr-10388.

**Last updated**: 2026-05-12

---

## Identity and role

GitHub handle: [@PBundyra](https://github.com/PBundyra) (often referenced as `@pbundyra` in mentions)

Role: Listed in `OWNERS_ALIASES` as a `kueue-reviewer`, and additionally in `dependency-approvers` and `test-approvers`. Author of the [[concurrent-admission|Concurrent Admission]] KEP and routinely tagged for API-design discussions.

**Primary domain expertise**:

- API design and Kubernetes versioning (beta → v1 promotion rules)
- [[concurrent-admission|Concurrent Admission]] (KEP author)
- [[fair-sharing|Fair Sharing]] and admission policies
- Deprecation strategy and migration paths
- Test infrastructure (test-approver role)

---

## Review philosophy

### Design before code

PBundyra engages on KEPs and API shape before the code review, rather than catching design problems late. From pr-8861 (Concurrent Admission KEP):

> "I've synced with @mimowo and made some changes to the API structure. All functionalities remain the same but the interface changed a bit."

The pattern: align with other approvers on the API surface, then revise the KEP, then write code. When a PR arrives without that alignment, PBundyra will `/hold` and ask for the design discussion to happen first.

### Kubernetes API practices are non-negotiable

PBundyra applies Kubernetes-wide API conventions strictly. From pr-10244 on the admissionFairSharing API consolidation:

> "This is a breaking change... this work should be done on promotion from v1beta2 to v1."

And:

> "We should never remove API fields without a new API promotion. This goes against Kubernetes api practices for beta fields."

The rule is: **deprecation and removal happen on version promotion boundaries, not in-place**. A field added in v1beta2 stays in v1beta2 until the API graduates; only then can it be dropped.

### Linter and marker correctness

When `+required` is declared on a field, the JSON tag must drop `omitempty`. From pr-10244:

```suggestion
Mode AdmissionMode `json:"mode"`
```

(removing `omitempty` from the original `json:"mode,omitempty"`). The Kubernetes API linter enforces this, and PBundyra catches it pre-CI.

---

## Code review patterns

### API field markers

- `+required` ⇒ no `omitempty`
- `+optional` ⇒ `omitempty` required
- Deprecation comments must include the version that introduced the deprecation and the target version for removal
- Defaulting markers (`+default=`) must match validation

### Migration paths

For any deprecated field, PBundyra wants the answer to:
- What replaces it?
- What happens to existing objects on upgrade?
- When is it eligible for removal? (Tied to the next API version promotion.)

A deprecation without a documented migration path is a block.

### KEP scope

For non-trivial features, PBundyra escalates to wg-batch design discussion before coding starts. KEPs are treated as the contract; code that drifts from the KEP gets sent back to the KEP first.

---

## Approval workflow

### Standard approval

```
/lgtm
/approve
```

Clean and minimal once the design is settled.

### Hold for design discussion

When the API/KEP is not yet aligned:

```
/hold
```

with a comment proposing the design conversation (often: "let's bring this to wg-batch").

### Cherry-picks

PBundyra approves cherry-picks that align with the feature's release timeline and don't introduce breaking changes. For breaking changes, the answer is "wait for the next API version."

---

## Communication style

### Tone

Formal and design-focused. Speaks in terms of "promotion," "migration path," "API practices." Cites Kubernetes-wide conventions when objecting.

### Shorthand

- `/hold` early in the review when design needs discussion
- Direct API guidance phrased as a rule, e.g., "we should never remove API fields without promotion"
- "Let's bring this to wg-batch meetings" — escalation for large design questions

---

## What triggers a block

1. **API field removal on a beta version** — must wait for promotion
2. **`+required` marker with `omitempty` JSON tag** — linter violation
3. **Architectural change without a KEP** — design discussion required first
4. **Deprecation without documented migration path or timeline**
5. **Validation inconsistent with field markers**

---

## What earns approval

- API changes that follow Kubernetes versioning (no in-place breaks)
- Deprecations with a clear timeline and replacement
- Design that has been pre-aligned with [[reviewer-mimowo|@mimowo]], [[reviewer-tenzen-y|@tenzen-y]], or wg-batch
- Linter-clean field markers and JSON tags

---

## Patterns to copy when reviewing as PBundyra

**API design**
- Verify `omitempty` is absent on required fields and present on optional ones
- Verify deprecated fields document the replacement and the target version for removal
- Treat in-place removal of beta fields as a hard block; wait for API promotion

**Process**
- For non-trivial features, require a KEP before code review starts
- Escalate large design questions to wg-batch rather than litigating in the PR

**Backwards compatibility**
- Confirm migration paths are consistent across all code paths reading the same field
- For cherry-picks, confirm the change doesn't break the API surface on the release branch

---

## Related pages

- [[reviewer-mimowo]]
- [[reviewer-tenzen-y]]
- [[reviewer-gabesaba]]
- [[reviewers]]
- [[code-quality]]
- [[concurrent-admission]]
- [[fair-sharing]]
- [[feature-gates]]
