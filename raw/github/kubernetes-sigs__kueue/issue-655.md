# Issue #655: Use kueue metrics in load test

**Summary**: Use kueue metrics in load test

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/655

**Last updated**: 2023-04-05T14:42:36Z

---

## Metadata

- **State**: open
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2023-03-20T17:46:21Z
- **Updated**: 2023-04-05T14:42:36Z
- **Closed**: —
- **Labels**: `kind/feature`, `help wanted`
- **Assignees**: _none_
- **Comments**: 6

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

There are a number of metrics exported by kueue that could be used to measure its performance under load. We need to complete https://github.com/kubernetes-sigs/kueue/pull/481 and update README.

**Why is this needed**:

For better tracking of kueue performance

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-03-20T17:46:37Z

/help

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-03-20T17:46:39Z

@alculquicondor: 
	This request has been marked as needing help from a contributor.

### Guidelines
Please ensure that the issue body includes answers to the following questions:
- Why are we solving this issue?
- To address this issue, are there any code changes? If there are code changes, what needs to be done in the code and what places can the assignee treat as reference points?
- Does this issue have zero to low barrier of entry?
- How can the assignee reach out to you for help?


For more details on the requirements of such an issue, please see [here](https://git.k8s.io/community/contributors/guide/help-wanted.md) and ensure that they are met.

If this request no longer meets these requirements, the label can be removed
by commenting with the `/remove-help` command.


<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/655):

>/help


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mikouaj](https://github.com/mikouaj) — 2023-03-27T13:26:48Z

@alculquicondor I've drafted Grafana dashboard that leverages metrics from Kueue for purpose of HPC on GKE workshops, do you think this might be useful?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-03-28T12:33:18Z

Yeah, they could be useful in the context of load tests but also in production.

Can grafana dashboards be shared as configuration files? Otherwise you could add a documentation page here https://github.com/kubernetes-sigs/kueue/tree/main/site/content/en/docs/tasks

Do you mind opening a separate issue for this?

### Comment by [@mikouaj](https://github.com/mikouaj) — 2023-04-05T13:43:31Z

FYI [here is the dashboard](https://github.com/mikouaj/gke-kueue-demo/tree/main/assets) that I have created and play with.
Sure, I can create the separate issue for this.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-04-05T14:42:35Z

cc @moficodes @alizaidis
