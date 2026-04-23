# Issue #52: Publish kueue in GCR

**Summary**: Publish kueue in GCR

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/52

**Last updated**: 2022-03-04T20:59:47Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2022-02-22T21:21:42Z
- **Updated**: 2022-03-04T20:59:47Z
- **Closed**: 2022-03-04T20:59:47Z
- **Labels**: `kind/feature`, `priority/important-longterm`
- **Assignees**: [@ArangoGutierrez](https://github.com/ArangoGutierrez)
- **Comments**: 4

## Description

We don't necessarily need to wait for a production-ready version. We can publish alpha/beta builds

/kind feature

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-02-22T21:22:24Z

/priority important-longterm

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-02-22T23:05:51Z

/assign

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-03-04T20:59:36Z

```bash
[eduardo@fedora-workstation ~]$ skopeo list-tags docker://gcr.io/k8s-staging-kueue
{
    "Repository": "gcr.io/k8s-staging-kueue",
    "Tags": []
}
```
Repo is up
/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2022-03-04T20:59:47Z

@ArangoGutierrez: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/52#issuecomment-1059526444):

>```bash
>[eduardo@fedora-workstation ~]$ skopeo list-tags docker://gcr.io/k8s-staging-kueue
>{
>    "Repository": "gcr.io/k8s-staging-kueue",
>    "Tags": []
>}
>```
>Repo is up
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
