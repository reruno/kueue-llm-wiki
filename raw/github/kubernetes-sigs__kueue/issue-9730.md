# Issue #9730: Scheduling: improve logging for start/end of each phase of scheduling cycle

**Summary**: Scheduling: improve logging for start/end of each phase of scheduling cycle

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9730

**Last updated**: 2026-03-11T17:11:39Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-03-06T19:47:30Z
- **Updated**: 2026-03-11T17:11:39Z
- **Closed**: 2026-03-11T17:11:39Z
- **Labels**: `kind/feature`
- **Assignees**: [@sohankunkerkar](https://github.com/sohankunkerkar)
- **Comments**: 2

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

 I would like to log boundaries between each phase of scheduling cycle to make it easy to infer from logs how long they took, in particular:
- obtaining heads
- nomination
- snapshoting (can be long for TAS)
- workload processing 

Finally, in defer it would be nice to log the end. This way we can also easily tell how long scheduler was sleeping between cycles.

**Why is this needed**:

There are no clear logs indicating boundaries between phases of each scheduling cycle takes.
Estimation of the times is possible by side effects or internal logs at higher levels, but we should make it convenient.

The motivation was investigation for https://github.com/kubernetes-sigs/kueue/issues/9715

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-06T19:48:12Z

cc @sohankunkerkar @tenzen-y @mwielgus @gabesaba

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-03-06T20:53:19Z

/assign
