# Issue #9714: Pod groups when Single CQ Should only admit a complete group

**Summary**: Pod groups when Single CQ Should only admit a complete group

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9714

**Last updated**: 2026-04-17T17:13:22Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-03-06T12:47:01Z
- **Updated**: 2026-04-17T17:13:22Z
- **Closed**: 2026-04-17T17:13:21Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@sohankunkerkar](https://github.com/sohankunkerkar), [@PannagaRao](https://github.com/PannagaRao)
- **Comments**: 4

## Description

<!--
Please use this template for reporting flaky tests.
Links to specific failures in Prow are appreciated.
-->

**Which test is flaking?**:
Pod groups when Single CQ Should only admit a complete group
**Link to failed CI job or steps to reproduce locally**:
https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-release-0-16-1-35/2029796010150072320
**Failure message or logs**:
```
End To End Suite: kindest/node:v1.35.0: [It] Pod groups when Single CQ Should only admit a complete group [area:singlecluster, feature:pod] expand_less	1m30s
{Timed out after 45.001s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/util/util.go:448 with:
it's finished
Expected
    <[]v1.Condition | len:2, cap:2>: [
        {
            Type: "QuotaReserved",
            Status: "True",
            ObservedGeneration: 1,
            LastTransitionTime: {
                Time: 2026-03-06T06:08:12Z,
            },
            Reason: "QuotaReserved",
            Message: "Quota reserved in ClusterQueue cq-pod-e2e-kzf8r",
        },
        {
            Type: "Admitted",
            Status: "True",
            ObservedGeneration: 1,
            LastTransitionTime: {
                Time: 2026-03-06T06:08:12Z,
            },
            Reason: "Admitted",
            Message: "The workload is admitted",
        },
    ]
to have condition type Finished and status True failed [FAILED] Timed out after 45.001s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/util/util.go:448 with:
it's finished
Expected
    <[]v1.Condition | len:2, cap:2>: [
        {
            Type: "QuotaReserved",
            Status: "True",
            ObservedGeneration: 1,
            LastTransitionTime: {
                Time: 2026-03-06T06:08:12Z,
            },
            Reason: "QuotaReserved",
            Message: "Quota reserved in ClusterQueue cq-pod-e2e-kzf8r",
        },
        {
            Type: "Admitted",
            Status: "True",
            ObservedGeneration: 1,
            LastTransitionTime: {
                Time: 2026-03-06T06:08:12Z,
            },
            Reason: "Admitted",
            Message: "The workload is admitted",
        },
    ]
to have condition type Finished and status True
In [It] at: /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/singlecluster/pod_test.go:178 @ 03/06/26 06:08:57.107
}
```

**Anything else we need to know?**:

Same build as https://github.com/kubernetes-sigs/kueue/issues/9713

## Discussion

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-03-06T20:53:41Z

/assign

### Comment by [@PannagaRao](https://github.com/PannagaRao) — 2026-03-26T04:53:15Z

/assign @PannagaRao 

Working on bumping timeout to LongTimeout (90s)  for ExpectWorkloadToFinish — testing with 200 iterations in [#10086.](https://github.com/kubernetes-sigs/kueue/pull/10086)

### Comment by [@mimowo](https://github.com/mimowo) — 2026-04-17T17:13:14Z

I think this is already fixed, because it was using the 45 timeout, but now the group is using LongTimeout: https://github.com/kubernetes-sigs/kueue/blob/main/test/e2e/singlecluster/pod_test.go#L178

After https://github.com/kubernetes-sigs/kueue/pull/10430

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-04-17T17:13:22Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/9714#issuecomment-4269923950):

>I think this is already fixed, because it was using the 45 timeout, but now the group is using LongTimeout: https://github.com/kubernetes-sigs/kueue/blob/main/test/e2e/singlecluster/pod_test.go#L178
>
>After https://github.com/kubernetes-sigs/kueue/pull/10430
>
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
