# Issue #1344: ClusterQueue not considering next ResourceFlavor when whenCanPreempt: Preempt is set

**Summary**: ClusterQueue not considering next ResourceFlavor when whenCanPreempt: Preempt is set

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1344

**Last updated**: 2023-11-27T20:43:26Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@nstogner](https://github.com/nstogner)
- **Created**: 2023-11-17T22:47:27Z
- **Updated**: 2023-11-27T20:43:26Z
- **Closed**: 2023-11-27T20:43:26Z
- **Labels**: `kind/bug`
- **Assignees**: [@alculquicondor](https://github.com/alculquicondor)
- **Comments**: 6

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

Setting `whenCanPreempt: Preempt` in a ClusterQueue with 2 resource flavors appears to stop the ClusterQueue from considering the 2nd resource flavor.

**How to reproduce it (as minimally and precisely as possible)**:

* Created a cluster queue with 2 resource flavors
* Each resource flavor has quota for 2 cpus
* Submitting 3 jobs that require 1 cpu each (via Job or plain Pod API) will result in 2 being admitted and 1 not

NOTE: ClusterQueue is configured as follows:

```yaml
  preemption:
    reclaimWithinCohort: Any
    withinClusterQueue: LowerOrNewerEqualPriority
  flavorFungibility:
    whenCanBorrow: Borrow
    whenCanPreempt: Preempt
```

**What you expected to happen**:

All 3 jobs should be admitted (quota from resource flavor 2 should be used).

**Anything else we need to know?**:

Condition of non-admitted Workload:

```
status:
  conditions:
  - lastTransitionTime: "2023-11-17T22:37:24Z"
    message: 'couldn''t assign flavors to pod set main: borrowing limit for cpu in
      flavor flav-1 exceeded'
    reason: Pending
    status: "False"
    type: QuotaReserved
```

**Environment**:
- Kubernetes version (use `kubectl version`):
```
Client Version: version.Info{Major:"1", Minor:"27", GitVersion:"v1.27.4", GitCommit:"fa3d7990104d7c1f16943a67f11b154b71f6a132", GitTreeState:"clean", BuildDate:"2023-07-19T12:20:54Z", GoVersion:"go1.20.6", Compiler:"gc", Platform:"darwin/amd64"}
Kustomize Version: v5.0.1
Server Version: version.Info{Major:"1", Minor:"27", GitVersion:"v1.27.3-gke.100", GitCommit:"6466b51b762a5c49ae3fb6c2c7233ffe1c96e48c", GitTreeState:"clean", BuildDate:"2023-06-23T09:27:28Z", GoVersion:"go1.20.5 X:boringcrypto", Compiler:"gc", Platform:"linux/amd64"}
```
- Kueue version (use `git describe --tags --dirty --always`): Built from main (commit `4405e35b51bb153611e0a01f48884aa2c131055c` - deployed with manifests from `0.5.0`)
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@nstogner](https://github.com/nstogner) — 2023-11-17T22:51:06Z

I will plan on submitting a test case reproducing this issue if nobody has gotten to it at my next chance - might be Monday.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-11-20T14:24:54Z

/assign

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-11-20T15:09:09Z

cc @KunWuLuan if you have any ideas.

### Comment by [@KunWuLuan](https://github.com/KunWuLuan) — 2023-11-21T01:34:00Z

I will try to reproduce the case today.

### Comment by [@KunWuLuan](https://github.com/KunWuLuan) — 2023-11-21T12:04:31Z

There is some problem in cq.AllocatableResourceGeneration and wl.LastAssignment.ClusterQueueGeneration. I am working on it. cc @alculquicondor

### Comment by [@KunWuLuan](https://github.com/KunWuLuan) — 2023-11-21T12:28:01Z

It seem that cluster queue is updated and cq.AllocatableResourceGeneration is added after the third job is scheduled. After I add a check about RGs, the problem is solved.
