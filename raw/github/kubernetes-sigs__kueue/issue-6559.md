# Issue #6559: Pending Workloads in integration tests occasionally have incorrect `QuotaReserved` condition

**Summary**: Pending Workloads in integration tests occasionally have incorrect `QuotaReserved` condition

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6559

**Last updated**: 2025-12-10T14:28:37Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@PBundyra](https://github.com/PBundyra)
- **Created**: 2025-08-12T12:39:02Z
- **Updated**: 2025-12-10T14:28:37Z
- **Closed**: 2025-12-10T14:28:36Z
- **Labels**: `kind/bug`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 4

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->

**What happened**:
When running integration tests, pending Workloads are not discovered by the `ExpectWorkloadsToBePending` util function, even if the workload is indeed pending and the `ExpectPendingWorkloadsMetric` return the correct value.

**What you expected to happen**:
Pending Workloads to have `QuotaReserved=false` condition

**How to reproduce it (as minimally and precisely as possible)**:
No clear scenario to reproduce, need further investigation

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-11-10T13:29:08Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-12-10T14:19:34Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-10T14:28:31Z

I think this is likely solved by this PR: https://github.com/kubernetes-sigs/kueue/issues/6789
/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-12-10T14:28:37Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/6559#issuecomment-3637353378):

>I think this is likely solved by this PR: https://github.com/kubernetes-sigs/kueue/issues/6789
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
