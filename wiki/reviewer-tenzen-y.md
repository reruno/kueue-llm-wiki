
# Reviewer: tenzen-y

**Summary**: Profile of Kueue core approver @tenzen-y — their review philosophy, domain expertise, recurring concerns, and approval workflow. Intended for LLMs and contributors so that review feedback in tenzen-y's areas is coherent with the project's implicit standards.

**Sources**: `raw/github/kubernetes-sigs__kueue/` — analysis of PRs where @tenzen-y left substantive feedback. Representative examples: pr-10145, pr-10282, pr-10623, pr-10668, pr-10674, pr-10677, pr-10684.

**Last updated**: 2026-05-12

---

## Identity and role

GitHub handle: [@tenzen-y](https://github.com/tenzen-y)

Role: One of three top-level Kueue approvers (alongside `gabesaba` and `mimowo`), listed in `OWNERS_ALIASES` under both `kueue-approvers` and `kueue-reviewers`. Co-assigned with [[reviewer-mimowo|@mimowo]] to every new release issue (`.github/ISSUE_TEMPLATE/NEW_RELEASE.md`) and listed in `SECURITY_CONTACTS`. The de-facto release manager for Kueue.

**Primary domain expertise** (inferred from CHANGELOG and review activity):

- Release management — cherry-picks across `release-0.x` branches, version targeting, release notes
- [[topology-aware-scheduling|Topology-Aware Scheduling]] (TAS): rank-based ordering, node failure handling, pod-index evaluation, annotation semantics
- Client-go and API plumbing: Cohort client, Config API connections
- Cross-cutting backwards-compatibility concerns across release branches
- Core integration with [[admission]] and workload state transitions

---

## Review philosophy

### Release-branch thinking

Unlike reviewers who focus on a single PR in isolation, tenzen-y mentally maps every change to the supported release branches. Bugfixes are routinely cherry-picked to the last 2–3 releases immediately after merge. From pr-10282:

```
/cherrypick release-0.16
/cherrypick release-0.17
```

When scope is unclear, tenzen-y will escalate to the other top-level approvers before approving: from pr-10145, "@mimowo @gabesaba Is this for the 0.18 target?"

### Semantic correctness over speed

tenzen-y blocks when annotation names, feature gate scopes, or release notes don't match what the code actually does. They will run multiple rounds of clarifying questions rather than accept "close enough" wording. From pr-10282, when reviewing a TAS annotation check:

> "Doesn't that mean `kueue.x-k8s.io/podset-slice-required-topology-constraints`? The `...-constraints` annotation manages multi-layer topology constraints."

The point: when a check tests one annotation in a related pair, the reviewer should ask whether the **set** of annotations is exhaustive.

### Process discipline

tenzen-y enforces the PR template because it drives release-note automation. From pr-10282:

> "For the next contributions, could you keep the PR template? Because our template has a couple of automation mechanism for release."

---

## Code review patterns

### Annotation and feature-gate exhaustiveness

In TAS and other annotation-driven code, tenzen-y checks that conditional branches cover the **whole** annotation family, not just one member. Mutually-exclusive pairs (`podset-required-topology` vs `podset-preferred-topology`) and constraints-style annotations (`...-constraints`) are common stumbling points; reviewers should ask whether each branch handles both.

### Release notes must describe the user-visible scenario

A release note that says "fix bug in X" is rejected; tenzen-y rewrites it to describe the scenario, the symptom, and the fix. Example from pr-10282 (rewritten by tenzen-y):

> "TAS: fix a bug that Pods which only contain the `kueue.x-k8s.io/podset-slice-required-topology` ... are not ungated."

The note must be specific enough for an operator reading the changelog to understand whether they were affected.

### Conflict resolution must be explicit

When merge conflicts arise in cherry-picks, tenzen-y asks the author to call out what was in conflict and how it was resolved, rather than accepting silently. From pr-10674:

> "Could you tell us where the conflict is in this file? ... CONFLICT (content): Merge conflict in pkg/util/tas/tas_assignment.go"

And when a conflict pulled in unused code from the other branch: "Can you manually revert these functions? They seem unused on 0.16 and brought here by the conflict."

### Follow-ups when stalled

tenzen-y pings authors after a few days of silence. From pr-10282 (after 5 days): "Hi, what about progressing here?" Polite, but a signal that the PR is being actively tracked.

---

## Approval workflow

### Standard approval

```
/lgtm
/approve
```

Or, when tenzen-y wants other approvers to also sign off:

```
Looks awesome!
/approve
Leaving lgtm @mimowo @mwysokin
```

(from pr-10677). Splitting `/approve` from `/lgtm` is intentional: it signals "I'm satisfied with the design but want someone closer to the code to confirm the last mile."

### Cherry-pick defaults

For production-relevant fixes, the default is to cherry-pick to the last 2 releases right after merge. tenzen-y will do this themselves if the original author doesn't request it.

### Escalation pattern

For scope/timing questions: tag both other top-level approvers (`@mimowo @gabesaba`). For domain-specific guidance: tag the area owner (e.g., `@mbobrovskyi`, `@PBundyra`).

---

## Communication style

### Tone

Direct, professional, solution-oriented. Positive feedback is short ("Thank you!", "Looks awesome!"); concerns are phrased as clarifying questions ("Doesn't that mean...?").

### Shorthand

Standard k8s shorthand: `sgtm`, `wdyt`, `ptal`. Less prolific use of `nit:` than [[reviewer-mimowo|mimowo]] — tenzen-y tends to either block or approve, with fewer style-level comments.

### Who they defer to

- Style / naming / log levels: [[reviewer-mimowo|@mimowo]]
- Test coverage details: @mimowo or area reviewers
- Cache/scheduler algorithmic concerns: [[reviewer-gabesaba|@gabesaba]]

This division is observable: tenzen-y's comments tend to cluster around release semantics, cherry-picks, and annotation/API correctness, not Go style.

---

## What triggers a block

1. **Release note that does not match code behavior** — rewritten before merge
2. **Annotation check that handles only part of a related family** — must cover the full set
3. **Merge conflict in a cherry-pick without an explanation** — author must describe the resolution
4. **Scope unclear for the release target** — escalated to other approvers before approval
5. **Missing PR template** — asked to use it next time (soft block)

---

## Patterns to copy when reviewing as tenzen-y

**Release management**
- Default to cherry-picking production bugs to the last 2 releases
- Verify the release note describes a scenario, not just a code change
- Ask "what release does this target?" if the PR doesn't say

**Annotation/API correctness**
- For any branch that checks one annotation, ask whether sibling annotations need the same treatment
- Confirm feature gate scope matches the names of the gates referenced

**Cherry-picks**
- Require explicit explanation of any merge-conflict resolution
- Strip in unused code that conflicts pulled across branches

**Escalation**
- Tag `@mimowo @gabesaba` when scope or timing for the release is unclear
- Tag the area maintainer when the question is domain-specific

---

## Related pages

- [[reviewer-mimowo]]
- [[reviewer-gabesaba]]
- [[reviewers]]
- [[code-quality]]
- [[topology-aware-scheduling]]
- [[release-process]]
