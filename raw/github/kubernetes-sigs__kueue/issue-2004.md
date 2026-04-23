# Issue #2004: Use k8s v1.30.0

**Summary**: Use k8s v1.30.0

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2004

**Last updated**: 2024-05-29T14:13:45Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@trasc](https://github.com/trasc)
- **Created**: 2024-04-18T05:21:52Z
- **Updated**: 2024-05-29T14:13:45Z
- **Closed**: 2024-05-29T14:13:44Z
- **Labels**: `kind/feature`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 6

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Use k8s v1.30.0

**Why is this needed**:

- Stay up to date with k/k
- Make use of the `batch.Job`  `spec.managedBy` field in MultiKueue

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@trasc](https://github.com/trasc) — 2024-04-18T05:22:00Z

/assign

### Comment by [@trasc](https://github.com/trasc) — 2024-04-18T06:32:36Z

We should hold this and #2005 until k8s 1.30.0 is supported by controller-runtime and envtest.

### Comment by [@kannon92](https://github.com/kannon92) — 2024-04-18T13:15:52Z

And probably kind needs to be released with 1.30.

https://hub.docker.com/r/kindest/node/tags

### Comment by [@trasc](https://github.com/trasc) — 2024-04-25T09:23:49Z

Controller runtime v0.18 is out, now we wait for `github.com/open-policy-agent/cert-controller`.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-04-29T11:32:47Z

> github.com/open-policy-agent/cert-controller

@trasc FYI: https://github.com/open-policy-agent/cert-controller/pull/202

### Comment by [@trasc](https://github.com/trasc) — 2024-05-15T08:49:18Z

> open-policy-agent/cert-controller#202

Looks like k/k 1.30.1 is out so maybe we'll have some progress on this in the near future.
