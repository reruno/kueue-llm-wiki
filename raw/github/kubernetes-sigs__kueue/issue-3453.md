# Issue #3453: [Flaky multikueue e2e test] The connection to a worker cluster is unreliable Should update the cluster status to reflect the connection state

**Summary**: [Flaky multikueue e2e test] The connection to a worker cluster is unreliable Should update the cluster status to reflect the connection state

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3453

**Last updated**: 2025-02-05T06:31:17Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-11-05T11:10:43Z
- **Updated**: 2025-02-05T06:31:17Z
- **Closed**: 2025-02-05T06:30:52Z
- **Labels**: `kind/bug`, `kind/flake`, `lifecycle/frozen`
- **Assignees**: _none_
- **Comments**: 5

## Description

**What happened**:

The test failed on unrelated branch: https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/3445/pull-kueue-test-multikueue-e2e-main/1853747452654391296

**What you expected to happen**:

No random failures

**How to reproduce it (as minimally and precisely as possible)**:

Use CI

**Anything else we need to know?**:

```
End To End MultiKueue Suite: kindest/node:v1.30.0: [It] MultiKueue when The connection to a worker cluster is unreliable Should update the cluster status to reflect the connection state expand_less	1m16s
{Timed out after 5.000s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/util/util.go:88 with:
NotFoundError expects an error failed [FAILED] Timed out after 5.000s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/util/util.go:88 with:
NotFoundError expects an error
In [AfterEach] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/multikueue/e2e_test.go:178 @ 11/05/24 10:44:58.957
}
```

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-11-05T18:36:19Z

/kind flake

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-02-03T18:56:05Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-04T21:40:18Z

I think that this can not be handled by ourselves since I guess this error comes from an infrastructure problem.
So, let me freeze for now.

/lifecycle frozen

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-05T06:30:48Z

I prefer to close it. It didnt happen for the last 3 months. Also, we already dont have logs to investigate. Finally, there have been some chnages to MK and the way we run tests which could have already resolved it ( like increasing the timeout to 10s).
/close
We will reopen when it re-occurs.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-02-05T06:30:53Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3453#issuecomment-2635810458):

>I prefer to close it. It didnt happen for the last 3 months. Also, we already dont have logs to investigate. Finally, there have been some chnages to MK and the way we run tests which could have already resolved it ( like increasing the timeout to 10s).
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
