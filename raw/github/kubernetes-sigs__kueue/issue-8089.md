# Issue #8089: MultiKueue: Kueue admission gets stuck when ProvisioningRequests keeps failing

**Summary**: MultiKueue: Kueue admission gets stuck when ProvisioningRequests keeps failing

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8089

**Last updated**: 2026-01-22T09:19:27Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-12-05T09:32:51Z
- **Updated**: 2026-01-22T09:19:27Z
- **Closed**: 2026-01-22T09:19:26Z
- **Labels**: `kind/bug`, `priority/important-soon`, `area/multikueue`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 10

## Description


**What happened**:

When MultiKueue chooses a worker cluster, and the worker fails to provision using ProvisioningRequest due to stockout, then the admission is essentially stuck.

**What you expected to happen**:

I expect that MultiKueue should repeat the process of choosing the worker cluster if the admission fails and the worker cluster loses reservation, eg due to failing ProvisioningRequest.

Alternatively we can wait until the workload on the worker cluster is Deactivated. This would allow a couple of ProvisioningRequest retries on the worker cluster. However, we can leave it for later as a configuration option.

**How to reproduce it (as minimally and precisely as possible)**:

Create a worker cluster using ProvsioningRequest which can never be fulfield.

**Anything else we need to know?**:

This looks related to the preemption issue https://github.com/kubernetes-sigs/kueue/issues/7350

For start I think we could handle both cases by just restarting admission at the manager level when that happens.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-17T13:24:16Z

As I synced with @mwielgus we could start with the simple fix where any eviction (lost of quota) at the worker results in returning the control to the manager cluster. This will largely mitigate the issue with AdmissionChecks, and preemption.

### Comment by [@mwielgus](https://github.com/mwielgus) — 2025-12-17T13:33:18Z

Yes, the default behavior for preempted MK workloads should be getting back to square one and to admission on the management cluster level. Then if individual worker cluster has issues (for whatever reasons - failing checks, preemptions, etc) other may pick up the workload.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T08:19:43Z

/area multikueue
/priority important-soon

### Comment by [@mszadkow](https://github.com/mszadkow) — 2026-01-19T12:06:05Z

/assign

### Comment by [@mszadkow](https://github.com/mszadkow) — 2026-01-19T12:17:25Z

Running tests after merge of https://github.com/kubernetes-sigs/kueue/pull/8477.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-19T12:19:20Z

Thank you! I think assuming the recent changes : re do admission in case of failure, and waiting for admission rather than reservation this should be covered. So we could close

### Comment by [@mszadkow](https://github.com/mszadkow) — 2026-01-21T09:08:51Z

I have tested 2 scenarios:

1. Admitted workload of the remote worker was set to inactive thus triggering eviction and in result re-admission of the workload.
Note: re-admitted workload keeps the name of the original workload as the manager workload was re-queued and not re-created.

2. I have tried to reproduce the scenario when failed ProvisionRequest keeps the workload stuck (request 2 gpu while only 1 can is available in the pool).
However I was not able to do that, in the situation when none of the workers has enough resources the manager workload will not receive the [reservingRemote](https://github.com/kubernetes-sigs/kueue/blob/7b1f89403a0c14d310b657c2f614d3887b7eecd4/pkg/controller/admissionchecks/multikueue/workload.go#L433). 
I think the real fix comes from [here](https://github.com/kubernetes-sigs/kueue/pull/8592).
As the worker workload has the following status while the ProvReq on the worker keeps failing:
```
status:
  admission:
    clusterQueue: dws-cluster-queue
    podSetAssignments:
    - count: 2
      delayedTopologyRequest: Pending
      flavors:
        cpu: tas-flavor
        memory: tas-flavor
        nvidia.com/gpu: tas-flavor
      name: main
      resourceUsage:
        cpu: 200m
        memory: 200Mi
        nvidia.com/gpu: "2"
  admissionChecks:
  - lastTransitionTime: "2026-01-20T13:04:25Z"
    message: 'Reset to Pending after eviction. Previously: Retry'
    name: dws-prov
    requeueAfterSeconds: 60
    retryCount: 1
    state: Pending
  conditions:
  - lastTransitionTime: "2026-01-20T13:02:16Z"
    message: Quota reserved in ClusterQueue dws-cluster-queue
    observedGeneration: 1
    reason: QuotaReserved
    status: "True"
    type: QuotaReserved
  - lastTransitionTime: "2026-01-20T13:04:25Z"
    message: At least one admission check is false
    observedGeneration: 1
    reason: AdmissionCheck
    status: "True"
    type: Evicted
  schedulingStats:
    evictions:
    - count: 1
      reason: AdmissionCheck
      underlyingCause: ""
```
WIth the mentioned fix we no longer rely on the `QuotaReserved` rather on `Admitted`

### Comment by [@mszadkow](https://github.com/mszadkow) — 2026-01-22T09:17:24Z

My conclusion is that we can close the ticket

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-22T09:19:19Z

/close
Thank you for testing and confirming it works in the foreseen cases. We will open dedicated issues if users encounter some specific problems.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-01-22T09:19:27Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/8089#issuecomment-3783362879):

>/close
>Thank you for testing and confirming it works in the foreseen cases. We will open dedicated issues if users encounter some specific problems.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
