# Issue #1196: hack/update-codegen.sh uses deprecated scripts

**Summary**: hack/update-codegen.sh uses deprecated scripts

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1196

**Last updated**: 2023-10-12T05:32:24Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2023-10-11T18:07:04Z
- **Updated**: 2023-10-12T05:32:24Z
- **Closed**: 2023-10-12T05:32:23Z
- **Labels**: `kind/cleanup`
- **Assignees**: _none_
- **Comments**: 4

## Description

**What would you like to be cleaned**:

When running `make generate`, this message shows up:

```
WARNING: generate-groups.sh is deprecated.
WARNING: Please use k8s.io/code-generator/kube_codegen.sh instead.

WARNING: generate-internal-groups.sh is deprecated.
WARNING: Please use k8s.io/code-generator/kube_codegen.sh instead.
```

**Why is this needed**:

Keep kueue building

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2023-10-12T00:07:02Z

I think https://github.com/kubernetes-sigs/kueue/pull/1151/files should resolve this

### Comment by [@kannon92](https://github.com/kannon92) — 2023-10-12T00:07:46Z

Maybe this ticket is a duplicate of https://github.com/kubernetes-sigs/kueue/issues/1134

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-10-12T05:32:18Z

> Maybe this ticket is a duplicate of https://github.com/kubernetes-sigs/kueue/issues/1134

Yes, that's right.
/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-10-12T05:32:24Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1196#issuecomment-1758937711):

>> Maybe this ticket is a duplicate of https://github.com/kubernetes-sigs/kueue/issues/1134
>
>Yes, that's right.
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
