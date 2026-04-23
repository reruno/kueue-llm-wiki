# Issue #5592: The preemption "In a multi-level cohort" test does not clear global resources after itself

**Summary**: The preemption "In a multi-level cohort" test does not clear global resources after itself

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5592

**Last updated**: 2025-10-07T08:16:19Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-06-10T06:12:36Z
- **Updated**: 2025-10-07T08:16:19Z
- **Closed**: 2025-10-07T08:16:17Z
- **Labels**: `lifecycle/stale`, `kind/cleanup`
- **Assignees**: [@kaisoz](https://github.com/kaisoz)
- **Comments**: 5

## Description

/kind cleanup
/king bug

**What would you like to be cleaned**:

This test https://github.com/kubernetes-sigs/kueue/blob/21f36d3e040c1cd192e3b552db399e77f302f6cb/test/integration/singlecluster/scheduler/preemption_test.go#L915 does not clear global resources after itself in AfterEach.

**Why is this needed**:

It risks conflicts with other tests, it also prevents running the preemption tests in a loop to detect flakes.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-10T06:12:54Z

cc @kaisoz @gabesaba

### Comment by [@kaisoz](https://github.com/kaisoz) — 2025-06-10T06:15:38Z

/assign

Thanks!

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-09-08T06:29:51Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-07T08:16:12Z

/close
done in https://github.com/kubernetes-sigs/kueue/pull/5867

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-10-07T08:16:18Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/5592#issuecomment-3375714187):

>/close
>done in https://github.com/kubernetes-sigs/kueue/pull/5867


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
