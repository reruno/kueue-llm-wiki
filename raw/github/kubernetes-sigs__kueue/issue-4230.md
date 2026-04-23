# Issue #4230: Feature gate GA Policy is not clear in the documentation

**Summary**: Feature gate GA Policy is not clear in the documentation

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4230

**Last updated**: 2025-02-12T16:38:12Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kannon92](https://github.com/kannon92)
- **Created**: 2025-02-11T16:47:21Z
- **Updated**: 2025-02-12T16:38:12Z
- **Closed**: 2025-02-12T16:38:12Z
- **Labels**: `kind/documentation`
- **Assignees**: _none_
- **Comments**: 8

## Description

https://kueue.sigs.k8s.io/docs/installation/#change-the-feature-gates-configuration

Reading this table, it reads to me that we don't promote features to GA but leave them as permanent beta.

If a production user relies on a feature gate, when does Kueue drop the ability to set this feature gate?

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-11T17:07:35Z

Basically, we follow the k/k graduation policy. Actually, we promoted 2 features to GA: https://github.com/kubernetes-sigs/kueue/blob/2738e8b05c03fe5dcf38beba1f4769fe2e1888c9/pkg/features/kube_features.go#L187

The same as k/k documentation, we do not mention the GA status in our documentation.
https://kubernetes.io/docs/reference/command-line-tools-reference/feature-gates/

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-11T17:07:42Z

/kind support

### Comment by [@kannon92](https://github.com/kannon92) — 2025-02-11T17:23:32Z

https://kubernetes.io/docs/reference/command-line-tools-reference/feature-gates/#feature-gates-for-graduated-or-deprecated-features

They have a section for GA or deprecated features also.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-11T17:25:08Z

> https://kubernetes.io/docs/reference/command-line-tools-reference/feature-gates/#feature-gates-for-graduated-or-deprecated-features

Oh, I see. Great catch! In that case, we might be able to add a similar section to our documentation.
@mimowo WDYT?

### Comment by [@kannon92](https://github.com/kannon92) — 2025-02-11T21:04:36Z

/remove-kind feature
/kind documentation

Opened up https://github.com/kubernetes-sigs/kueue/pull/4234 for discussion.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-02-11T21:04:40Z

@kannon92: Those labels are not set on the issue: `kind/feature`

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4230#issuecomment-2652064929):

>/remove-kind feature
>/kind documentation
>
>Opened up https://github.com/kubernetes-sigs/kueue/pull/4234 for discussion.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@kannon92](https://github.com/kannon92) — 2025-02-11T21:04:51Z

/remove-kind support

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-12T07:45:40Z

> Oh, I see. Great catch! In that case, we might be able to add a similar section to our documentation.
> [@mimowo](https://github.com/mimowo) WDYT?

+1, thanks for the suggestion
