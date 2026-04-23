# Issue #2097: Testgrid for integration tests is broken

**Summary**: Testgrid for integration tests is broken

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2097

**Last updated**: 2024-05-13T18:04:50Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2024-04-29T14:28:42Z
- **Updated**: 2024-05-13T18:04:50Z
- **Closed**: 2024-05-13T18:04:49Z
- **Labels**: `kind/bug`
- **Assignees**: [@gabesaba](https://github.com/gabesaba)
- **Comments**: 11

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

The testgrid shows error for `Overall` and doesn't show the individual tests.

Other testgrids (E2E, unit) look fine.

**What you expected to happen**:

A line for every test.

**How to reproduce it (as minimally and precisely as possible)**:

https://testgrid.k8s.io/sig-scheduling#pull-kueue-test-integration-main&width=20

**Anything else we need to know?**:

We have lost history for the last time it worked.

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-04-29T14:38:11Z

The release-0.6 branch looks healthy https://testgrid.k8s.io/sig-scheduling#pull-kueue-test-integration-release-0-6&width=20

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-04-29T14:43:07Z

The only difference in the presubmit configuration is that `main` is running on golang 1.22

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-04-29T16:04:49Z

/assign @gabesaba

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-04-29T16:04:51Z

@alculquicondor: GitHub didn't allow me to assign the following users: gabesaba.

Note that only [kubernetes-sigs members](https://github.com/orgs/kubernetes-sigs/people) with read permissions, repo collaborators and people who have commented on this issue/PR can be assigned. Additionally, issues/PRs can only have 10 assignees at the same time.
For more information please see [the contributor guide](https://git.k8s.io/community/contributors/guide/first-contribution.md#issue-assignment-in-github)

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/2097#issuecomment-2083123762):

>/assign @gabesaba 


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@gabesaba](https://github.com/gabesaba) — 2024-04-29T16:06:49Z

Probably because junit output is too large - there's an error message that it is malformed since over 100MB

We could either bump this limit, or reduce verbosity

### Comment by [@gabesaba](https://github.com/gabesaba) — 2024-04-29T16:17:49Z

/assign @gabesaba

### Comment by [@gabesaba](https://github.com/gabesaba) — 2024-04-29T17:47:58Z

removing -v ginkgo flag from test-integration target, junit.xml went from 204MB to 88MB. This would fix issue, but we're still close to the limit.

Looking next into any particularly spammy logs

### Comment by [@gabesaba](https://github.com/gabesaba) — 2024-04-30T08:29:03Z

Much of the size can be attributed to a few tests. Below are the tests with output > 1MB (after HTML unescaping, so the actual size is larger)

| size | test name | suite name
| -- | -- | --
| 40.906763MB | Scheduler when Queueing with StrictFIFO Should report pending workloads properly when blocked | Scheduler Suite
| 26.427274MB | Scheduler when Queueing with StrictFIFO Should allow mutating the requeueingStrategy | Scheduler Suite
| 16.314269MB | Scheduler when Queueing with StrictFIFO Should schedule workloads by their priority strictly | Scheduler Suite
| 10.625324MB | Preemption In a cohort with StrictFIFO Should reclaim from cohort even if another CQ has pending workloads | Scheduler Suite
| 10.117538MB | Scheduler when Preemption is enabled Admits workloads respecting fair share | Scheduler Fair Sharing Suite
| 7.241802MB | Scheduler when Using cohorts for sharing unused resources Should start workloads that are under min quota before borrowing | Scheduler Suite
| 3.692636MB | Scheduler when Queueing with StrictFIFO Pending workload with StrictFIFO doesn't block other CQ from borrowing from a third CQ | Scheduler Suite
| 2.651555MB | Preemption In a ClusterQueue that is part of a cohort Should preempt all necessary workloads in concurrent scheduling with different priorities | Scheduler Suite
| 2.404417MB | Preemption In a single ClusterQueue Should preempt Workloads with lower priority when there is not enough quota | Scheduler Suite
| 2.389974MB | Preemption When lending limit enabled Should be able to preempt when lending limit enabled | Scheduler Suite
| 2.365368MB | Preemption In a single ClusterQueue Should preempt newer Workloads with the same priority when there is not enough quota | Scheduler Suite
| 2.359989MB | Scheduler when Using cohorts for sharing unused resources Should preempt before try next flavor | Scheduler Suite
| 2.338912MB | Scheduler when Scheduling workloads on clusterQueues Should admit workloads when resources are dynamically reclaimed | Scheduler Suite
| 2.167817MB | Preemption In a ClusterQueue that is part of a cohort Should preempt all necessary workloads in concurrent scheduling with the same priority | Scheduler Suitep
| 2.062887MB | Preemption When most quota is in a shared ClusterQueue in a cohort should allow preempting workloads while borrowing | Scheduler Suite
| 1.989364MB | Preemption In a ClusterQueue that is part of a cohort Should preempt Workloads in the cohort borrowing quota | when the ClusterQueue is using less than nominal quota | Scheduler Suite

### Comment by [@gabesaba](https://github.com/gabesaba) — 2024-04-30T11:46:28Z

within those tests, attributing output to certain lines

|size | #lines | line 
| -- | -- | --
| 10MB | 86649 | queue/manager.go:475
| 32MB | 93902 | [scheduler/logging.go:40](https://github.com/kubernetes-sigs/kueue/blob/28d9bd0fc777de37ef32f3354cdb63e61a71e220/pkg/scheduler/logging.go#L40)
| 38MB | 93985 | [recorder/recorder.go:104](https://github.com/kubernetes-sigs/kueue/blob/28d9bd0fc777de37ef32f3354cdb63e61a71e220/pkg/scheduler/flavorassigner/flavorassigner.go#L92-L95)
| 27MB | 93826 | [scheduler/scheduler.go:617](https://github.com/kubernetes-sigs/kueue/blob/28d9bd0fc777de37ef32f3354cdb63e61a71e220/pkg/scheduler/scheduler.go#L617)
| 5MB | 20762 | preemption/preemption.go:175
| 23MB | 62530 | [scheduler/scheduler.go:262](https://github.com/kubernetes-sigs/kueue/blob/28d9bd0fc777de37ef32f3354cdb63e61a71e220/pkg/scheduler/scheduler.go#L262)

We're repeatedly reconciling unschedulable workloads without any backoff. Should there be a backoff here? I imagine that a backoff of even a fraction of a second would drastically reduce the logging output here

### Comment by [@gabesaba](https://github.com/gabesaba) — 2024-04-30T12:35:21Z

212MB to 15MB after changing [scheduler.go:128](https://github.com/kubernetes-sigs/kueue/blob/28d9bd0fc777de37ef32f3354cdb63e61a71e220/pkg/scheduler/scheduler.go#L128) to 10ms

```
$ wc -c before.xml fix.xml 
211955097 before.xml
 14650361 fix.xml
```

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-04-30T13:08:02Z

Uhm.... maybe we can use a [`NewItemExponentialFailureRateLimiter`](https://github.com/kubernetes/kubernetes/blob/02365ecec1cb1ddf993cf4ed12407737db950cea/staging/src/k8s.io/client-go/util/workqueue/default_rate_limiters.go#L95) to have a backoff when we couldn't admit any workload in that iteration. And we clear the backoff anytime we successfully admit something.
