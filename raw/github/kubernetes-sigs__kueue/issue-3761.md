# Issue #3761: Make Topology-Aware Scheduling compatible with cohorts and preemption

**Summary**: Make Topology-Aware Scheduling compatible with cohorts and preemption

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3761

**Last updated**: 2025-03-11T07:52:08Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-12-06T16:06:55Z
- **Updated**: 2025-03-11T07:52:08Z
- **Closed**: 2025-03-10T12:15:49Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 5

## Description

**What would you like to be added**:

Make TAS compatible with cohorts and preemption.

**Why is this needed**:

Currently, TAS does not work when cohorts or preemption are used. In that case the CQ is marked as inactive (see https://github.com/kubernetes-sigs/kueue/tree/main/keps/2724-topology-aware-scheduling#alpha). 

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [x] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-06T16:07:07Z

cc @mwielgus @mwysokin @tenzen-y

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-12T10:05:37Z

Listing cleanups to do identified during https://github.com/kubernetes-sigs/kueue/pull/4200:
- introduce PodSetReference to represent PodSet names for static code analysis
- add a unit test for `if len(cq.TASFlavors) == 0 {` as requested in [comment](https://github.com/kubernetes-sigs/kueue/pull/4200#discussion_r1951691235)
- add a unit test for `if cq.TASFlavors[*tasFlvr] == nil {` as requested in [comment](https://github.com/kubernetes-sigs/kueue/pull/4200#discussion_r1952616625)
- attempt to commonize the structures for `PodSetResources` and `TASPodSetRequests` as requested in [comment](https://github.com/kubernetes-sigs/kueue/pull/4200#discussion_r1950788801)

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-12T13:13:21Z

Could you add https://github.com/kubernetes-sigs/kueue/pull/4200#discussion_r1952616625 to your list?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-12T13:34:14Z

Sure, updated the list, but I think long-term it is better to manage in the refreshed [spreadsheet](https://docs.google.com/spreadsheets/d/1MXCjKZtAfqBTb61bJo46u7jIUqRIlu1NrYj1L8Xz-UU/edit?resourcekey=0-gr1ML2A1Axi8s6Lxr-Zhlw&gid=0#gid=0).

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-12T13:35:34Z

> spreadsheet

Thanks, SGTM
