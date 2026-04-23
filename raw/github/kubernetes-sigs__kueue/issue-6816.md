# Issue #6816: Confusing annotation semantics for `kueue.x-k8s.io/retriable-in-group`

**Summary**: Confusing annotation semantics for `kueue.x-k8s.io/retriable-in-group`

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6816

**Last updated**: 2026-04-11T02:41:28Z

---

## Metadata

- **State**: open
- **Author**: [@ichekrygin](https://github.com/ichekrygin)
- **Created**: 2025-09-12T20:54:08Z
- **Updated**: 2026-04-11T02:41:28Z
- **Closed**: —
- **Labels**: `lifecycle/stale`
- **Assignees**: _none_
- **Comments**: 4

## Description

**Summary:**

Kueue’s *pod-integration* framework supports **pod groups**, allowing multiple Pods to be logically grouped and represented by a single Workload. This includes support for retrying failed Pods within the group—replacing them with new instances.

Currently, this *retriable Pods* behavior is enabled **by default**, and users can opt out by setting the following annotation on a Pod:

```
kueue.x-k8s.io/retriable-in-group=false
```

**Problem:**

In typical Kubernetes conventions, when a boolean annotation is omitted, the assumed default is usually `false` (i.e., opt-in behavior). However, in this case, the pod controller interprets the logic **inverted**, as shown in the current implementation:

```go
func isUnretriablePod(pod corev1.Pod) bool {
	return pod.Annotations[podconstants.RetriableInGroupAnnotationKey] == podconstants.RetriableInGroupAnnotationValue
}
```

This results in `retriable-in-group` being treated as `true` by default when:

* The annotation is **absent**
* The annotation is explicitly set to `"true"`

This inversion is both **non-idiomatic** and **confusing**, especially for users expecting opt-in semantics for behavior that changes workload retry characteristics.

**Proposed Change:**

A more natural and intuitive implementation would invert the check and follow the more typical “absent means false” pattern:

```go
func isUnretriablePod(pod corev1.Pod) bool {
	return pod.Annotations[podconstants.RetriableInGroupAnnotationKey] != "true"
}
```

This would make the semantics clearer:

* Pods are **not retriable** by default
* Pods become **retriable only when explicitly opted in**

**Alternatives Considered:**

* Keep current behavior but improve documentation to clarify the implicit default
* To avoid ambiguity and misinterpretation, and if opt-out behavior is desired, consider defaulting `kueue.x-k8s.io/retriable-in-group=true` 
* Use a different annotation key, e.g., `unretriable-in-group=true`, to reflect the actual logic (less preferred)

Unless there is strong justification for the current design, would you be open to flipping the logic to align with typical Kubernetes annotation expectations and avoid potential confusion for users and integrators?

## Discussion

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-12-11T21:37:36Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-01-10T22:33:21Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-11T01:46:43Z

/remove-lifecycle rotten
This is meaningful feedback, I think.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-04-11T02:41:24Z

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
