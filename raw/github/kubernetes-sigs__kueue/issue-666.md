# Issue #666: Support for RayJob

**Summary**: Support for RayJob

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/666

**Last updated**: 2023-05-24T19:12:52Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mwielgus](https://github.com/mwielgus)
- **Created**: 2023-03-31T13:27:28Z
- **Updated**: 2023-05-24T19:12:52Z
- **Closed**: 2023-05-24T19:12:52Z
- **Labels**: `kind/feature`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 3

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Kueue support for RayJob - https://ray-project.github.io/kuberay/guidance/rayjob/

**Why is this needed**:

Ray is one of the most popular AI/ML frameworks out there and with RayJob it fits nicely into Kueue model.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@trasc](https://github.com/trasc) — 2023-04-05T11:09:21Z

/assign

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-05-10T15:05:14Z

ref https://github.com/ray-project/kuberay/pull/926
It looks like it's almost ready to merge

### Comment by [@trasc](https://github.com/trasc) — 2023-05-10T15:07:17Z

> ref [ray-project/kuberay#926](https://github.com/ray-project/kuberay/pull/926) It looks like it's almost ready to merge

I'll rebase and rework #667 as soon as it is.
