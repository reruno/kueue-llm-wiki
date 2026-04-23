# Issue #297: Support kubeflow operator

**Summary**: Support kubeflow operator

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/297

**Last updated**: 2023-10-16T16:16:28Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@xiaoxubeii](https://github.com/xiaoxubeii)
- **Created**: 2022-07-14T00:28:08Z
- **Updated**: 2023-10-16T16:16:28Z
- **Closed**: 2023-10-16T15:10:05Z
- **Labels**: `kind/feature`, `lifecycle/frozen`
- **Assignees**: [@tenzen-y](https://github.com/tenzen-y)
- **Comments**: 12

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
Support kubeflow training operator.

**Why is this needed**:
It is to track the status of kueue to support kubeflow training operator.

- [ ] https://github.com/kubeflow/common/pull/196 
- [x] #65

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-07-14T13:14:44Z

Note that MPIJob latest version is not currently part of the training-operator https://github.com/kubeflow/training-operator/issues/1479

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2022-10-12T13:21:35Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues and PRs.

This bot triages issues and PRs according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue or PR as fresh with `/remove-lifecycle stale`
- Mark this issue or PR as rotten with `/lifecycle rotten`
- Close this issue or PR with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-10-12T15:29:50Z

/lifecycle frozen

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-03-20T13:21:10Z

This is currently blocked on https://github.com/kubeflow/common/pull/196

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-07-05T19:10:20Z

/assign

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-07-19T07:09:04Z

As a first step, I opened a PR to add the PyTorchJob support, and then I will add the following framework support:

- TFJob
- MXJob
- XGboostJob
- PaddleJob

Also, I'm on the fence if we should support MPIJob v1 hosted only on kubeflow/training-operator (currently, MPIJob v2 hosted only on kubeflow/mpi-operator)

Regarding MPIJob v1 wdyt? @alculquicondor @mimowo @kerthcet @trasc

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-07-19T14:26:49Z

I'm ok leaving it out if it's not trivial to support 2 API versions. I think the CRD objects themselves are not compatible.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-07-19T15:25:07Z

> I think the CRD objects themselves are not compatible.

Right.

> I'm ok leaving it out if it's not trivial to support 2 API versions.

We can not support v1 and v2 API by a single controller: https://github.com/kubernetes-sigs/kueue/tree/a103723023aa6c5a63cc8c1248fd38d8640d7003/pkg/controller/jobs/mpijob.

However, once we implement a separate controller for v1 like https://github.com/kubernetes-sigs/kueue/blob/3589969054023cb8b584a4639f4b9dec8c371a67/pkg/controller/jobs/kubeflow/jobs/pytorchjob/pytorchjob_controller.go, we can support v1.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-07-19T15:26:10Z

Anyway, I think MPIJob v1 is a lower priority since we already support MPIJob v2.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-07-20T03:13:45Z

 +1 to defer the work unless we receive strong demands.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-07-20T05:02:04Z

> +1 to defer the work unless we receive strong demands.

I agree.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-08-16T20:15:11Z

Tasks:

- [x] PyTorchJob: https://github.com/kubernetes-sigs/kueue/pull/995
- [x] TFJob: https://github.com/kubernetes-sigs/kueue/pull/1068
- [x] XGBoostJob: https://github.com/kubernetes-sigs/kueue/pull/1114
- [x] MXJob: https://github.com/kubernetes-sigs/kueue/pull/1183
- [x] PaddleJob: https://github.com/kubernetes-sigs/kueue/pull/1142
