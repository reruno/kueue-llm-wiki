# Issue #1230: Let Helm chart specify which FeatureGates should be used

**Summary**: Let Helm chart specify which FeatureGates should be used

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1230

**Last updated**: 2023-11-14T10:10:09Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@rhaps0dy](https://github.com/rhaps0dy)
- **Created**: 2023-10-19T21:17:50Z
- **Updated**: 2023-11-14T10:10:09Z
- **Closed**: 2023-11-14T10:10:09Z
- **Labels**: `kind/feature`, `triage/accepted`
- **Assignees**: _none_
- **Comments**: 5

## Description

**What would you like to be added**:

kueue uses [feature gates](https://github.com/kubernetes-sigs/kueue/blob/main/pkg/features/kube_features.go#L29-L67) to preview features, and these are present in releases.

I would like to add a section in the Helm chart, either under [`controllerManager.config`](https://github.com/kubernetes-sigs/kueue/blob/91d5f645a326dae1ea8542879adcc62ba4db7f5d/charts/kueue/values.yaml#L19C11-L19C11) or [`managerConfig`](https://github.com/kubernetes-sigs/kueue/blob/main/charts/kueue/values.yaml#L53), which looks like this:

```yaml
featureGates:
  partialAdmission: true
  queueVisibility: false
  flavorFungibility: true
```

**Why is this needed**:

At the moment, enabling or disabling feature gates requires either:
- kustomizing the manifests
- forking the Helm chart and changing it to include feature gates

Often the feature gates are [documented in releases](https://kueue.sigs.k8s.io/docs/tasks/setup_sequential_admission/) even while they're in alpha. Changing a command-line argument shouldn't require forking.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

Is there appetite for a PR with this? I'd be happy to write the docs and API change if so

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-10-20T11:18:38Z

This is a good point. Probably, we can select [controllerManager.config](https://github.com/kubernetes-sigs/kueue/blob/91d5f645a326dae1ea8542879adcc62ba4db7f5d/charts/kueue/values.yaml#L19C11-L19C11).

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-10-20T14:56:07Z

/triage accepted

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-10-23T02:42:46Z

cc @B1F030 this also relates to kueue's features which are controlled by the feature gate.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-11-07T03:50:44Z

/assign @B1F030

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-11-07T03:50:46Z

@kerthcet: GitHub didn't allow me to assign the following users: B1F030.

Note that only [kubernetes-sigs members](https://github.com/orgs/kubernetes-sigs/people) with read permissions, repo collaborators and people who have commented on this issue/PR can be assigned. Additionally, issues/PRs can only have 10 assignees at the same time.
For more information please see [the contributor guide](https://git.k8s.io/community/contributors/guide/first-contribution.md#issue-assignment-in-github)

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1230#issuecomment-1797700163):

>/assign @B1F030 


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
