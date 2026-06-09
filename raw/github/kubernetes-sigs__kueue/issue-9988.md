# Issue #9988: Support quota automation in MultiKueue manager cluster

**Summary**: Support quota automation in MultiKueue manager cluster

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9988

**Last updated**: 2026-06-04T12:00:30Z

---

## Metadata

- **State**: open (reopened)
- **Author**: [@olekzabl](https://github.com/olekzabl)
- **Created**: 2026-03-18T18:41:54Z
- **Updated**: 2026-06-04T12:00:30Z
- **Closed**: —
- **Labels**: `kind/feature`, `area/multikueue`
- **Assignees**: [@olekzabl](https://github.com/olekzabl), [@Singularity23x0](https://github.com/Singularity23x0)
- **Comments**: 4

## Description

**What would you like to be added**:

An option to automatically adjust the quotas for a MultiKueue manager cluster ClusterQueue based on the total worker quotas.

**Why is this needed**:

Currently, MultiKueue docs advise keeping manager quotas in sync with worker quotas: specifically, equal to the sum of worker quotas. There are 2 problems with this:

- When such maintenance is left as user's responsibility, it is inconvenient and error-prone.
- Strict equality may not be optimal for scheduling throughput. A user may want to keep the manager quota _somewhat above_ or _somewhat below_ total workers' quota, depending on the use case.

A relatively simple yet reasonably powerful approach here would be to introduce a configurable _relative multiplier_ (i.e. keep manager quota equal to `customMultiplier * sum(workerQuotas)`).

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@olekzabl](https://github.com/olekzabl) — 2026-03-18T18:42:21Z

/area multikueue
/assign

### Comment by [@olekzabl](https://github.com/olekzabl) — 2026-03-25T13:11:09Z

Note: this is related to #10105, though - as I'm diving into details of both - they're going to be quite independent on the API surface, and even the implementations may end up having a relatively small overlap.

Thus, I found it best to split #10105 out from here as a separate issue. I'm considering driving it in a separate KEP (very likely referring to _some_ parts of the KEP for the issue here).

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-05-27T10:15:48Z

@Singularity23x0: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/9988#issuecomment-4553606194):

>/reopen
>/assign


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@michael-pryor](https://github.com/michael-pryor) — 2026-06-04T12:00:30Z

+1 from a production user perspective. We're also tracking KEP-10270 (NodeQuotaPolicy) for the single-cluster side of this — the combination of auto-detecting worker capacity from nodes (#10270) and aggregating it at the manager level (#9988) would fully automate our quota management.
