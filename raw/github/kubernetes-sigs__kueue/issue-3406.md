# Issue #3406: Flaky E2E Test: TopologyAwareScheduling when Creating a JobSet requesting TAS should admit a JobSet via TAS

**Summary**: Flaky E2E Test: TopologyAwareScheduling when Creating a JobSet requesting TAS should admit a JobSet via TAS

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3406

**Last updated**: 2024-11-01T12:27:30Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2024-10-31T20:09:40Z
- **Updated**: 2024-11-01T12:27:30Z
- **Closed**: 2024-11-01T12:27:30Z
- **Labels**: `kind/bug`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 1

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

End To End Suite: kindest/node:v1.28.9: [It] TopologyAwareScheduling when Creating a JobSet requesting TAS should admit a JobSet via TAS 

```
{Timed out after 5.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/tas_test.go:283 with:
Expected
    <[]v1.Condition | len:2, cap:4>: [
        {
            Type: "QuotaReserved",
            Status: "True",
            ObservedGeneration: 1,
            LastTransitionTime: {
                Time: 2024-10-31T20:04:59Z,
            },
            Reason: "QuotaReserved",
            Message: "Quota reserved in ClusterQueue cluster-queue",
        },
        {
            Type: "Admitted",
            Status: "True",
            ObservedGeneration: 1,
            LastTransitionTime: {
                Time: 2024-10-31T20:04:59Z,
            },
            Reason: "Admitted",
            Message: "The workload is admitted",
        },
    ]
to have condition Finished and status True failed [FAILED] Timed out after 5.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/tas_test.go:283 with:
Expected
    <[]v1.Condition | len:2, cap:4>: [
        {
            Type: "QuotaReserved",
            Status: "True",
            ObservedGeneration: 1,
            LastTransitionTime: {
                Time: 2024-10-31T20:04:59Z,
            },
            Reason: "QuotaReserved",
            Message: "Quota reserved in ClusterQueue cluster-queue",
        },
        {
            Type: "Admitted",
            Status: "True",
            ObservedGeneration: 1,
            LastTransitionTime: {
                Time: 2024-10-31T20:04:59Z,
            },
            Reason: "Admitted",
            Message: "The workload is admitted",
        },
    ]
to have condition Finished and status True
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/tas_test.go:284 @ 10/31/24 20:05:04.578
}
```

**What you expected to happen**:
No errors happened

**How to reproduce it (as minimally and precisely as possible)**:
https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/3384/pull-kueue-test-e2e-main-1-28/1852076939313942528

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

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-11-01T10:57:25Z

/assign
