# Issue #7393: A bug in the preemption logic

**Summary**: A bug in the preemption logic

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7393

**Last updated**: 2026-04-18T12:16:59Z

---

## Metadata

- **State**: open
- **Author**: [@zhifei92](https://github.com/zhifei92)
- **Created**: 2025-10-27T08:51:32Z
- **Updated**: 2026-04-18T12:16:59Z
- **Closed**: —
- **Labels**: `kind/bug`, `priority/important-longterm`, `lifecycle/rotten`
- **Assignees**: [@zhifei92](https://github.com/zhifei92)
- **Comments**: 4

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
The following queue fails to reclaim `vcuda-memory` and `vcuda-ratio` resources because CPU and memory have borrowed resources from other queues. This causes the reclamation of `vcuda-memory` and `vcuda-ratio` to fail, which is undesirable—since reclaiming only `vcuda-memory` and `vcuda-ratio` should be sufficient for our job to be handled by the admit
```
apiVersion: kueue.x-k8s.io/v1beta1
  kind: ClusterQueue
  metadata:
    finalizers:
    - kueue.x-k8s.io/resource-in-use
    generation: 5
    name: queue-3e
  spec:
    cohort: group-60
    flavorFungibility:
      whenCanBorrow: Borrow
      whenCanPreempt: Preempt
    preemption:
      borrowWithinCohort:
        policy: Never
      reclaimWithinCohort: Any
      withinClusterQueue: Never
    queueingStrategy: BestEffortFIFO
    resourceGroups:
    - coveredResources:
      - cpu
      - memory
      - pods
      - storage
      - rdma_devices
      flavors:
      - name: group-60-normal
        resources:
        - borrowingLimit: "40"
          name: cpu
          nominalQuota: "660"
        - borrowingLimit: 250Gi
          name: memory
          nominalQuota: 3450Gi
        - borrowingLimit: "2147483647"
          name: pods
          nominalQuota: "2147483647"
        - borrowingLimit: "35183298347008"
          name: storage
          nominalQuota: "35183298347008"
        - borrowingLimit: "35183298347008"
          name: rdma_devices
          nominalQuota: "35183298347008

    - coveredResources:
      - vcuda-core
      - vcuda-ratio
      - vcuda-memory
      flavors:
      - name: group-60-b
        resources:
        - borrowingLimit: "0"
          name: vcuda-core
          nominalQuota: "560"
        - borrowingLimit: "0"
          name: vcuda-ratio
          nominalQuota: "3500"
        - borrowingLimit: "0"
          name: vcuda-memory
          nominalQuota: "6265"
    stopPolicy: None

flavorsUsage:
    - name: group-60-normal
      resources:
      - borrowed: 8900m
        name: cpu
        total: 668900m
      - borrowed: "0"
        name: rdma_devices
        total: "0"
      - borrowed: 79700Mi
        name: memory
        total: 3612500Mi
      - borrowed: "0"
        name: pods
        total: "34"
      - borrowed: "0"
        name: storage
        total: "0"

    - name: group-60-b
      resources:
      - borrowed: "0"
        name: vcuda-core
        total: "34"
      - borrowed: "0"
        name: vcuda-memory
        total: "5186"
      - borrowed: "0"
        name: vcuda-ratio
        total: "2900"
```

**What you expected to happen**:
If `CPU` and `memory` resources do not need to be reclaimed, and only vcuda-memory and vcuda-ratio are being reclaimed, then `CPU` and `memory` should not be validated. Once sufficient `vcuda-memory` and `vcuda-ratio` have been reclaimed, the job should be allowed to be scheduled successfully.

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

### Comment by [@zhifei92](https://github.com/zhifei92) — 2025-10-27T08:52:39Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T10:42:27Z

/priority important-longterm

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-03-19T11:47:22Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle stale`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-04-18T12:16:56Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle rotten

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/
