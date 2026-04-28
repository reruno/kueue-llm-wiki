# Failure Recovery

**Summary**: Kueue's opt-in failure recovery mechanism detects and force-deletes zombie pods — pods stuck in `Terminating` after a node failure — so that job replacement pods can start and quota is not wasted.

**Sources**: `raw/kueue/keps/6757-failure-recovery/README.md`, `raw/kueue/keps/6757-failure-recovery/kep.yaml`, `raw/kueue/pkg/controller/failurerecovery/failurerecovery.go`, `raw/kueue/pkg/controller/failurerecovery/pod_termination_controller.go`

**Last updated**: 2026-04-28

---

> **Stage: Alpha** — Feature gate `FailureRecovery`, disabled by default. (source: keps/6757-failure-recovery/kep.yaml)

## The zombie pod problem

When a node loses its `kubelet` heartbeat:

1. After `node-monitor-grace-period` (~50 s), the node gets the `node.kubernetes.io/unreachable` taint.
2. Pods get an automatic 5-minute toleration for that taint.
3. After the toleration expires, the control plane sets `deletionTimestamp` on the pods.
4. After `deletionGracePeriodSeconds` (~30 s), the `kubelet` should send `SIGKILL` — but it can't because it's offline.
5. The pod is stuck in `Terminating` indefinitely.

(source: keps/6757-failure-recovery/README.md)

For `batch/v1` Jobs with `podReplacementPolicy: Failed`, Kubernetes will not start a replacement pod until the stuck pod is actually gone. The job — and its Kueue quota reservation — are blocked. (source: keps/6757-failure-recovery/README.md)

## Solution: force-delete after a grace period

Kueue's failure recovery controller watches pods belonging to Kueue-managed workloads. When a pod has had a `deletionTimestamp` set for longer than a configurable grace period **and** the pod has the opt-in annotation, Kueue:

1. Moves the pod to the `Failed` phase (writes status update).
2. Force-deletes the pod (removes it from etcd).

This unblocks the Job controller, which then starts replacement pods. (source: keps/6757-failure-recovery/README.md)

## Opt-in: the safe-to-forcefully-delete annotation

**Both** the cluster admin (feature gate) and the user (pod annotation) must opt in:

```yaml
apiVersion: batch/v1
kind: Job
spec:
  template:
    metadata:
      annotations:
        kueue.x-k8s.io/safe-to-forcefully-delete: "true"
```

Only pods carrying this annotation are affected. Without it, Kueue leaves the pod alone even when the feature gate is enabled. (source: keps/6757-failure-recovery/README.md)

## Grace period

The controller waits for `deletionGracePeriodSeconds` on the pod to pass before force-deleting. A configurable additional grace period is planned for Beta. (source: keps/6757-failure-recovery/README.md)

## Interaction with gang scheduling

For gang-scheduled workloads (e.g. JobSet with `WaitForPodsReady`), a single zombie pod can block the entire job from completing. Force-deleting it unblocks the replacement, but the job may still need to re-queue depending on the restart policy. The re-queue is handled by [[gang-scheduling]] and [[admission]] logic: if the workload's `PodsReady` condition times out, the workload is evicted and goes back to the pending queue. (source: keps/6757-failure-recovery/README.md)

## Risk: premature replacement

Force-deleting a pod does not guarantee the original pod actually stopped. On a network-partitioned node (not a crashed node), the pod may still be running and writing to shared storage. The annotation is the user's declaration that this race condition is acceptable for their workload. (source: keps/6757-failure-recovery/README.md)

## Related pages

- [[workload]]
- [[gang-scheduling]]
- [[admission]]
- [[integration-plain-pod]]
- [[feature-gates]]
- [[testing]]
