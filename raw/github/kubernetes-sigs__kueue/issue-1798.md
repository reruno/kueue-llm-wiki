# Issue #1798: Improve Helm charts sync from Kustomize manifests

**Summary**: Improve Helm charts sync from Kustomize manifests

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1798

**Last updated**: 2025-05-12T05:53:15Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@astefanutti](https://github.com/astefanutti)
- **Created**: 2024-03-04T17:42:38Z
- **Updated**: 2025-05-12T05:53:15Z
- **Closed**: 2025-05-12T05:53:15Z
- **Labels**: `kind/feature`, `help wanted`
- **Assignees**: [@IrvingMg](https://github.com/IrvingMg)
- **Comments**: 11

## Description

**What would you like to be added**:

The Helm charts are currently synchronised from the Kustomize manifests, that are the source of truth for deploying Kueue, with the `hack/update-helm.sh` script, that performs a series of ad-hoc file manipulations using `yq` and `sed` commands.

It would be great to consider a more robust approach to generate the Helm charts from the Kustomize manifests. Part of the solution could be to move to a strongly typed approach, or (not necessarily mutually exclusive) add some tests that'd guarantee the generated Helm charts are valid. 

**Why is this needed**:

#1695 has added an extra level of complexity to that script, reaching a point where it may become difficult to maintain it, and guarantee non-regression, as discussed in  https://github.com/kubernetes-sigs/kueue/pull/1695#discussion_r1489203905.

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-03-25T15:07:31Z

Is this something you or your team is interested in taking?

### Comment by [@astefanutti](https://github.com/astefanutti) — 2024-03-25T16:08:27Z

That won't be a high priority for us as we're not using Helm charts.

I've created the issue more as a follow up from https://github.com/kubernetes-sigs/kueue/pull/1695#discussion_r1489203905 than something we would really need 🙂.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-04-02T16:59:56Z

@alculquicondor @astefanutti If this issue is not a high priority in both teams, should we mark this as a good-first-issue?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-04-02T17:36:53Z

I'm not sure it's a good "first" issue, but we can give it

/help

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-04-02T17:36:54Z

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

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1798):

>I'm not sure it's a good "first" issue, but we can give it
>
>/help


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@Vandit1604](https://github.com/Vandit1604) — 2024-04-12T22:44:03Z

/assign
I'll take a look into this.

### Comment by [@Vandit1604](https://github.com/Vandit1604) — 2024-05-17T13:00:25Z

I'm unable to give time to this right now. Unassigning myself so someone else can give it a go.

### Comment by [@rptaylor](https://github.com/rptaylor) — 2025-01-14T22:24:43Z


Is hack/update-helm.sh still used to generate/modify a Helm chart based on the kustomize manifests?

It seems like it would be complicated and confusing indeed if the current Helm chart in https://github.com/kubernetes-sigs/kueue/tree/main/charts/kueue underwent modifications from that script before being published.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2025-01-15T14:22:04Z

Yes, it is used. In some ways, it alerts us if we do changes in kustomize that aren't reflected on the helm charts and vice versa. But there are some changes that currently escape the verifications.

If you can devise a different mechanism that would give us a similar or better level of verification, then it could be considered.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-29T17:43:46Z

cc @mbobrovskyi @mszadkow ptal, bumping the need for a more maintainable way of synchronizing the manifests as it becomes an issue raised in https://github.com/kubernetes-sigs/kueue/pull/3852.

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2025-02-14T08:44:49Z

/assign
