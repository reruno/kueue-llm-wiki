# Issue #3366: Flaky Test: SchedulerWithWaitForPodsReady Short PodsReady timeout Should requeue a workload which exceeded the timeout to reach PodsReady=True [slow]

**Summary**: Flaky Test: SchedulerWithWaitForPodsReady Short PodsReady timeout Should requeue a workload which exceeded the timeout to reach PodsReady=True [slow]

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3366

**Last updated**: 2024-11-05T09:01:31Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2024-10-30T04:46:48Z
- **Updated**: 2024-11-05T09:01:31Z
- **Closed**: 2024-11-05T09:01:31Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 6

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

Failed `Scheduler with WaitForPodsReady Suite: [It] SchedulerWithWaitForPodsReady Short PodsReady timeout Should requeue a workload which exceeded the timeout to reach PodsReady=True [slow]`.

```shell
{Timed out after 5.001s.
the workload should be evicted after the timeout expires
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/integration/scheduler/podsready/scheduler_test.go:237 with:
Expected
    <[]v1.Condition | len:3, cap:4>: [
        {
            Type: "QuotaReserved",
            Status: "True",
            ObservedGeneration: 1,
            LastTransitionTime: {
                Time: 2024-10-29T18:18:27Z,
            },
            Reason: "QuotaReserved",
            Message: "Quota reserved in ClusterQueue prod-cq",
        },
        {
            Type: "Evicted",
            Status: "True",
            ObservedGeneration: 1,
            LastTransitionTime: {
                Time: 2024-10-29T18:18:28Z,
            },
            Reason: "PodsReadyTimeout",
            Message: "Exceeded the PodsReady timeout podsready-v4pth/prod1",
        },
        {
            Type: "Admitted",
            Status: "True",
            ObservedGeneration: 1,
            LastTransitionTime: {
                Time: 2024-10-29T18:18:27Z,
            },
            Reason: "Admitted",
            Message: "The workload is admitted",
        },
    ]
not to have condition Evicted and status True failed [FAILED] Timed out after 5.001s.
the workload should be evicted after the timeout expires
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/integration/scheduler/podsready/scheduler_test.go:237 with:
Expected
    <[]v1.Condition | len:3, cap:4>: [
        {
            Type: "QuotaReserved",
            Status: "True",
            ObservedGeneration: 1,
            LastTransitionTime: {
                Time: 2024-10-29T18:18:27Z,
            },
            Reason: "QuotaReserved",
            Message: "Quota reserved in ClusterQueue prod-cq",
        },
        {
            Type: "Evicted",
            Status: "True",
            ObservedGeneration: 1,
            LastTransitionTime: {
                Time: 2024-10-29T18:18:28Z,
            },
            Reason: "PodsReadyTimeout",
            Message: "Exceeded the PodsReady timeout podsready-v4pth/prod1",
        },
        {
            Type: "Admitted",
            Status: "True",
            ObservedGeneration: 1,
            LastTransitionTime: {
                Time: 2024-10-29T18:18:27Z,
            },
            Reason: "Admitted",
            Message: "The workload is admitted",
        },
    ]
not to have condition Evicted and status True
In [It] at: /home/prow/go/src/kubernetes-sigs/kueue/test/integration/scheduler/podsready/scheduler_test.go:243 @ 10/29/24 18:18:32.963
}
```

**What you expected to happen**:

No errors happened

**How to reproduce it (as minimally and precisely as possible)**:

https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-integration-main/1851324069593485312

<img width="1307" alt="Screenshot 2024-10-30 at 13 46 19" src="https://github.com/user-attachments/assets/bec24093-39ed-453a-b368-adf450ea9cd3">

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-10-30T04:46:54Z

/kind flake

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-11-04T06:31:49Z

/reopen

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-11-04T06:31:53Z

@tenzen-y: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3366#issuecomment-2453913692):

>/reopen
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-11-04T06:33:35Z

This does not seem to be resolved. Indeed, we observed the same error this weekend 2 times:

- https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-integration-main/1853317222689148928
- https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-integration-main/1852954831338082304

<img width="1384" alt="Screenshot 2024-11-04 at 15 33 02" src="https://github.com/user-attachments/assets/2ec39809-a1b0-42a7-a52c-9a099d1a3999">

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-11-05T07:07:11Z

Anyone can take a look?

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-11-05T07:10:28Z

/assign
