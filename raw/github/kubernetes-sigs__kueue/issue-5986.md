# Issue #5986: [Feature Request] Kueue Dashboard resources support View YAML

**Summary**: [Feature Request] Kueue Dashboard resources support View YAML

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5986

**Last updated**: 2025-07-24T16:28:29Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@samzong](https://github.com/samzong)
- **Created**: 2025-07-16T01:02:05Z
- **Updated**: 2025-07-24T16:28:29Z
- **Closed**: 2025-07-24T16:28:29Z
- **Labels**: `kind/feature`, `area/dashboard`
- **Assignees**: _none_
- **Comments**: 2

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

when i use kueue web dashboard(kubeviz) view resources.

I wonder if it's possible to provide the ability to view YAML.
(workload,localqueue,clusterqueue,cohort,resourceflavor)

**Why is this needed**:

In most cases, in addition to the basic resource definitions, I would like to see detailed definitions.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [x] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-16T07:50:59Z

+1 for the feature known from k9s, we could also add an option to see describe, based on the k9s inspiration (might be separate issue)

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-07-17T06:42:44Z

/area dashboard
