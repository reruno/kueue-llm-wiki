# Issue #3279: MVP support for arbitrary resizing a StatefulSet (investigate if feasible)

**Summary**: MVP support for arbitrary resizing a StatefulSet (investigate if feasible)

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3279

**Last updated**: 2025-06-03T08:17:37Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-10-21T14:44:21Z
- **Updated**: 2025-06-03T08:17:37Z
- **Closed**: 2025-06-03T08:17:35Z
- **Labels**: `kind/feature`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 10

## Description

**What would you like to be added**:

Investigate if we can achieve resizing of a stateful set based on PodGroups.

In the MVP approach it is ok to recreate the entire PodGroup.

This is a follow up to https://github.com/kubernetes-sigs/kueue/issues/2717.

Long-term we may want to support smooth resizes, but it probably will require https://github.com/kubernetes-sigs/kueue/issues/77.

**Why is this needed**:

To support use-cases for resizing StatefulSets.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-21T14:45:23Z

/cc @mwielgus @vladikkuzn @mbobrovskyi @alculquicondor

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-11-06T18:03:37Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-15T11:07:43Z

The very MVP of scaling-down and up via 0 is covered already with https://github.com/kubernetes-sigs/kueue/pull/3487. Keeping this open to investigate arbitrary scaling x->y, where x<y or x>y.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-15T11:08:21Z

/retitle MVP support for arbitrary resizing a StatefulSet (investigate if feasible)

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-12-30T15:34:57Z

/assign

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-03-30T16:27:15Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle stale`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-04-29T17:06:47Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle rotten

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-01T06:50:21Z

/remove-lifecycle rotten

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-03T08:17:30Z

At the moment of opening the issue I didn't have  any use-cases, but thought it might be an nice addition. However, I think making it work is complex.

We can re-open if there is some interest in the community, let us know in that case.

For now closing to avoid distractions.

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-06-03T08:17:36Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3279#issuecomment-2934074953):

>At the moment of opening the issue I didn't have  any use-cases, but thought it might be an nice addition. However, I think making it work is complex.
>
>We can re-open if there is some interest in the community, let us know in that case.
>
>For now closing to avoid distractions.
>
>/close
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
