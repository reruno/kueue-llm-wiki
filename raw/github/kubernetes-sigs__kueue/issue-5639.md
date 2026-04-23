# Issue #5639: [flaky test]  JobSet when Creating a JobSet Should run a jobSet if admitted

**Summary**: [flaky test]  JobSet when Creating a JobSet Should run a jobSet if admitted

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5639

**Last updated**: 2025-07-03T10:01:28Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-06-13T07:42:39Z
- **Updated**: 2025-07-03T10:01:28Z
- **Closed**: 2025-07-03T10:01:28Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mykysha](https://github.com/mykysha)
- **Comments**: 3

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may sult in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

flake https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-release-0-12-1-32/1933255326035873792

**What you expected to happen**:
no failure
**How to reproduce it (as minimally and precisely as possible)**:
ci
**Anything else we need to know?**:

```
{Timed out after 45.000s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/singlecluster/jobset_test.go:99 with:
Expected
    <[]v1.Condition | len:2, cap:2>: [
        {
            Type: "QuotaReserved",
            Status: "True",
            ObservedGeneration: 1,
            LastTransitionTime: {
                Time: 2025-06-12T20:34:34Z,
            },
            Reason: "QuotaReserved",
            Message: "Quota reserved in ClusterQueue cluster-queue",
        },
        {
            Type: "Admitted",
            Status: "True",
            ObservedGeneration: 1,
            LastTransitionTime: {
                Time: 2025-06-12T20:34:34Z,
            },
            Reason: "Admitted",
            Message: "The workload is admitted",
        },
    ]
to have condition type Finished, status True and reason Succeeded failed [FAILED] Timed out after 45.000s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/singlecluster/jobset_test.go:99 with:
Expected
    <[]v1.Condition | len:2, cap:2>: [
        {
            Type: "QuotaReserved",
            Status: "True",
            ObservedGeneration: 1,
            LastTransitionTime: {
                Time: 2025-06-12T20:34:34Z,
            },
            Reason: "QuotaReserved",
            Message: "Quota reserved in ClusterQueue cluster-queue",
        },
        {
            Type: "Admitted",
            Status: "True",
            ObservedGeneration: 1,
            LastTransitionTime: {
                Time: 2025-06-12T20:34:34Z,
            },
            Reason: "Admitted",
            Message: "The workload is admitted",
        },
    ]
to have condition type Finished, status True and reason Succeeded
In [It] at: /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/singlecluster/jobset_test.go:100 @ 06/12/25 20:35:19.683
}
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-13T07:42:47Z

cc @mbobrovskyi @mszadkow

### Comment by [@mykysha](https://github.com/mykysha) — 2025-06-17T08:49:31Z

/assign

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-06-17T11:29:40Z

/kind flake
