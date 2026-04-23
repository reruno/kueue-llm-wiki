# Issue #8819: ☂️ Fix the most common flakes 2.0

**Summary**: ☂️ Fix the most common flakes 2.0

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8819

**Last updated**: 2026-02-02T15:18:07Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-01-27T13:31:56Z
- **Updated**: 2026-02-02T15:18:07Z
- **Closed**: 2026-02-02T15:18:06Z
- **Labels**: `kind/cleanup`
- **Assignees**: _none_
- **Comments**: 3

## Description

I would like to make sure we prioritize fixing the following common flakes as they impact many branches:

- https://github.com/kubernetes-sigs/kueue/issues/8752
- https://github.com/kubernetes-sigs/kueue/issues/8733
- https://github.com/kubernetes-sigs/kueue/issues/8809
- https://github.com/kubernetes-sigs/kueue/issues/8736
- https://github.com/kubernetes-sigs/kueue/issues/8850
- https://github.com/kubernetes-sigs/kueue/issues/8911

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-27T13:32:12Z

cc @tenzen-y @gabesaba @mbobrovskyi @sohankunkerkar

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-02T15:18:01Z

/close
I think https://github.com/kubernetes-sigs/kueue/issues/8911 is not that common, only one occurrence so far. 
Oft I still welcome any PRs fixing the flakes, but I think the purpose of the issue is achieved by eliminating the top 4 flakes.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-02-02T15:18:07Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/8819#issuecomment-3835784046):

>/close
>I think https://github.com/kubernetes-sigs/kueue/issues/8911 is not that common, only one occurrence so far. 
>Oft I still welcome any PRs fixing the flakes, but I think the purpose of the issue is achieved by eliminating the top 4 flakes. 


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
