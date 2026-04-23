# Issue #9109: Releasing the promote_pull.sh fails

**Summary**: Releasing the promote_pull.sh fails

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9109

**Last updated**: 2026-03-02T09:28:14Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-02-11T09:10:23Z
- **Updated**: 2026-03-02T09:28:14Z
- **Closed**: 2026-03-02T09:28:14Z
- **Labels**: `kind/bug`
- **Assignees**: [@mimowo](https://github.com/mimowo)
- **Comments**: 2

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
Doing 0.16.1 patch release

```
GITHUB_USER=mimowo KUBERNETES_K8S_IO_PATH=../../k8s.io/k8s.io KUBERNETES_REPOS_PATH=../../k8s.io ./hack/releasing/promote_pull.sh v0.16.1
```

```
+++ I'm about to do the following to push to GitHub (and I'm assuming origin is your personal fork):

  git push origin kueue-promote-0.16-1770800919:kueue-promote-0.16

+++ Proceed (anything other than 'y' aborts it)? [y/N] y
Enumerating objects: 11, done.
Counting objects: 100% (11/11), done.
Delta compression using up to 64 threads
Compressing objects: 100% (6/6), done.
Writing objects: 100% (6/6), 921 bytes | 921.00 KiB/s, done.
Total 6 (delta 3), reused 0 (delta 0), pack-reused 0 (from 0)
remote: Resolving deltas: 100% (3/3), completed with 3 local objects.
To https://github.com/mimowo/k8s.io.git
 + da59e3a0b...99c7cfe67 kueue-promote-0.16-1770800919 -> kueue-promote-0.16 (forced update)

+++ Creating a pull request on GitHub repo kubernetes/k8s at mimowo:kueue-promote-0.16 for main
GraphQL: Could not resolve to a Repository with the name 'kubernetes/k8s'. (repository)

+++ Returning to the main branch.
!!! Deleting branch kueue-promote-0.16-1770800919.
```


**What you expected to happen**:
no failure

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-11T09:11:10Z

I thik this part looks wrong, probably some regex is wrong: `'kubernetes/k8s'. (repository)`, it should be `kubernetes/k8s.io`.

cc @mbobrovskyi @gabesaba @tenzen-y

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-02T08:11:41Z

/assign
