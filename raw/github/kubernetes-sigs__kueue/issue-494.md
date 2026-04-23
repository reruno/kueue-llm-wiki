# Issue #494: Use a fake clock to avoid sleep in the podsready integration tests

**Summary**: Use a fake clock to avoid sleep in the podsready integration tests

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/494

**Last updated**: 2023-05-08T10:50:04Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2022-12-22T17:13:46Z
- **Updated**: 2023-05-08T10:50:04Z
- **Closed**: 2023-05-08T10:50:03Z
- **Labels**: _none_
- **Assignees**: [@mimowo](https://github.com/mimowo)
- **Comments**: 8

## Description

In the `podsready` integration test we sleep for a second to ensure the two created workloads have different creation timestamps: https://github.com/kubernetes-sigs/kueue/blob/e688dccea0c3683a35bd51e9d67dba40a3997d83/test/integration/scheduler/podsready/scheduler_test.go#L131. This can be avoided if the test could use a fake clock. This will require refactoring of some controllers to enable injecting the fake clock.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2023-01-03T08:01:08Z

/assign

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2023-04-03T08:32:45Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2023-05-03T09:05:50Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle rotten

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-05-08T09:56:18Z

/remove-lifecycle rotten

@mimowo Are there any leaving tasks to complete this issue?

### Comment by [@mimowo](https://github.com/mimowo) — 2023-05-08T10:30:03Z

I haven't started implementation (no PRs). It remains a question if the return is worth the investment. 

Currently, there are only two tests which use sleep 1s to order workloads based on their creation time (https://github.com/kubernetes-sigs/kueue/search?q=time.Sleep). Given that there are only 2s to gain, and the integration tests which use real clocks are more valuable, we can defer the refactoring. So, I suggest to close it for now and reopen when we see a need, or bigger benefit.

Also, with the latest lookup to the `Evicted.LastTranstionTime` condition we may eliminate the sleeps, although in a workaround-ish way.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-05-08T10:42:37Z

> Given that there are only 2s to gain, and the integration tests which use real clocks are more valuable, we can defer the refactoring. 

It makes sense.

> So, I suggest to close it for now and reopen when we see a need, or bigger benefit.

To avoid forgetting this issue, adding a `lifecycle/frozen` label might be better instead of closing the issue although I'm also ok with closing this.

### Comment by [@mimowo](https://github.com/mimowo) — 2023-05-08T10:50:00Z

/close 
Let me close as this will probably not be needed for a while and can make the backlog if issues look cleaner. We will reassess the need in the future.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-05-08T10:50:04Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/494#issuecomment-1538166943):

>/close 
>Let me close as this will probably not be needed for a while and can make the backlog if issues look cleaner. We will reassess the need in the future.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
