# Issue #5800: Allow for excludeResources to be specified at Cluster Queue Level

**Summary**: Allow for excludeResources to be specified at Cluster Queue Level

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5800

**Last updated**: 2025-11-19T17:28:23Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kannon92](https://github.com/kannon92)
- **Created**: 2025-06-29T16:32:09Z
- **Updated**: 2025-11-19T17:28:23Z
- **Closed**: 2025-11-19T17:28:22Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 4

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

I would like to add the configuration option excludeResources to ClusterQueues.

**Why is this needed**:

I'd like to move more of the configuration fields to admin specified configurations. Admins have a hard time figuring out all kinds of resources that need to be added to the excludeResources configuration. If a user uses huge pages or ephemeral-storage than they have to find a way to update the kueue configuration which may be possible for most end-users.

Deploying a new value to the configuration requires a restart of the controller and I think it would make sense to also have this field on the ClusterQueue.

ref: https://kueue.sigs.k8s.io/docs/tasks/manage/administer_cluster_quotas/#exclude-arbitrary-resources-in-the-quota-management


**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-09-27T17:25:55Z

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

### Comment by [@kannon92](https://github.com/kannon92) — 2025-09-28T18:00:38Z

/remove-lifecycle stale

cc @mimowo @gabesaba @tenzen-y 

WDYT?

I can see a limitation of the config map is that this is global for all ClusterQueues.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-11-19T17:28:17Z

/close

I don't think this is a good idea.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-11-19T17:28:23Z

@kannon92: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/5800#issuecomment-3553881406):

>/close
>
>I don't think this is a good idea.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
