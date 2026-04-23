# Issue #4505: [Flaky test] End To End Suite: kindest/node:v1.32.0: 4 failed e2e tests

**Summary**: [Flaky test] End To End Suite: kindest/node:v1.32.0: 4 failed e2e tests

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4505

**Last updated**: 2025-03-19T08:13:48Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@nasedil](https://github.com/nasedil)
- **Created**: 2025-03-05T13:35:02Z
- **Updated**: 2025-03-19T08:13:48Z
- **Closed**: 2025-03-19T08:13:47Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 3

## Description

/kind flake
<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->

**What happened**:
Flaky e2e tests in #4475 : https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/4475/pull-kueue-test-e2e-main-1-32/1897218139884621824
**What you expected to happen**:
test passes
**How to reproduce it (as minimally and precisely as possible)**:
run in CI
**Anything else we need to know?**:
End To End Suite: kindest/node:v1.32.0: [It] Pod groups when Single CQ Unscheduled Pod which is deleted can be replaced in group
```
{Timed out after 10.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/util/util.go:104 with:
Error matcher expects an error.  Got:
    <nil>: nil failed [FAILED] Timed out after 10.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/util/util.go:104 with:
Error matcher expects an error.  Got:
    <nil>: nil
In [AfterEach] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/pod_test.go:79 @ 03/05/25 09:43:00.078
}
```
might be related to #2529

End To End Suite: kindest/node:v1.32.0: [It] Pod groups when Single CQ should allow to schedule a group of diverse pods
```
{Timed out after 45.014s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/util/util.go:343 with:
it's finished
Expected
    <[]v1.Condition | len:2, cap:2>: [
        {
            Type: "QuotaReserved",
            Status: "True",
            ObservedGeneration: 1,
            LastTransitionTime: {
                Time: 2025-03-05T09:43:02Z,
            },
            Reason: "QuotaReserved",
            Message: "Quota reserved in ClusterQueue cq",
        },
        {
            Type: "Admitted",
            Status: "True",
            ObservedGeneration: 1,
            LastTransitionTime: {
                Time: 2025-03-05T09:43:02Z,
            },
            Reason: "Admitted",
            Message: "The workload is admitted",
        },
    ]
to have condition type Finished and status True failed [FAILED] Timed out after 45.014s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/util/util.go:343 with:
it's finished
Expected
    <[]v1.Condition | len:2, cap:2>: [
        {
            Type: "QuotaReserved",
            Status: "True",
            ObservedGeneration: 1,
            LastTransitionTime: {
                Time: 2025-03-05T09:43:02Z,
            },
            Reason: "QuotaReserved",
            Message: "Quota reserved in ClusterQueue cq",
        },
        {
            Type: "Admitted",
            Status: "True",
            ObservedGeneration: 1,
            LastTransitionTime: {
                Time: 2025-03-05T09:43:02Z,
            },
            Reason: "Admitted",
            Message: "The workload is admitted",
        },
    ]
to have condition type Finished and status True
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/pod_test.go:387 @ 03/05/25 09:43:47.731

There were additional failures detected after the initial failure. These are visible in the timeline
}
```
might be related to #1898


End To End Suite: kindest/node:v1.32.0: [It] Pod groups when Single CQ should allow to preempt the lower priority group
```
{Timed out after 45.000s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/pod_test.go:483 with:
Expected
    <v1.PodPhase>: Running
to equal
    <v1.PodPhase>: Failed failed [FAILED] Timed out after 45.000s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/pod_test.go:483 with:
Expected
    <v1.PodPhase>: Running
to equal
    <v1.PodPhase>: Failed
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/pod_test.go:485 @ 03/05/25 09:44:48.892

There were additional failures detected after the initial failure. These are visible in the timeline
}
```
might be related to #4434 

End To End Suite: kindest/node:v1.32.0: [It] TopologyAwareScheduling when Creating a Job requesting TAS should admit a Job via TAS
```
{Timed out after 45.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/tas_test.go:144 with:
Expected
    <[]v1.Condition | len:2, cap:2>: [
        {
            Type: "QuotaReserved",
            Status: "True",
            ObservedGeneration: 1,
            LastTransitionTime: {
                Time: 2025-03-05T09:45:01Z,
            },
            Reason: "QuotaReserved",
            Message: "Quota reserved in ClusterQueue cluster-queue",
        },
        {
            Type: "Admitted",
            Status: "True",
            ObservedGeneration: 1,
            LastTransitionTime: {
                Time: 2025-03-05T09:45:01Z,
            },
            Reason: "Admitted",
            Message: "The workload is admitted",
        },
    ]
to have condition type Finished and status True failed [FAILED] Timed out after 45.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/tas_test.go:144 with:
Expected
    <[]v1.Condition | len:2, cap:2>: [
        {
            Type: "QuotaReserved",
            Status: "True",
            ObservedGeneration: 1,
            LastTransitionTime: {
                Time: 2025-03-05T09:45:01Z,
            },
            Reason: "QuotaReserved",
            Message: "Quota reserved in ClusterQueue cluster-queue",
        },
        {
            Type: "Admitted",
            Status: "True",
            ObservedGeneration: 1,
            LastTransitionTime: {
                Time: 2025-03-05T09:45:01Z,
            },
            Reason: "Admitted",
            Message: "The workload is admitted",
        },
    ]
to have condition type Finished and status True
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/tas_test.go:145 @ 03/05/25 09:45:46.878
}
```

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-07T20:43:58Z

I extracted `End To End Suite: kindest/node:v1.32.0: [It] Pod groups when Single CQ should allow to preempt the lower priority group` to https://github.com/kubernetes-sigs/kueue/issues/4525 since there are some of similar testing failures.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-19T08:13:43Z

/close
Doing reset of e2e-related flakes as agreed in https://github.com/kubernetes-sigs/kueue/issues/4674#issuecomment-2734095182.

The reason is that we recently bumped up the job resources, and it is expected to help for most of the flakes were attributed to long termination of a job. So, this way we can avoid people looking into an already solved problem.

For more details check the PR [kubernetes/test-infra#34529](https://github.com/kubernetes/test-infra/pull/34529) as discussed here: [#4669](https://github.com/kubernetes-sigs/kueue/issues/4669).

If the failure re-occurs feel free to re-open or open a new one.

Also, feel free to re-open if you have some evidence / hints that constrained resources is not the reason for the failure.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-03-19T08:13:48Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4505#issuecomment-2735677424):

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
