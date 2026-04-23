# Issue #6919: Failure to remove finalizer for pod / podgroup workload type

**Summary**: Failure to remove finalizer for pod / podgroup workload type

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6919

**Last updated**: 2025-10-23T17:08:13Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@amy](https://github.com/amy)
- **Created**: 2025-09-18T20:37:57Z
- **Updated**: 2025-10-23T17:08:13Z
- **Closed**: 2025-09-18T23:45:04Z
- **Labels**: `kind/bug`
- **Assignees**: [@amy](https://github.com/amy)
- **Comments**: 11

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
Nevermind

**What you expected to happen**:

**How to reproduce it (as minimally and precisely as possible)**:

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-09-18T21:21:43Z

@amy: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/6919#issuecomment-3309764745):

>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-09-18T21:36:07Z

@amy: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/6919#issuecomment-3309795870):

>/reopen


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@amy](https://github.com/amy) — 2025-09-18T23:45:00Z

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-09-18T23:45:05Z

@amy: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/6919#issuecomment-3310024109):

>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-19T07:53:09Z

Oh, it reminded me something: maybe the "Terminating" Pod was already "Failed", but it would display in kubectl as Terminating. This bug was fixed in 1.31: https://github.com/kubernetes/kubernetes/pull/122038

### Comment by [@Panlq](https://github.com/Panlq) — 2025-10-21T10:14:21Z

<img width="1001" height="60" alt="Image" src="https://github.com/user-attachments/assets/dc3d70bb-5841-44f0-8e15-6fe8f3c5d1c8" />

<img width="1006" height="324" alt="Image" src="https://github.com/user-attachments/assets/bf696216-d76a-4b40-9911-f410681407c3" />

```bash
k get deployment -n xxx | grep xx       ⎈ k8s-xxxxxxxx-cluster
Warning: Use tokens from the TokenRequest API or manually created secret-based tokens instead of auto-generated secret-based tokens.
xxxxx-55                        1/1       1            1           4h36m
```
Last time when the deployment was deleted, the pod finalizers were not successfully removed, which caused the pod to remain stuck in the terminating state.

This is a single-replica deployment of mine. In what circumstances would the removal of the finalizer fail? @mimowo

### Comment by [@amy](https://github.com/amy) — 2025-10-22T01:44:23Z

@Panlq just checking, did you also delete the Workload?

### Comment by [@Panlq](https://github.com/Panlq) — 2025-10-22T02:14:48Z

> [@Panlq](https://github.com/Panlq) just checking, did you also delete the Workload?

There are two workload records of 55. I tried to delete the workload record corresponding to the Terminating pod, but the pod still did not exit automatically

### Comment by [@amy](https://github.com/amy) — 2025-10-22T17:28:15Z

@Panlq are you able to provide instructions for a repro?

### Comment by [@Panlq](https://github.com/Panlq) — 2025-10-23T10:52:03Z

> [@Panlq](https://github.com/Panlq) are you able to provide instructions for a repro?

```bash
{"level":"error","ts":"2025-10-23T10:31:24.753195283Z","caller":"controller/controller.go:316","msg":"Reconciler error","controller":"v1_pod","namespace":"media","name":"xxxxxxxxxx-57f9dc6f47-l2rmf","reconcileID":"1a5573bc-5686-4116-b0f2-a2536bc9b510","error":"Pod \"xxxxxxxxxx-57f9dc6f47-l2rmf\" is invalid: spec: Forbidden: pod updates may not change fields other than `spec.containers[*].image`,`spec.initContainers[*].image`,`spec.activeDeadlineSeconds`,`spec.tolerations` (only additions to existing tolerations),`spec.terminationGracePeriodSeconds` (allow it to be set to 1 if it was previously negative)\n  core.PodSpec{\n  \t... // 27 identical fields\n  \tOverhead:                  nil,\n  \tEnableServiceLinks:        &true,\n- \tTopologySpreadConstraints: nil,\n+ \tTopologySpreadConstraints: []core.TopologySpreadConstraint{\n+ \t\t{\n+ \t\t\tMaxSkew:           1,\n+ \t\t\tTopologyKey:       \"topology.kubernetes.io/zone\",\n+ \t\t\tWhenUnsatisfiable: \"ScheduleAnyway\",\n+ \t\t\tLabelSelector:     s\"&LabelSelector{MatchLabels:map[string]string{app: online-dev-cod\"...,\n+ \t\t},\n+ \t\t{\n+ \t\t\tMaxSkew:           1,\n+ \t\t\tTopologyKey:       \"kubernetes.io/hostname\",\n+ \t\t\tWhenUnsatisfiable: \"ScheduleAnyway\",\n+ \t\t\tLabelSelector:     s\"&LabelSelector{MatchLabels:map[string]string{app: online-dev-cod\"...,\n+ \t\t},\n+ \t},\n  \tOS:              nil,\n  \tSchedulingGates: nil,\n  \tResourceClaims:  nil,\n  }\n","stacktrace":"sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).reconcileHandler\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:316\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).processNextWorkItem\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:263\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).Start.func2.2\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:224"}
```

For the moment, I don't know what caused it either. Right now, I can't delete it unless I stop the kueue controller-manager pod or the pod webhook.

The above is the log of kueue controller-manager

### Comment by [@amy](https://github.com/amy) — 2025-10-23T17:08:13Z

@Panlq can you submit a new github issue with these clues?
