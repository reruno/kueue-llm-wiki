# Issue #463: Migrate some validations to CEL

**Summary**: Migrate some validations to CEL

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/463

**Last updated**: 2024-04-26T20:20:13Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@nayihz](https://github.com/nayihz)
- **Created**: 2022-12-06T01:58:26Z
- **Updated**: 2024-04-26T20:20:13Z
- **Closed**: 2024-04-26T20:16:00Z
- **Labels**: `kind/cleanup`, `priority/important-longterm`, `kind/deprecation`, `lifecycle/frozen`
- **Assignees**: [@IrvingMg](https://github.com/IrvingMg)
- **Comments**: 5

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:
we can remove the webhooks in favor of CEL once 1.24 reaches EoL https://kubernetes.io/releases/

**Why is this needed**:
Since Kubernetes 1.25, we can use CEL validation rules to implement a few common immutability patterns directly in the manifest for a CRD.
ref: https://kubernetes.io/blog/2022/09/29/enforce-immutability-using-cel/

## Discussion

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-12-06T02:30:50Z

/kind deprecation
/priority important-longterm

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-12-06T13:36:29Z

/lifecycle frozen

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-03-28T18:20:02Z

Maybe we cannot fully replace defaulting, but at least we can replace validation.

/assign trasc

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2024-04-08T11:45:57Z

/assign @IrvingMg

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-04-26T20:20:11Z

/retitle Migrate some validations to CEL

Since we couldn't delete the webhooks entirely due to some limitations of CEL.

We requested some improvements upstream https://github.com/kubernetes/kubernetes/issues/124490
