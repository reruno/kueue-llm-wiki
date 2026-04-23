# Issue #1618: Optional garbage collection of finished Workloads

**Summary**: Optional garbage collection of finished Workloads

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1618

**Last updated**: 2025-05-14T12:07:22Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@woehrl01](https://github.com/woehrl01)
- **Created**: 2024-01-19T11:00:54Z
- **Updated**: 2025-05-14T12:07:22Z
- **Closed**: 2025-05-14T12:07:22Z
- **Labels**: `kind/feature`
- **Assignees**: [@mykysha](https://github.com/mykysha), [@mwysokin](https://github.com/mwysokin)
- **Comments**: 24

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

I would like to have an manager option to delete workload resources as soon as (or with a ttl) the scheduled Job is finished.

**Why is this needed**:

 I changed a configuration to retain more history of job executions of a cronjob, and the memory consumption of the kueue-manager more than doubled:

![Bildschirmfoto 2024-01-19 um 11 57 50](https://github.com/kubernetes-sigs/kueue/assets/2535856/c6ff8083-f69e-4268-b24a-edf7a16f3fc7)

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@woehrl01](https://github.com/woehrl01) — 2024-01-19T11:21:29Z

Not sure if this is related, but I also found out that after that change of keeping history ( and not having a ttl on jobs), Kueue stopped working and showing an insane amount of admitted workloads (using v0.5.2)


![Bildschirmfoto 2024-01-19 um 12 16 28](https://github.com/kubernetes-sigs/kueue/assets/2535856/6b733219-9ba5-4dbc-9260-a24f6c509292)

Deleting all the succeeded jobs by hand recovered that.

### Comment by [@woehrl01](https://github.com/woehrl01) — 2024-02-07T16:45:02Z

I guess the admitted workload bug this is fixed by #1654. It would be still nice to remove the workload resource all together.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-05-07T16:45:27Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-06-06T17:23:33Z

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

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-06-25T20:56:21Z

Are you asking to just delete the Workload but keep the parent Job (or Job CRD)?

### Comment by [@woehrl01](https://github.com/woehrl01) — 2024-06-25T20:58:59Z

@alculquicondor yes. That was the idea. The workload will be deleted eventually, but this would free up etcd storage until ttl of the job crd has been reached.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-06-25T21:32:42Z

/retitle Optional garbage collection of finished Workloads

🤔 maybe we can also do this for orphan Workloads #1789

### Comment by [@mwysokin](https://github.com/mwysokin) — 2024-07-02T14:39:20Z

/assign

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-08-01T15:03:32Z

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

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-08-01T15:03:38Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1618#issuecomment-2263301502):

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


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@kannon92](https://github.com/kannon92) — 2024-08-01T19:50:40Z

/reopen

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-08-01T19:50:44Z

@kannon92: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1618#issuecomment-2263856566):

>/reopen


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@kannon92](https://github.com/kannon92) — 2024-08-01T19:50:58Z

Opening due to the work seems to be in flight.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-08-31T20:24:28Z

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

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-08-31T20:24:32Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1618#issuecomment-2323035097):

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


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@woehrl01](https://github.com/woehrl01) — 2024-08-31T20:41:57Z

/reopen

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-08-31T20:42:01Z

@woehrl01: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1618#issuecomment-2323038437):

>/reopen


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@woehrl01](https://github.com/woehrl01) — 2024-08-31T20:43:00Z

/remove-lifecycle rotten

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-11-29T20:57:16Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-12-29T21:31:59Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-07T12:27:33Z

/remove-lifecycle rotten
cc @mwysokin would you like to continue working on this?

### Comment by [@mykysha](https://github.com/mykysha) — 2025-04-03T11:05:10Z

/assign

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-04-18T09:25:56Z

You must be a member of the [kubernetes-sigs/kueue-maintainers](https://github.com/orgs/kubernetes-sigs/teams/kueue-maintainers/members) GitHub team to add status labels. If you believe you should be able to issue the /status command, please contact your Kueue Maintainers and have them propose you as an additional delegate for this responsibility.
