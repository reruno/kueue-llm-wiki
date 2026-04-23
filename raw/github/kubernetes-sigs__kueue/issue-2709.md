# Issue #2709: Update Kubeflow image tag

**Summary**: Update Kubeflow image tag

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2709

**Last updated**: 2024-09-26T15:48:43Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mszadkow](https://github.com/mszadkow)
- **Created**: 2024-07-29T07:34:44Z
- **Updated**: 2024-09-26T15:48:43Z
- **Closed**: 2024-09-26T15:48:40Z
- **Labels**: `kind/cleanup`
- **Assignees**: _none_
- **Comments**: 3

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

Kubeflow image tag in the current form is based on the manual lookup, because the tag doesn't match semantic version.
``` shell
export KUBEFLOW_IMAGE=kubeflow/training-operator:v1-855e096
```
This requires a manual intervention in multiple places if Kubeflow version has changed.

**Why is this needed**:

That could be updated and automated whenever Kubeflow release process starts include the semantic versioning image tags - https://github.com/kubeflow/training-operator/issues/2155

## Discussion

### Comment by [@mszadkow](https://github.com/mszadkow) — 2024-07-29T07:43:31Z

Requested here: https://github.com/kubernetes-sigs/kueue/pull/2626#discussion_r1690920760
The PR is not merged yet

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-09-26T15:48:35Z

/close 

Due to we already fixed it on https://github.com/kubernetes-sigs/kueue/pull/2880.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-09-26T15:48:41Z

@mbobrovskyi: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/2709#issuecomment-2377341694):

>/close 
>
>Due to we already fixed it on https://github.com/kubernetes-sigs/kueue/pull/2880.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
