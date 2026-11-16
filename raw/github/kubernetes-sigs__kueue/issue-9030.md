# Issue #9030: Error silencing in AdjustResources (pkg/workload/resources.go)

**Summary**: Error silencing in AdjustResources (pkg/workload/resources.go)

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9030

**Last updated**: 2026-11-14T02:39:53Z

---

## Metadata

- **State**: open
- **Author**: [@Singularity23x0](https://github.com/Singularity23x0)
- **Created**: 2026-02-06T13:48:29Z
- **Updated**: 2026-11-14T02:39:53Z
- **Closed**: —
- **Labels**: `kind/bug`, `lifecycle/stale`
- **Assignees**: [@Dasmat13](https://github.com/Dasmat13)
- **Comments**: 7

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
The `AdjustResources` function in `pkg/workload/resources.go` ignore any errors encountered when handling Overhead and Limits.
This means when Creating/Updating a workload, scheduling it or updating Limit Ranges or Runtime Classes any issue with performing the adjusting will be ignored.
As a consequence we may schedule a workload incorrectly due to an issue with Runtime Classes or Limit Ranges.

On top of that, we have no reliable way of performing a retry when an error occurs, as `AdjustResources` is performed in multiple places outside of the reconciler.

**What you expected to happen**:
* `AdjustResources` is used only in the WorkloadController -> Reconcile
* When a Runtime Class is missing for any PodSets of a workload, the workload should be marked as inadmissible.
* When any other error occurs upon Getting the RuntimeClass we should also retry the reconcile.
* Similarly we should retry the reconcile when we are unable to fetch the LimitRangeList.
* Workload should not be scheduled until `AdjustResources` is able to adjust it without error.

**How to reproduce it (as minimally and precisely as possible)**:
The case of a missing RuntimeClass is currently covered by the test: **_Workload controller with scheduler when the workload defines only resource limits and the LocalQueue is created late [It] The limits should be used as request values_** in `test/integration/singlecluster/scheduler/workload_controller_test.go` (we currently expect no Overhead to be adjusted in this case).

**Anything else we need to know?**:
The adjustment may be difficult to implement until we have a reliable plan for handling #5310 

**Environment**:
- Kueue version (use `git describe --tags --dirty --always`):  `v0.16.0-devel-397-ga26d4942a-dirty`

## Discussion

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-05-07T13:53:48Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-06-06T14:47:45Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2026-06-08T09:31:47Z

/remove-lifecycle rotten

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-08-15T12:26:28Z

/assign @Dasmat13

### Comment by [@kubernetes-prow[bot]](https://github.com/apps/kubernetes-prow) — 2026-08-15T12:26:30Z

@tenzen-y: GitHub didn't allow me to assign the following users: Dasmat13.

Note that only [kubernetes-sigs members](https://github.com/orgs/kubernetes-sigs/people) with read permissions, repo collaborators and people who have commented on this issue/PR can be assigned. Additionally, issues/PRs can only have 10 assignees at the same time.
For more information please see [the contributor guide](https://git.k8s.io/community/contributors/guide/first-contribution.md#issue-assignment-in-github)

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/9030#issuecomment-5302214774):

>/assign @Dasmat13 


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@Dasmat13](https://github.com/Dasmat13) — 2026-08-16T02:01:37Z

/assign

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-11-14T02:39:50Z

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
