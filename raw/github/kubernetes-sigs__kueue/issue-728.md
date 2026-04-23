# Issue #728: Prevent merge commits

**Summary**: Prevent merge commits

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/728

**Last updated**: 2024-03-19T08:47:05Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2023-04-26T19:58:29Z
- **Updated**: 2024-03-19T08:47:05Z
- **Closed**: 2024-03-19T08:47:03Z
- **Labels**: `kind/cleanup`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 10

## Description

**What would you like to be cleaned**:

#689 originally had a merge commit, but nothing was holding it from merging. Let's prevent that. Not sure where this is configured.

**Why is this needed**:

To match the git management of kubernetes/kubernetes

## Discussion

### Comment by [@trasc](https://github.com/trasc) — 2023-04-27T08:50:47Z

Strictly on github there should be in "Setting->General->Pull Requests->Allow merge commits "  but I have no idea how `tide` is making use of its labels.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-04-27T16:04:44Z

Thanks.
I changed the setting. Let's see if that's it in future PRs.

/close
for now

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-04-27T16:04:48Z

@alculquicondor: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/728#issuecomment-1525959300):

>Thanks.
>I changed the setting. Let's see if that's it in future PRs.
>
>/close
>for now


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-04-27T17:04:22Z

/reopen

That didn't work 
![image](https://user-images.githubusercontent.com/1299064/234936795-e5762f19-124a-4a99-92d9-1536969e826e.png)

#714

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-04-27T17:04:26Z

@alculquicondor: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/728#issuecomment-1526042944):

>/reopen
>
>That didn't work 
>![image](https://user-images.githubusercontent.com/1299064/234936795-e5762f19-124a-4a99-92d9-1536969e826e.png)
>
>#714


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-04-27T17:06:35Z

maybe @ArangoGutierrez knows the trick

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-01-19T07:00:02Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-02-18T07:59:12Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-03-19T08:46:59Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues and PRs.

This bot triages issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Reopen this issue with `/reopen`
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/close not-planned

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-03-19T08:47:04Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/728#issuecomment-2006346077):

>The Kubernetes project currently lacks enough active contributors to adequately respond to all issues and PRs.
>
>This bot triages issues according to the following rules:
>- After 90d of inactivity, `lifecycle/stale` is applied
>- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
>- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed
>
>You can:
>- Reopen this issue with `/reopen`
>- Mark this issue as fresh with `/remove-lifecycle rotten`
>- Offer to help out with [Issue Triage][1]
>
>Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).
>
>/close not-planned
>
>[1]: https://www.kubernetes.dev/docs/guide/issue-triage/


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
