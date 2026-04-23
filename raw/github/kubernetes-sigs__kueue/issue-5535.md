# Issue #5535: Drop RELEASE_BRANCH from Makefile

**Summary**: Drop RELEASE_BRANCH from Makefile

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5535

**Last updated**: 2025-06-06T09:51:30Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-06-06T09:20:12Z
- **Updated**: 2025-06-06T09:51:30Z
- **Closed**: 2025-06-06T09:51:28Z
- **Labels**: `kind/cleanup`
- **Assignees**: _none_
- **Comments**: 4

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

Drop the [RELEASE_BRANCH](https://github.com/kubernetes-sigs/kueue/blob/main/Makefile#L92) variable and replace with `BRANCH_NAME=git branch --show-current`.

**Why is this needed**:

The RELEASE_BRANCH variable in our Makefile adds [unnecessary step](https://github.com/kubernetes-sigs/kueue/blob/a413f4e30c56c4bc506691773ae350f46515e3c9/.github/ISSUE_TEMPLATE/NEW_RELEASE.md?plain=1#L24) during the release process to update it manually.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-06T09:20:22Z

cc @tenzen-y @mbobrovskyi wdyt?

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-06-06T09:48:21Z

If I understood correctly, you're running `make prepare-release-branch` from the prepare-release branch (e.g., #5479). That won't work as expected, because in this case, BRANCH_NAME will be set to `prepare-v0.12.2`.

Instead, you need to explicitly specify the target release branch, like this:

```
make prepare-release-branch BRANCH_NAME=release-0.12
```

To be honest, I think this approach is more complicated.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-06T09:51:24Z

> That won't work as expected, because in this case, BRANCH_NAME will be set to prepare-v0.12.2.

Ah, yes, I missed this.

> To be honest, I think this approach is more complicated.

Agree, this could work, but both need manual step, so I'm ok as is. Thank you for catching that.

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-06-06T09:51:29Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/5535#issuecomment-2948706432):

>> That won't work as expected, because in this case, BRANCH_NAME will be set to prepare-v0.12.2.
>
>Ah, yes, I missed this.
>
>> To be honest, I think this approach is more complicated.
>
>Agree, this could work, but both need manual step, so I'm ok as is. Thank you for catching that.
>
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
