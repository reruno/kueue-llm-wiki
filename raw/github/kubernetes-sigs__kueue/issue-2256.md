# Issue #2256: Deprecate the `QueueVisibility` feature gate and corresponding API

**Summary**: Deprecate the `QueueVisibility` feature gate and corresponding API

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2256

**Last updated**: 2024-09-24T16:48:02Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@PBundyra](https://github.com/PBundyra)
- **Created**: 2024-05-22T13:10:45Z
- **Updated**: 2024-09-24T16:48:02Z
- **Closed**: 2024-09-24T16:48:02Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 10

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:
I suggest coming with a plan to deprecate [the `QueueVisibility` API](https://github.com/kubernetes-sigs/kueue/tree/main/keps/168-pending-workloads-visibility). I would start with deprecating the `QueueVisiblity` feature gate and deleting logic behind it, and then remove [the visibility field](https://github.com/kubernetes-sigs/kueue/blob/a7ca2acc2042b047137a769bfcb1e6b749eba469/apis/kueue/v1beta1/clusterqueue_types.go#L302) from ClusterQueue's Status when migrating to a next beta version of Kueue API.

**Why is this needed**:
There was [the visibility API](https://github.com/kubernetes-sigs/kueue/tree/main/keps/168-2-pending-workloads-visibility) introduced that covers all business needs that were cover by the `QueueVisibility` API and more. The visibility API resolves all drawback related to the `QueueVisibility` API and addresses its limitations. For now I don't see a rationale for maintaining the `QueueVisiblity` API. Additionally I believe having two different ways (and two feature gates) to monitor pending workloads may lead to a little confusion regarding their pros and cons.

## Discussion

### Comment by [@PBundyra](https://github.com/PBundyra) — 2024-05-22T13:11:44Z

@alculquicondor @mimowo @mwielgus @tenzen-y WDYT?

### Comment by [@PBundyra](https://github.com/PBundyra) — 2024-05-22T13:12:52Z

If you agree with this idea I will add this to the v1beta2 wishlist.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-05-22T13:31:10Z

Yeah, I never liked the mechanism, but we may want to seek additional community feedback at the batch-wg meeting / slack.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-05-22T14:01:32Z

I agree with you, but let's keep it while v1beta1 for the backward compatibility.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-08-20T14:39:22Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-08-20T14:43:46Z

/remove-lifecycle stale

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-11T17:25:10Z

> I agree with you, but let's keep it while v1beta1 for the backward compatibility.

Keeping for backwards compatibility makes sense, but I think we can already deprecate it, so:
1. update the kube_features to mention it is deprecated, like [here](https://github.com/kubernetes/kubernetes/blob/c3ebd95c837a21c0c79ab64721c28bba44331bf9/pkg/features/kube_features.go#L49)
2. and also mention it is deprecated in the docs.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-11T17:26:17Z

Just to x-reference the related effort of promoting the VisibilityOnDemand to beta: https://github.com/kubernetes-sigs/kueue/issues/2973

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-20T09:49:34Z

@mbobrovskyi would you like to continue with this as a follow up to https://github.com/kubernetes-sigs/kueue/issues/2973?

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-09-20T10:14:26Z

/assign
