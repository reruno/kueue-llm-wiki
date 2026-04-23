# Issue #2732: Extend waitForPodsReady to evict a workload if a replacement pod cannot schedule

**Summary**: Extend waitForPodsReady to evict a workload if a replacement pod cannot schedule

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2732

**Last updated**: 2025-05-28T09:48:01Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-07-31T10:32:19Z
- **Updated**: 2025-05-28T09:48:01Z
- **Closed**: 2025-05-28T09:47:59Z
- **Labels**: `kind/feature`, `lifecycle/stale`
- **Assignees**: [@PBundyra](https://github.com/PBundyra)
- **Comments**: 9

## Description

**What would you like to be added**:

Extend the waitForPodsReady mechanism to allow workload eviction if there is a replacement pod which cannot be scheduled within a specified timeout.

**Why is this needed**:

Currently the mechanism only evicts workloads if they cannot start, but a pod can fail while the  workload is running.

**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [x] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-07-31T10:32:29Z

/assign @PBundyra

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-10-29T10:45:52Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-29T10:49:37Z

/remove-lifecycle stale

### Comment by [@yaroslava-serdiuk](https://github.com/yaroslava-serdiuk) — 2024-12-18T09:31:45Z

cc: @yaroslava-serdiuk

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-26T16:36:32Z

/reopen

@PBundyra could you extend documentation in https://kueue.sigs.k8s.io/docs/tasks/manage/setup_wait_for_pods_ready/?

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-02-26T16:36:38Z

@tenzen-y: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/2732#issuecomment-2685594259):

>/reopen
>
>@PBundyra could you extend documentation in https://kueue.sigs.k8s.io/docs/tasks/manage/setup_wait_for_pods_ready/?
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-05-27T17:09:57Z

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

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-05-28T09:47:55Z

The field has been documented a while ago with this PR https://github.com/kubernetes-sigs/kueue/pull/4964
I believe we can close this issue as it was addressed
/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-05-28T09:48:00Z

@PBundyra: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/2732#issuecomment-2915689037):

>The field has been documented a while ago with this PR https://github.com/kubernetes-sigs/kueue/pull/4964
>I believe we can close this issue as it was addressed
>/close
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
