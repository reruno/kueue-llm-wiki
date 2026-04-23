# Feature gates

**Summary**: Kueue follows the Kubernetes feature-gate convention: new features land alpha → beta → GA, with a named gate (`--feature-gates=Foo=true|false`) controlling the on/off switch. Each graduation updates the default (alpha defaults off, beta defaults on, GA locked on).

**Sources**: `raw/github/kubernetes-sigs__kueue/`.

**Last updated**: 2026-04-23

---

## Canonical lifecycle

For each gate:

1. **Alpha.** Off by default. Breaking API changes permitted. Code shipped but opt-in.
2. **Beta.** On by default, opt-out remains. API considered stable; changes are deprecation-worthy.
3. **GA.** Locked on; the gate is deprecated and then removed.

The graduation of gates is tracked via dedicated issues per gate per release — e.g. "KEP 2936 (LocalQueueDefaulting): stage not updated for GA promotion" (source: issue-9633.md) caught a missed graduation update.

## Gates that have shipped

Representative subset (not exhaustive):

- **`QueueVisibility`** — the original [[visibility-api]] gate; later deprecated (source: issue-2256.md — Deprecate the QueueVisibility feature gate and corresponding API).
- **`LocalQueueDefaulting`** (KEP-2936) — allows a namespace to designate a default LocalQueue for jobs without the `queue-name` label. Graduated to GA per KEP-2936 (source: pr-3652.md). See [[local-queue]].
- **`FairSharing`** — see [[fair-sharing]] and KEP-1714 (source: pr-1773.md).
- **`TopologyAwareScheduling`** — see [[topology-aware-scheduling]], Alpha-to-Beta tracked in issue-3450.md.
- **`MultiKueue`** — see [[multikueue]]; the MultiKueue admission check and its controller sit behind the gate.
- **`ElasticJobsViaWorkloadSlices`** (KEP-77) — see [[elastic-jobs]].
- **`AdmissionCheckRetry`** — see [[admission-check]]; governs retry-across-flavors semantics (source: issue-10618.md).
- **`DynamicResourceAllocation` / KEP-2941** — DRA support for [[resource-flavor]] / partitionable devices (source: pr-3071.md — DRA design; source: pr-8734.md — extended resources design for DRA integration; source: pr-10283.md — partitionable devices).
- **`FairSharingPrioritizeNonBorrowing`** — see [[fair-sharing]] (source: issue-10126.md).
- **`BorrowWithinCohort` policies** — `LowerPriorityBorrowersOnly` added to protect nominal quota (source: issue-10171.md).

## When a gate graduates

Graduation is primarily a documentation + defaults change; the code typically stays the same. Missed graduation issues (source: issue-9633.md) are usually about forgetting to flip the stage annotation in the code so release tooling knows the new status.

## Related pages

- [[release-process]] — when gates graduate.
- [[fair-sharing]], [[topology-aware-scheduling]], [[multikueue]], [[elastic-jobs]] — feature-area pages that reference their gates.
