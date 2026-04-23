# Issue #7219: Ray Job against existing RayCluster shouldn't be handled by Kueue as the RayCluster is already admitted.

**Summary**: Ray Job against existing RayCluster shouldn't be handled by Kueue as the RayCluster is already admitted.

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7219

**Last updated**: 2025-10-15T16:35:56Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@laurafitzgerald](https://github.com/laurafitzgerald)
- **Created**: 2025-10-09T16:29:08Z
- **Updated**: 2025-10-15T16:35:56Z
- **Closed**: 2025-10-15T16:35:55Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 3

## Description

### Title
RayJob webhook panics when clusterSelector is set

Addressed by: https://github.com/kubernetes-sigs/kueue/pull/7218

Also some related discussion: https://github.com/kubernetes-sigs/kueue/pull/6844

### Description

**Problem:**
When a RayJob has `spec.clusterSelector` set (to use an existing RayCluster), the Kueue webhook validation panics with a nil pointer dereference. This occurs because the validation code attempts to access fields in `spec.RayClusterSpec` that may be nil or incomplete when using an existing cluster.

**Current Behavior:**
1. RayJobs with `clusterSelector` and a queue label trigger webhook validation
2. Validation attempts to check `RayClusterSpec.EnableInTreeAutoscaling` and `RayClusterSpec.WorkerGroupSpecs`
3. These fields may be nil/missing when using `clusterSelector`, causing a panic
4. The webhook crashes and the RayJob creation is blocked with an unclear error

**Expected Behavior:**
RayJobs that use `clusterSelector` to reference existing clusters should not be managed by Kueue at all. These jobs:
- Should pass webhook validation without being checked by Kueue
- Should be skipped by the Kueue reconciler
- Should be handled entirely by the Ray operator

**Use Case:**
Users want to:
1. Create a RayCluster that is managed and queued by Kueue
2. Submit multiple RayJobs against that existing cluster without additional queueing
3. The RayJobs should run on the already-admitted cluster without Kueue interference

**Environment:**
- Kueue version: v0.11.6
- Job type: RayJob (ray.io/v1)

**Reproduction:**
```yaml
apiVersion: ray.io/v1
kind: RayJob
metadata:
  name: test-job
  namespace: default
  labels:
    kueue.x-k8s.io/queue-name: user-queue  # Has queue label
spec:
  clusterSelector:  # References existing cluster
    ray.io/cluster: my-existing-cluster
  entrypoint: python script.py
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-09T17:02:33Z

Thank you for the issue, and the fix.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-10-15T16:35:50Z

@laurafitzgerald I believe this is fixed in main, 0.14 and 0.13.

/close

If I am mistaken please feel free to reopen.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-10-15T16:35:56Z

@kannon92: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/7219#issuecomment-3407350527):

>@laurafitzgerald I believe this is fixed in main, 0.14 and 0.13.
>
>/close
>
>If I am mistaken please feel free to reopen.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
