# Issue #9438: [flaky test] MultiKueue with TopologyAwareScheduling when Creating a Job with TAS requirements Should admit a Job and assign topology in the worker cluster

**Summary**: [flaky test] MultiKueue with TopologyAwareScheduling when Creating a Job with TAS requirements Should admit a Job and assign topology in the worker cluster

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9438

**Last updated**: 2026-02-27T16:13:34Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-02-24T07:58:08Z
- **Updated**: 2026-02-27T16:13:34Z
- **Closed**: 2026-02-27T16:13:34Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 1

## Description

**Which test is flaking?**:

MultiKueue with TopologyAwareScheduling when Creating a Job with TAS requirements Should admit a Job and assign topology in the worker cluster 

**Link to failed CI job or steps to reproduce locally**:

https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-multikueue-release-0-16/2026170270561079296#1:build-log.txt%3A2024

**Failure message or logs**:
```
End To End MultiKueue Suite: kindest/node:v1.35.0: [It] MultiKueue with TopologyAwareScheduling when Creating a Job with TAS requirements Should admit a Job and assign topology in the worker cluster expand_less	1m12s
{Timed out after 45.001s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/multikueue/tas_test.go:290 with:
Expected
    <[]v1.Condition | len:2, cap:2>: [
        {
            Type: "QuotaReserved",
            Status: "True",
            ObservedGeneration: 1,
            LastTransitionTime: {
                Time: 2026-02-24T05:58:03Z,
            },
            Reason: "QuotaReserved",
            Message: "Quota reserved in ClusterQueue q1",
        },
        {
            Type: "Admitted",
            Status: "True",
            ObservedGeneration: 1,
            LastTransitionTime: {
                Time: 2026-02-24T05:58:05Z,
            },
            Reason: "Admitted",
            Message: "The workload is admitted",
        },
    ]
to have condition type Finished, status True and reason Succeeded failed [FAILED] Timed out after 45.001s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/multikueue/tas_test.go:290 with:
Expected
    <[]v1.Condition | len:2, cap:2>: [
        {
            Type: "QuotaReserved",
            Status: "True",
            ObservedGeneration: 1,
            LastTransitionTime: {
                Time: 2026-02-24T05:58:03Z,
            },
            Reason: "QuotaReserved",
            Message: "Quota reserved in ClusterQueue q1",
        },
        {
            Type: "Admitted",
            Status: "True",
            ObservedGeneration: 1,
            LastTransitionTime: {
                Time: 2026-02-24T05:58:05Z,
            },
            Reason: "Admitted",
            Message: "The workload is admitted",
        },
    ]
to have condition type Finished, status True and reason Succeeded
In [It] at: /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/multikueue/tas_test.go:291 @ 02/24/26 05:58:59.326
}
```

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-02-25T03:41:56Z

This was observed again in https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-multikueue-release-0-15/2026474025085046784
