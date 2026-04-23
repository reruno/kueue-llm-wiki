# Issue #3370: Flaky Test: Workload controller when the workload has a maximum execution time set should deactivate the workload when the time expires

**Summary**: Flaky Test: Workload controller when the workload has a maximum execution time set should deactivate the workload when the time expires

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3370

**Last updated**: 2024-10-30T19:55:16Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2024-10-30T07:09:37Z
- **Updated**: 2024-10-30T19:55:16Z
- **Closed**: 2024-10-30T09:15:29Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 1

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
Core Controllers Suite: [It] Workload controller when the workload has a maximum execution time set should deactivate the workload when the time expires

```
{Timed out after 2.000s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/integration/controller/core/workload_controller_test.go:470 with:
Expected
    <[]v1.Condition | len:3, cap:4>: [
        {
            Type: "QuotaReserved",
            Status: "True",
            ObservedGeneration: 1,
            LastTransitionTime: {
                Time: 2024-10-30T07:01:39Z,
            },
            Reason: "QuotaReserved",
            Message: "Quota reserved in ClusterQueue cq",
        },
        {
            Type: "Admitted",
            Status: "True",
            ObservedGeneration: 1,
            LastTransitionTime: {
                Time: 2024-10-30T07:01:40Z,
            },
            Reason: "Admitted",
            Message: "The workload is admitted",
        },
        {
            Type: "DeactivationTarget",
            Status: "True",
            ObservedGeneration: 1,
            LastTransitionTime: {
                Time: 2024-10-30T07:01:42Z,
            },
            Reason: "MaximumExecutionTimeExceeded",
            Message: "exceeding the maximum execution time",
        },
    ]
to contain element matching
    <*matchers.BeComparableToMatcher | 0xc000a38780>: {
        Expected: <v1.Condition>{
            Type: "Evicted",
            Status: "True",
            ObservedGeneration: 0,
            LastTransitionTime: {
                Time: 0001-01-01T00:00:00Z,
            },
            Reason: "InactiveWorkloadMaximumExecutionTimeExceeded",
            Message: "The workload is deactivated due to exceeding the maximum execution time",
        },
        Options: [
            <*cmp.pathFilter | 0xc0001912f0>{
                core: {},
                fnc: 0x26988a0,
                opt: <cmp.ignore>{core: {}},
            },
        ],
    } failed [FAILED] Timed out after 2.000s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/integration/controller/core/workload_controller_test.go:470 with:
Expected
    <[]v1.Condition | len:3, cap:4>: [
        {
            Type: "QuotaReserved",
            Status: "True",
            ObservedGeneration: 1,
            LastTransitionTime: {
                Time: 2024-10-30T07:01:39Z,
            },
            Reason: "QuotaReserved",
            Message: "Quota reserved in ClusterQueue cq",
        },
        {
            Type: "Admitted",
            Status: "True",
            ObservedGeneration: 1,
            LastTransitionTime: {
                Time: 2024-10-30T07:01:40Z,
            },
            Reason: "Admitted",
            Message: "The workload is admitted",
        },
        {
            Type: "DeactivationTarget",
            Status: "True",
            ObservedGeneration: 1,
            LastTransitionTime: {
                Time: 2024-10-30T07:01:42Z,
            },
            Reason: "MaximumExecutionTimeExceeded",
            Message: "exceeding the maximum execution time",
        },
    ]
to contain element matching
    <*matchers.BeComparableToMatcher | 0xc000a38780>: {
        Expected: <v1.Condition>{
            Type: "Evicted",
            Status: "True",
            ObservedGeneration: 0,
            LastTransitionTime: {
                Time: 0001-01-01T00:00:00Z,
            },
            Reason: "InactiveWorkloadMaximumExecutionTimeExceeded",
            Message: "The workload is deactivated due to exceeding the maximum execution time",
        },
        Options: [
            <*cmp.pathFilter | 0xc0001912f0>{
                core: {},
                fnc: 0x26988a0,
                opt: <cmp.ignore>{core: {}},
            },
        ],
    }
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/integration/controller/core/workload_controller_test.go:479 @ 10/30/24 07:01:42.261
}
```

**What you expected to happen**:
No errors happened

**How to reproduce it (as minimally and precisely as possible)**:
https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/3367/pull-kueue-test-integration-main/1851518470143873024

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-10-30T19:55:14Z

/kind flake
