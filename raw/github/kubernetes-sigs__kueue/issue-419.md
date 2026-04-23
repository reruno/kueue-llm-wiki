# Issue #419: Automate adoption of jobs that didn't start via Kueue

**Summary**: Automate adoption of jobs that didn't start via Kueue

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/419

**Last updated**: 2024-06-25T21:02:54Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@ahg-g](https://github.com/ahg-g)
- **Created**: 2022-10-18T20:22:36Z
- **Updated**: 2024-06-25T21:02:54Z
- **Closed**: 2024-06-25T21:02:52Z
- **Labels**: `kind/feature`, `lifecycle/stale`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 14

## Description

**What would you like to be added**:

Automate the adoption of jobs that didn't start via Kueue, this means creating the Workload object for those jobs. Admins will need an API to specify which CQ those jobs should be counted against.

**Why is this needed**:
 This can help transition existing clusters to use Kueue

**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [x] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-12-06T06:12:31Z

You mean adopt running jobs with kueue? Does it worth, job is run-to-complete, we can adopt them next time when they're ready to start again.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2023-03-06T06:24:47Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2023-04-05T06:49:46Z

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

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-04-05T09:15:15Z

/remove-lifecycle rotten

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2023-07-04T09:16:34Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-07-04T09:59:48Z

/remove-lifecycle rotten

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-07-04T10:01:14Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-01-23T19:53:05Z

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

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-02-14T20:54:07Z

IHAC which is interested in this. Their setup looks like the following:
- One flavor (so this could be a constant in the script arguments)
- Each Pod has a label for which the value can be passed through a map to derive a ClusterQueue name.
- It is possible for the customer to stop sending new jobs through whatever mechanism was running before Kueue. 

Does anyone have other mappings that we would need to account for?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-02-14T20:54:27Z

/remove-lifecycle stale

### Comment by [@nstogner](https://github.com/nstogner) — 2024-02-15T20:37:38Z

One possible implementation: https://github.com/kubernetes-sigs/kueue/pull/1742 ... thoughts?

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-05-28T21:12:00Z

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

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-06-25T21:02:48Z

https://github.com/kubernetes-sigs/kueue/tree/main/cmd/importer

/assign @trasc 

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-06-25T21:02:53Z

@alculquicondor: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/419#issuecomment-2189965429):

>https://github.com/kubernetes-sigs/kueue/tree/main/cmd/importer
>
>/assign @trasc 
>
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
