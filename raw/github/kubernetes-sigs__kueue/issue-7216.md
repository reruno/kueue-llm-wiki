# Issue #7216: Add security context to in helm chart for kueueviz

**Summary**: Add security context to in helm chart for kueueviz

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7216

**Last updated**: 2026-02-17T14:25:07Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@Coec0](https://github.com/Coec0)
- **Created**: 2025-10-09T11:39:52Z
- **Updated**: 2026-02-17T14:25:07Z
- **Closed**: 2026-02-17T14:25:07Z
- **Labels**: `kind/feature`, `priority/important-longterm`
- **Assignees**: _none_
- **Comments**: 9

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Add a predefined pod security context to the Helm chart for kueueviz (alternatively, just add the possibility to set the values).

**Why is this needed**:

If you are running with a restricted pod security profile in your cluster, you will require hardened security contexts for workloads to run them. You cannot configure this for Kueueviz today in the Helm chart.

Ideally, this would be implemented as the controller manager implements it today:

https://github.com/kubernetes-sigs/kueue/blob/baf4c2392c60c13780b554d375c8fdb87c1d2f59/charts/kueue/values.yaml#L45C1-L55C16

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-09T12:13:26Z

sgtm, that is an omission I think

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-10T10:03:05Z

@Coec0  would you like to contribute a PR to align the approach with kueue-manager?

### Comment by [@Coec0](https://github.com/Coec0) — 2025-10-10T12:31:57Z

> [@Coec0](https://github.com/Coec0) would you like to contribute a PR to align the approach with kueue-manager?

Yes, I will work on a PR

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-10-10T12:44:48Z

SGTM

### Comment by [@Coec0](https://github.com/Coec0) — 2025-11-03T12:27:48Z

I haven't had time to get started on this yet. If anyone else would like to take over this, please feel free to do so.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T10:46:20Z

/priority important-longterm

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T10:46:29Z

@Coec0 any progress?

### Comment by [@Coec0](https://github.com/Coec0) — 2025-12-19T10:53:14Z

> [@Coec0](https://github.com/Coec0) any progress?

No, and I am currently too busy to plan working on it. If I find the time, I will add a new comment. I would suggest letting someone else implement it.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T10:55:39Z

/unassign @Coec0
