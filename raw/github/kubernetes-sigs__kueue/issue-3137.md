# Issue #3137: Remove webhook builder when controller-runtime allows overriding a mutation handler

**Summary**: Remove webhook builder when controller-runtime allows overriding a mutation handler

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3137

**Last updated**: 2024-11-06T08:46:09Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2024-09-25T15:36:14Z
- **Updated**: 2024-11-06T08:46:09Z
- **Closed**: 2024-11-06T08:46:07Z
- **Labels**: `kind/cleanup`
- **Assignees**: _none_
- **Comments**: 4

## Description

**What would you like to be cleaned**:

Remove `pkg/controller/jobframework/webhook/builder.go` when https://github.com/kubernetes-sigs/controller-runtime/pull/2932 is merged and released.

**Why is this needed**:

We duplicated the file to be able to provide a fix in Kueue faster in #3132

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-09-25T15:37:01Z

Do not assign this issue yet, because #3132 is not merged yet.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-06T08:45:54Z

Closing in favor of https://github.com/kubernetes-sigs/kueue/issues/3469, as with the controller-runtime fix we can drop also our defaulter altogether.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-06T08:46:02Z

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-11-06T08:46:08Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3137#issuecomment-2459022273):

>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
