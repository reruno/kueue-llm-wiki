# Issue #7471: ☂️ Fix the most common flakes

**Summary**: ☂️ Fix the most common flakes

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7471

**Last updated**: 2025-11-14T18:26:15Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-10-31T08:02:32Z
- **Updated**: 2025-11-14T18:26:15Z
- **Closed**: 2025-11-14T18:26:14Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 7

## Description

/kind flake

Ordered by my subjective perception:
- [x] https://github.com/kubernetes-sigs/kueue/issues/7390
- [x] https://github.com/kubernetes-sigs/kueue/issues/7457
- [x] https://github.com/kubernetes-sigs/kueue/issues/7462
- [x] https://github.com/kubernetes-sigs/kueue/issues/7470
- [x] https://github.com/kubernetes-sigs/kueue/issues/7004

These seem particularly common. Let me know if you think the list is missing some other common flake.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-31T08:02:58Z

cc @mwysokin @mbobrovskyi @IrvingMg @mszadkow

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-31T08:04:38Z

cc @tenzen-y @gabesaba

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-10-31T09:25:42Z

Hopefully, we might want to fix those before 0.15

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-31T09:40:51Z

Yes, I want to prioritize fixing them before releasing too.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-03T15:23:06Z

cc @pajakd if you have some ideas for 4

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-14T18:26:09Z

/close
As all known most common flakes from the list as fixed. The remaining less often flakes we can address tracking individually.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-11-14T18:26:15Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/7471#issuecomment-3534018397):

>/close
>As all known most common flakes from the list as fixed. The remaining less often flakes we can address tracking individually.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
