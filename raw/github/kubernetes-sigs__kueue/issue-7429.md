# Issue #7429: MultiKueue: support mutating the priority class for workloads managed by MultiKueue

**Summary**: MultiKueue: support mutating the priority class for workloads managed by MultiKueue

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7429

**Last updated**: 2026-01-15T17:53:15Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-10-29T15:19:40Z
- **Updated**: 2026-01-15T17:53:15Z
- **Closed**: 2026-01-15T17:53:13Z
- **Labels**: `kind/feature`, `priority/important-soon`, `area/multikueue`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 5

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Recently we introduced this feature https://github.com/kubernetes-sigs/kueue/pull/7289. 

However, I expect this is not working well currently as explained here: https://github.com/kubernetes-sigs/kueue/pull/7289#discussion_r2435152853

Also, for MultiKueue we need to solve another prerequisite issue: https://github.com/kubernetes-sigs/kueue/issues/7350

**Why is this needed**:

To allow the functionality of mutating the workload priority also when MultiKueue is used.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-29T15:19:54Z

cc @mwysokin @mwielgus @mbobrovskyi

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T08:21:08Z

/area multikueue
/priority important-soon

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-01-07T14:04:18Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-15T17:53:06Z

/close
This seems completed by https://github.com/kubernetes-sigs/kueue/pull/8464. I'm not totally sure there might be some issues due to inconsistent Job and Workload priority on the worker, but apparently @mbobrovskyi tested and this works well. Let's open dedicated issues if we detect bugs related to that. The feature as such is done.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-01-15T17:53:14Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/7429#issuecomment-3756145970):

>/close
>This seems completed by https://github.com/kubernetes-sigs/kueue/pull/8464. I'm not totally sure there might be some issues due to inconsistent Job and Workload priority on the worker, but apparently @mbobrovskyi tested and this works well. Let's open dedicated issues if we detect bugs related to that. The feature as such is done.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
