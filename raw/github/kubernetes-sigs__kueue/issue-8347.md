# Issue #8347: MultiKueue: report MK CQ as inactive if using ProvisioningRequest on the manager cluster

**Summary**: MultiKueue: report MK CQ as inactive if using ProvisioningRequest on the manager cluster

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8347

**Last updated**: 2026-01-12T15:14:46Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-12-19T08:03:16Z
- **Updated**: 2026-01-12T15:14:46Z
- **Closed**: 2026-01-12T15:14:46Z
- **Labels**: `kind/feature`, `priority/important-longterm`, `area/multikueue`
- **Assignees**: [@IrvingMg](https://github.com/IrvingMg)
- **Comments**: 3

## Description

**What would you like to be added**:

Soft validation (report as inactive) against using MK admission check and ProvReq AC in the management cluster.

We do the "soft validation" here: https://github.com/kubernetes-sigs/kueue/blob/main/pkg/cache/scheduler/clusterqueue.go

**Why is this needed**:

To drive users away from misconfiguration.

This configuration does not make sense currently as the management cluster would not create Pods anyway.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T08:16:54Z

/area multikueue

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T08:18:18Z

/priority important-longterm

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2026-01-07T09:53:19Z

/assign
