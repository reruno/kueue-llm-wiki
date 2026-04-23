# Issue #639: Graduate ComponentConfig API version to beta

**Summary**: Graduate ComponentConfig API version to beta

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/639

**Last updated**: 2023-03-17T17:59:18Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2023-03-16T05:24:10Z
- **Updated**: 2023-03-17T17:59:18Z
- **Closed**: 2023-03-17T17:59:18Z
- **Labels**: `kind/feature`
- **Assignees**: [@tenzen-y](https://github.com/tenzen-y)
- **Comments**: 5

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
I would like to graduate the `config.kueue.x-k8s.io` to `v1beta1`.

**Why is this needed**:
Currently, we use v1beta1 API for `kueue.x-k8s.io` (e.g., clusterQueue), and the API is production ready.
So it is better to graduate also `config.kueue.x-k8s.io` to beta API so that we declare the whole of Kueue is production ready. 

Maybe, there is no need to make any breaking changes to the `config.kueue.x-k8s.io`, unlike when we migrated `kueue.x-k8s.io` from v1alpha2 to v1beta1.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [x] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-03-16T05:24:47Z

cc: @kerthcet @alculquicondor

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-03-16T06:25:02Z

I think the config version has no strong correlation with the api version, but graduate to beta to mark it not in experiment seems necessary before we release v0.3?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-03-16T06:36:20Z

> I think the config version has no strong correlation with the api version,

I guess it's ok just to change the API version to v1beta1.

> graduate to beta to mark it not in experiment seems necessary

Yes, it is worth it.

> before we release v0.3?

I think it is better before we release v0.3.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-03-16T13:08:30Z

We haven't had any changes, so it should be good to graduate.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-03-16T13:28:50Z

Let me tackle this issue.

/assign
