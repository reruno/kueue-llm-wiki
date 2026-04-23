# Issue #5452: MultiKueue: Orphaned Pods Remain After Job Completion or Deletion in Manager Cluster

**Summary**: MultiKueue: Orphaned Pods Remain After Job Completion or Deletion in Manager Cluster

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5452

**Last updated**: 2025-06-10T16:18:28Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@ichekrygin](https://github.com/ichekrygin)
- **Created**: 2025-06-02T20:16:07Z
- **Updated**: 2025-06-10T16:18:28Z
- **Closed**: 2025-06-10T16:18:28Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 2

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

In a MultiKueue setup with a manager and worker cluster, when a Job completes, is updated, or deleted from the manager cluster, the corresponding Job and Workload are removed from the worker cluster. However, the pods created by the remote Job remain in _Completed_ or _Running_ (or in case of job deletion) state. This leads to orphaned pods that continue to exist in the worker cluster.

While completed pods primarily raise cleanup concerns, running pods are more problematic as they continue consuming resources and quota on the worker cluster.

**What you expected to happen**:
Job's pods should be removed form the remote cluster "together" with Job removal

**How to reproduce it (as minimally and precisely as possible)**:

1. Create a Job in the manager cluster.
2. Wait for the Workload to be admitted and the Job to start running in the worker cluster.
3. Either:
3.1. Wait for the Job to complete in the worker cluster,
3.2. or delete the Job from the manager cluster before completion.
4. Observe that while the Job and Workload are removed from both clusters, the pods in the worker cluster remain (active in case of deletion).

Repro for Job update: involve the same steps 1 and 2:
3.1 Update Job in the remove cluster (change concurrency setting)
4. Observe that the new Job instance pods are created in addition to still running the old Job instance 

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`): `v1.31.2`
- Kueue version (use `git describe --tags --dirty --always`): `v0.12.1`
- Cloud provider or hardware configuration: `kind v0.25.0 go1.23.4 darwin/arm64`
- OS (e.g: `cat /etc/os-release`): `darwin/arm64`
- Kernel (e.g. `uname -a`): `Darwin macbookpro.lan 24.4.0 Darwin Kernel Version 24.4.0: Fri Apr 11 18:33:47 PDT 2025; root:xnu-11417.101.15~117/RELEASE_ARM64_T6000 arm6`
- Install tools:
- Others:

## Discussion

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-06-02T20:24:10Z

A possible cause might be the Delete call in:

https://github.com/kubernetes-sigs/kueue/blob/main/pkg/controller/jobs/job/job_multikueue_adapter.go#L125
```golang
remoteClient.Delete(ctx, &job)
```
It appears to be missing a PropagationPolicy option, which could lead to child pods not being deleted when the remote Job is removed.

For comparison, a similar delete with explicit propagation policy is used here:
https://github.com/kubernetes-sigs/kueue/blob/main/pkg/controller/jobframework/reconciler.go#L626

As a workaround (and possible fix), I tested adding the Background propagation policy:
```golang
remoteClient.Delete(ctx, &job, client.PropagationPolicy(metav1.DeletePropagationBackground))
```
With this change, orphaned pods were properly cleaned up after the Job deletion.
Might be worth considering this addition to ensure expected garbage collection behavior.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-03T06:53:27Z

Thank you for reporting 👍 

I believe this is because indeed the default delete strategy of k8s Jobs is "orphan", see [here](https://github.com/kubernetes/kubernetes/blob/b65f712d2cb70a358e9c77d02b21874c14d3d1ba/pkg/registry/batch/job/strategy.go#L70C15-L70C21).

> As a workaround (and possible fix), I tested adding the Background propagation policy:

This looks to me as a proper fix. Looking at the comment in the k8s code reference above using "Background" is the default mode going forward. It was kept as Orphan just for backwards compatibility, since core k8s is a very "stable" project. It is completely ok to use "background" in Kueue.

@ichekrygin would you like to submit a PR? 

cc  @mszadkow @mwysokin
