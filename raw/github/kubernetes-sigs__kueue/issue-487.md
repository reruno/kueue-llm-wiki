# Issue #487: Kubectl plugin for listing objects

**Summary**: Kubectl plugin for listing objects

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/487

**Last updated**: 2024-04-29T17:11:05Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2022-12-21T18:41:24Z
- **Updated**: 2024-04-29T17:11:05Z
- **Closed**: 2024-04-29T17:11:03Z
- **Labels**: `kind/feature`, `lifecycle/stale`
- **Assignees**: _none_
- **Comments**: 17

## Description

**What would you like to be added**:

A [kubectl plugin](https://kubernetes.io/docs/tasks/extend-kubectl/kubectl-plugins/) that allows to list Jobs and ClusterQueues with comprehensive information.

And a `kubectl describe` equivalent for Jobs that includes Workload information.

Other useful helpers:
- Manually admit a workload.

**Why is this needed**:

The basic view of `kubectl get` can't include details such as whether a workload is admitted or why it's pending, because the information is present in compound objects. Similarly, it can't tell the status of a ClusterQueue if it's misconfigured.

Furthermore, when listing Jobs, you wouldn't see the details of the accompanying Workload.

**Completion requirements**:

This enhancement requires the following artifacts:

- [X] Design doc
- [X] API change: the command line interface is an API.
- [X] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2023-03-21T19:25:06Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-03-21T19:25:50Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2023-06-19T19:45:56Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-06-19T20:34:23Z

/remove-lifecycle stale

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-07-10T20:06:42Z

@vsoch this is the issue I was referring to.

### Comment by [@vsoch](https://github.com/vsoch) — 2023-07-11T20:46:45Z

Here is a design document for what I am thinking: https://gist.github.com/vsoch/954d8c95bdb71bcca92b438bbc879eca. Let me know if you'd like that as a Google document instead. Some notes:

- It will be more advantageous to have this scoped to be a command line tool for kueue, and one that folds into being a plugin if desired. I actually think the first use case (where someone could essentially interact with kueue via the command line and not with kubectl) would be hugely great for the converged computing use case - folks are used to command line tools to interact with / manage jobs, and we could provide similar interactions to it.
- I've proposed a set of subcommands to start, and additional ones I think would be useful.

And it's assumed that the implementation would be in Go.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-07-12T12:16:27Z

oh, we actually have a place for this in the repo itself :)
https://github.com/kubernetes-sigs/kueue/tree/main/keps

Either a PR or a google doc works better as we can comment on specific sections of the design.

I like the idea of a tool that works both standalone and as a plugin. To be fair, a plugin is not much more than a CLI that happens to start with `kubectl-` :)

### Comment by [@vsoch](https://github.com/vsoch) — 2023-07-12T12:47:29Z

All set! https://github.com/kubernetes-sigs/kueue/pull/977

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-01-24T07:57:07Z

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

### Comment by [@vsoch](https://github.com/vsoch) — 2024-01-24T07:59:07Z

Hey is there a status update here? I made my first plugin last weekend and it was fairly simple so I could jump in to help if the current assignee is low on bandwidth.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-01-24T08:03:22Z

> Hey is there a status update here? I made my first plugin last weekend and it was fairly simple so I could jump in to help if the current assignee is low on bandwidth.

@vsoch Thank you for offering help. @yaroslava-serdiuk is working on the KEP.

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-04-23T08:38:39Z

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

### Comment by [@vsoch](https://github.com/vsoch) — 2024-04-23T10:00:40Z

Checking in again - this is still a WIP?

### Comment by [@yaroslava-serdiuk](https://github.com/yaroslava-serdiuk) — 2024-04-23T14:21:03Z

I'm currently not working on it, but AFAIK this should be picked up soon. 
@mwielgus do you have any update on it?

### Comment by [@vsoch](https://github.com/vsoch) — 2024-04-23T18:59:19Z

I originally couldn't do it because we didn't have a proper CLA, but we do now, in case help is still wanted. Let me know!

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-04-29T17:11:00Z

/close

I see that @mwielgus created an updated issue.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-04-29T17:11:04Z

@alculquicondor: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/487#issuecomment-2083243537):

>/close
>
>I see that @mwielgus created an updated issue.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
