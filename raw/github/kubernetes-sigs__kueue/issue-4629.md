# Issue #4629: Flaky Test: Pod groups when Single CQ should admit group that fits

**Summary**: Flaky Test: Pod groups when Single CQ should admit group that fits

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4629

**Last updated**: 2025-03-19T08:11:22Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-03-16T11:06:54Z
- **Updated**: 2025-03-19T08:11:22Z
- **Closed**: 2025-03-19T08:11:20Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 3

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

Failed `End To End Suite: kindest/node:v1.29.4: [It] Pod groups when Single CQ should admit group that fits` on periodic Job:

```
{Timed out after 45.000s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/util/util.go:343 with:
it's finished
Expected
    <[]v1.Condition | len:2, cap:2>: [
        {
            Type: "QuotaReserved",
            Status: "True",
            ObservedGeneration: 1,
            LastTransitionTime: {
                Time: 2025-03-16T09:52:23Z,
            },
            Reason: "QuotaReserved",
            Message: "Quota reserved in ClusterQueue cq",
        },
        {
            Type: "Admitted",
            Status: "True",
            ObservedGeneration: 1,
            LastTransitionTime: {
                Time: 2025-03-16T09:52:23Z,
            },
            Reason: "Admitted",
            Message: "The workload is admitted",
        },
    ]
to have condition type Finished and status True failed [FAILED] Timed out after 45.000s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/util/util.go:343 with:
it's finished
Expected
    <[]v1.Condition | len:2, cap:2>: [
        {
            Type: "QuotaReserved",
            Status: "True",
            ObservedGeneration: 1,
            LastTransitionTime: {
                Time: 2025-03-16T09:52:23Z,
            },
            Reason: "QuotaReserved",
            Message: "Quota reserved in ClusterQueue cq",
        },
        {
            Type: "Admitted",
            Status: "True",
            ObservedGeneration: 1,
            LastTransitionTime: {
                Time: 2025-03-16T09:52:23Z,
            },
            Reason: "Admitted",
            Message: "The workload is admitted",
        },
    ]
to have condition type Finished and status True
In [It] at: /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/singlecluster/pod_test.go:112 @ 03/16/25 09:53:08.556

There were additional failures detected after the initial failure. These are visible in the timeline
}
```

**What you expected to happen**:

no errors.

**How to reproduce it (as minimally and precisely as possible)**:

https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-main-1-29/1901206729471823872

<img width="1479" alt="Image" src="https://github.com/user-attachments/assets/9d7899ae-9984-492f-81bc-8238ec320139" />

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-16T11:07:04Z

/kind flake

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-19T08:11:16Z

/close
Doing reset of e2e-related flakes as agreed in https://github.com/kubernetes-sigs/kueue/issues/4674#issuecomment-2734095182.

The reason is that we recently bumped up the job resources, and it is expected to help for most of the flakes were attributed to long termination of a job. So, this way we can avoid people looking into an already solved problem.

For more details check the PR [kubernetes/test-infra#34529](https://github.com/kubernetes/test-infra/pull/34529) as discussed here: [#4669](https://github.com/kubernetes-sigs/kueue/issues/4669).

If the failure re-occurs feel free to re-open or open a new one.

Also, feel free to re-open if you have some evidence / hints that constrained resources is not the reason for the failure.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-03-19T08:11:21Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4629#issuecomment-2735670858):

>/close
>Doing reset of e2e-related flakes as agreed in https://github.com/kubernetes-sigs/kueue/issues/4674#issuecomment-2734095182.
>
>The reason is that we recently bumped up the job resources, and it is expected to help for most of the flakes were attributed to long termination of a job. So, this way we can avoid people looking into an already solved problem.
>
>For more details check the PR [kubernetes/test-infra#34529](https://github.com/kubernetes/test-infra/pull/34529) as discussed here: [#4669](https://github.com/kubernetes-sigs/kueue/issues/4669).
>
>If the failure re-occurs feel free to re-open or open a new one.
>
>Also, feel free to re-open if you have some evidence / hints that constrained resources is not the reason for the failure.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
