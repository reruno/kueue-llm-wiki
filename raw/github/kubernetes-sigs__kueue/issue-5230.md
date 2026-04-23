# Issue #5230: TAS: In-Place Workload topology re-assignment when node failure

**Summary**: TAS: In-Place Workload topology re-assignment when node failure

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5230

**Last updated**: 2025-06-23T09:47:18Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-05-12T13:22:03Z
- **Updated**: 2025-06-23T09:47:18Z
- **Closed**: 2025-06-23T09:47:18Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 8

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

When the nodes go to down, the scheduled and running TAS workload want to be re-assigned the new healthy Topology (node).

**Why is this needed**:

Based on disruption and autoscaling, the node could go down. In that case, we want to re-schedule the workload to proper Topology nodes.

**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [x] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-12T13:22:32Z

@PBundyra @pajakd @mimowo Is this a valid issue for https://github.com/kubernetes-sigs/kueue/pull/5212?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-12T16:20:53Z

sgtm

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-05-13T08:33:30Z

Absolutely, thanks @tenzen-y! I would add that we want to assign the correct nodes without doing the whole rescheduling cycle, just eke the old assignment

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-13T10:32:35Z

> Absolutely, thanks [@tenzen-y](https://github.com/tenzen-y)! I would add that we want to assign the correct nodes without doing the whole rescheduling cycle, just eke the old assignment

Thank you for checking this. Let's track the feature by this issue.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-23T09:34:31Z

@PBundyra can we close this already?

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-06-23T09:46:29Z

Yes, we merged all PRs required for the iteration of this feature, so we're good with closing it. Thank you

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-06-23T09:46:41Z

@tenzen-y Feel free to close it

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-23T09:47:18Z

/close
