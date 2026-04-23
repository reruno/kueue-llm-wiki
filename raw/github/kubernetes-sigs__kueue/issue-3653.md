# Issue #3653: Move Pod group labels and annotations to `apis/` package

**Summary**: Move Pod group labels and annotations to `apis/` package

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3653

**Last updated**: 2025-06-23T08:13:09Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@PBundyra](https://github.com/PBundyra)
- **Created**: 2024-11-26T13:49:31Z
- **Updated**: 2025-06-23T08:13:09Z
- **Closed**: 2025-06-23T08:13:09Z
- **Labels**: `kind/feature`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 7

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
Move consts

```
GroupNameLabel               = "kueue.x-k8s.io/pod-group-name"
GroupTotalCountAnnotation    = "kueue.x-k8s.io/pod-group-total-count"
GroupFastAdmissionAnnotation = "kueue.x-k8s.io/pod-group-fast-admission"
RoleHashAnnotation           = "kueue.x-k8s.io/role-hash"
RetriableInGroupAnnotation   = "kueue.x-k8s.io/retriable-in-group"
```

from `pkg/controller/jobs/pod/pod_webhook.go` to `apis` package

**Why is this needed**:
To improve code quality and API visibility

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-11-26T14:03:41Z

I think that we should not move those labels to apis package since those are not for a whole of Kueue projects.

Instead of that, I think that creating dedicated constants package or restructure the Pod, Deployment, and StatefulSet packages. For example, we might be able to restructure those packages based on the Pod directory.

This is a similar concept to KubeflowJobs.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-02-24T14:37:15Z

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

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-02-25T09:31:42Z

/remove-lifecycle stale

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-02-26T08:32:15Z

/assign

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-05-27T09:09:56Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-27T09:34:03Z

/remove-lifecycle stale

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-06-23T08:13:09Z

This issue has been resolved by the PR linked above
