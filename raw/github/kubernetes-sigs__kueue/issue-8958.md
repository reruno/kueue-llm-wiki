# Issue #8958: TAS: support spreading for inference workloads based on LWS

**Summary**: TAS: support spreading for inference workloads based on LWS

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8958

**Last updated**: 2026-02-03T08:57:26Z

---

## Metadata

- **State**: open
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-02-03T08:56:44Z
- **Updated**: 2026-02-03T08:57:26Z
- **Closed**: —
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 1

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

We need some form of spreading to be supported by TAS for inference workloads, based on LWS.

We don't need "strict" spreading, just the best effort is enough. The MostFreeCapacity seems to do a good job, and I have prototyped already some idea based on the MostFreeCapacity here, and it seems to work: https://github.com/kubernetes-sigs/kueue/pull/8923

**Why is this needed**:

To better support failure tolerance. Placing all LWS groups on the same pool of nodes is risky for our users.

Imagine LWS with 4 groups, each group is 4 pods. This is 16 Pods, and all of them could fit into one "rack". If the rack fails the entire LWS may fail.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-03T08:57:04Z

cc @PBundyra @tenzen-y @gabesaba wdyt?
