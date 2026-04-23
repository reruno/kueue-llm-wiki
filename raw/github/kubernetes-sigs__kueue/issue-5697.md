# Issue #5697: Doc: Add schedulingStats

**Summary**: Doc: Add schedulingStats

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5697

**Last updated**: 2026-04-16T18:18:55Z

---

## Metadata

- **State**: open
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-06-20T13:02:03Z
- **Updated**: 2026-04-16T18:18:55Z
- **Closed**: —
- **Labels**: `kind/documentation`
- **Assignees**: _none_
- **Comments**: 15

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

I would like to add the documentation for `schedulingStats` Workload Status: https://github.com/kubernetes-sigs/kueue/blob/f49944e3eda5e43dafb9ac6db6bfec458a2be05d/apis/kueue/v1beta1/workload_types.go#L410

I think a better place is https://kueue.sigs.k8s.io/docs/concepts/workload/

**Why is this needed**:

All features must be described in the documentation.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-20T13:02:24Z

/remove-kind feature
/kind documentation

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-20T13:02:39Z

cc @mimowo @mszadkow @mbobrovskyi

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-20T13:05:56Z

Do we need to document Workload fields? I would prefer not need to do it. Documenting every workload API field is a lot of work.

I think some API comments to the fields should be enough for knowledgeable admins.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-20T13:12:00Z

> Do we need to document Workload fields? I would prefer not need to do it. Documenting every workload API field is a lot of work.
> 
> I think some API comments to the fields should be enough for knowledgeable admins.

I would like to offer to add documentation for this.
Indeed, we already have doc to describe for how to observe the requeueState.

This `schedulingStats` has a bit of complicated features. So, we can describe the mechanism.
The API comment will not reveal the mechanism depending on the `schedulingStats` field.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-20T13:16:38Z

Ok, I don't have a strong view but I would prefer to keep the docs user oriented and mostly focused on the user facing APIs. 

Workload officially is not a user facing API, but I agree some users need to know it to operate Kueue. So maybe we need some section in the docs like "Internal Workload API". 

The field was added to be able to track the information needed for the metrics, so I think the main thing is to make sure the metrics are documented.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-20T14:50:45Z

> Ok, I don't have a strong view but I would prefer to keep the docs user oriented and mostly focused on the user facing APIs.
> 
> Workload officially is not a user facing API, but I agree some users need to know it to operate Kueue. So maybe we need some section in the docs like "Internal Workload API".
> 
> The field was added to be able to track the information needed for the metrics, so I think the main thing is to make sure the metrics are documented.

I think that Workload is also user facing. We have 2 type of users, admins and batch users.
And, admins should know Workload API concept and functionalities to leverage all Kueue features.

Additionally, we already have https://kueue.sigs.k8s.io/docs/concepts/workload/ page which allows us to describe the Workload description. So, I think we can keep using this page.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-20T15:09:23Z

I see, ok let's add a section in  https://kueue.sigs.k8s.io/docs/concepts/workload/

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-20T15:17:12Z

> I see, ok let's add a section in https://kueue.sigs.k8s.io/docs/concepts/workload/

SGTM, thanks

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-09-18T15:53:47Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-18T15:58:13Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-12-17T16:43:05Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-01-16T17:38:17Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-16T17:42:29Z

/remove-lifecycle rotten

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-04-16T17:52:51Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-04-16T18:18:55Z

/remove-lifecycle stale
