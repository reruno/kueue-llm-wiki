# Issue #7608: Upgrade to use Kubeflow 2.1.0 and support TAS on 0.14.x branch

**Summary**: Upgrade to use Kubeflow 2.1.0 and support TAS on 0.14.x branch

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7608

**Last updated**: 2025-11-20T07:55:23Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-11-12T10:00:24Z
- **Updated**: 2025-11-20T07:55:23Z
- **Closed**: 2025-11-20T07:55:22Z
- **Labels**: `kind/feature`
- **Assignees**: [@IrvingMg](https://github.com/IrvingMg)
- **Comments**: 3

## Description

**What would you like to be added**:


Update Kubeflow to 2.1.0 on the release-0.14 branch

This is a follow up for https://github.com/kubernetes-sigs/kueue/issues/7577

**Why is this needed**:

To support TAS for Kubeflow trainer v2 on 0.14 branch.


**Completion requirements**:

Test what will users observe when the upgrade happens, assuming there is a running workload using Kubeflow 2.0.0.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-12T10:00:38Z

/assign @IrvingMg 
tentatively

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2025-11-20T07:55:17Z

/close

Fixed by #7755

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-11-20T07:55:23Z

@IrvingMg: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/7608#issuecomment-3556428398):

>/close
>
>Fixed by #7755 


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
