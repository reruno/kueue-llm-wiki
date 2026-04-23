# Issue #5034: Flaky E2E Test: TopologyAwareScheduling when Creating a Job requesting TAS should admit a Job via TAS

**Summary**: Flaky E2E Test: TopologyAwareScheduling when Creating a Job requesting TAS should admit a Job via TAS

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5034

**Last updated**: 2025-08-07T08:36:35Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2025-04-17T09:35:44Z
- **Updated**: 2025-08-07T08:36:35Z
- **Closed**: 2025-08-07T08:36:34Z
- **Labels**: `kind/bug`, `lifecycle/stale`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 4

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->

/kind flake


**What happened**:

End To End Suite: kindest/node:v1.32.3: [It] TopologyAwareScheduling when Creating a Job requesting TAS should admit a Job via TAS 

```
{Timed out after 45.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/tas_test.go:140 with:
Expected
    <[]v1.Condition | len:2, cap:2>: [
        {
            Type: "QuotaReserved",
            Status: "True",
            ObservedGeneration: 1,
            LastTransitionTime: {
                Time: 2025-04-17T09:09:04Z,
            },
            Reason: "QuotaReserved",
            Message: "Quota reserved in ClusterQueue cluster-queue",
        },
        {
            Type: "Admitted",
            Status: "True",
            ObservedGeneration: 1,
            LastTransitionTime: {
                Time: 2025-04-17T09:09:04Z,
            },
            Reason: "Admitted",
            Message: "The workload is admitted",
        },
    ]
to have condition type Finished and status True failed [FAILED] Timed out after 45.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/tas_test.go:140 with:
Expected
    <[]v1.Condition | len:2, cap:2>: [
        {
            Type: "QuotaReserved",
            Status: "True",
            ObservedGeneration: 1,
            LastTransitionTime: {
                Time: 2025-04-17T09:09:04Z,
            },
            Reason: "QuotaReserved",
            Message: "Quota reserved in ClusterQueue cluster-queue",
        },
        {
            Type: "Admitted",
            Status: "True",
            ObservedGeneration: 1,
            LastTransitionTime: {
                Time: 2025-04-17T09:09:04Z,
            },
            Reason: "Admitted",
            Message: "The workload is admitted",
        },
    ]
to have condition type Finished and status True
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/tas_test.go:141 @ 04/17/25 09:09:49.382

There were additional failures detected after the initial failure. These are visible in the timeline
}
```

**What you expected to happen**:

No errors.

**How to reproduce it (as minimally and precisely as possible)**:

https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/5031/pull-kueue-test-e2e-main-1-32/1912792918750400512

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-07-16T09:44:43Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle stale`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-07-17T05:38:06Z

/remove-lifecycle

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-07T08:36:30Z

/close
We no longer have logs to investigate, and also there were multiple fixes to TAS since reported.
I suggest to reopen if this re-occurs.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-08-07T08:36:35Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/5034#issuecomment-3163104141):

>/close
>We no longer have logs to investigate, and also there were multiple fixes to TAS since reported.
>I suggest to reopen if this re-occurs.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
