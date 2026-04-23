# Issue #1337: Support preemption while borrowing

**Summary**: Support preemption while borrowing

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1337

**Last updated**: 2024-01-18T14:57:21Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2023-11-16T13:58:11Z
- **Updated**: 2024-01-18T14:57:21Z
- **Closed**: 2024-01-18T14:57:21Z
- **Labels**: `kind/feature`
- **Assignees**: [@mimowo](https://github.com/mimowo)
- **Comments**: 4

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Enable preemption while borrowing. 

**Why is this needed**:

Today, preemption is not possible if it requires the CQ to borrow from another one.

There are scenarios where a globally shared quota is put in a separate ClusterQueue. In other words, every ClusterQueue in the cohort is borrowing from the shared CQ. Then, it is necessary to have preemption while borrowing, to be able to implement quality of service.

**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [x] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2023-11-16T13:58:27Z

cc @alculquicondor 
/assign

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-11-16T16:10:32Z

I think a possible API could look like this:

```yaml
preemption:
  borrowFromCohort:
    policy: Disable | LowerThanThreshold | LowerPriority
    priorityThreshold: 100
```

### Comment by [@yaroslava-serdiuk](https://github.com/yaroslava-serdiuk) — 2023-11-28T14:40:40Z

@mimowo I would like to review this, if you don't mind

### Comment by [@mimowo](https://github.com/mimowo) — 2024-01-16T11:41:19Z

Remaining is the docs, but it seems we don't have a good place now. Opend the Issue as prerequisite : https://github.com/kubernetes-sigs/kueue/issues/1587

EDIT: as pointed out we already have a basic docs page for preemption https://kueue.sigs.k8s.io/docs/concepts/cluster_queue/#preemption, which can be extended for the purpose of this Issue.
