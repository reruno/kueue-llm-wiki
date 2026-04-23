# Issue #1986: Use quantity library and optional types once 1.28 reaches EoL

**Summary**: Use quantity library and optional types once 1.28 reaches EoL

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1986

**Last updated**: 2025-12-02T12:25:51Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@IrvingMg](https://github.com/IrvingMg)
- **Created**: 2024-04-16T07:55:23Z
- **Updated**: 2025-12-02T12:25:51Z
- **Closed**: 2025-12-02T12:19:04Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@IrvingMg](https://github.com/IrvingMg)
- **Comments**: 18

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

1. We can remove the validation functions implemented for `ClusterQueue`  in fields with `resource.Quantity` type.
2. Additionally, we can shorten some rules that use the macro `has()` to check an optional field exists.

**Why is this needed**:

1. Since Kubernetes 1.29, we can use [Kubernetes quantity library](https://kubernetes.io/docs/reference/using-api/cel/#kubernetes-quantity-library) to validate fields of `resource.Quantity` type. 
2. Likewise, we can rewrite some rules to make them more concise using [CEL optional types](https://pkg.go.dev/github.com/google/cel-go@v0.17.4/cel#OptionalTypes).

Discussion: 
- https://github.com/kubernetes-sigs/kueue/pull/1972#discussion_r1565962705
- https://github.com/kubernetes-sigs/kueue/pull/2008#discussion_r1576665882

## Discussion

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-07-28T15:14:36Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-07-29T05:13:00Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-10-27T05:25:50Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-10-27T05:53:44Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-01-25T06:46:47Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-27T07:53:41Z

/remove-lifecycle stale
I would prefer to wait another release until 1.29 is EOL to give some buffer for users to migrate. 

Also, I would like to understand the consequences on the older versions - would the non-supported validation syntax break the API operations, or the API-server would just ignore the non-supported validations?

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-04-27T08:01:46Z

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

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-04-27T08:16:54Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-07-26T08:44:51Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-08-25T08:51:00Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-25T09:02:56Z

/remove-lifecycle rotten

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-11-23T09:33:19Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-24T07:17:59Z

/remove-lifecycle stale

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2025-12-01T09:34:07Z

/assign

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2025-12-02T10:38:13Z

After making some updates and running tests, neither Point 1 nor Point 2 from this issue can be implemented due to CEL cost-budget constraints in Kubernetes. See https://kubernetes.io/docs/reference/using-api/cel/#resource-constraints.

1. CEL Quantity Library for Resource Validations
The use of the quantity() function is too expensive. This is discussed in https://github.com/kubernetes/kubernetes/issues/132370, where some workarounds are proposed, but I believe they are not worth it for Kueue, as they would introduce temporary workarounds into the API. It is better to keep the current validations in Go code instead.

2. Optional Types for Simplifying CEL Rules
Even though the syntax is cleaner when using optional types, they are also expensive and easily exceed the CEL cost budget. Setting maxItems limits as recommended does not help. For example, adding a maxItems=16 constraint to the Conditions array in WorkloadStatus in v1beta1 did not help.

CEL cost-budget limitations have appeared before in related tasks such as #1972 and #2008. There are also further discussions here: https://github.com/kubernetes/kubernetes/issues/121162.

Therefore, I suggest closing this issue because, given the current CEL budget limitations, I don’t think it is possible to make any meaningful improvements.

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2025-12-02T12:18:59Z

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-12-02T12:19:05Z

@IrvingMg: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1986#issuecomment-3601756287):

>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-12-02T12:25:50Z

> After making some updates and running tests, neither Point 1 nor Point 2 from this issue can be implemented due to CEL cost-budget constraints in Kubernetes. See https://kubernetes.io/docs/reference/using-api/cel/#resource-constraints.
> 
> 1. CEL Quantity Library for Resource Validations
>    The use of the quantity() function is too expensive. This is discussed in [quantity() cel cost is too high kubernetes/kubernetes#132370](https://github.com/kubernetes/kubernetes/issues/132370), where some workarounds are proposed, but I believe they are not worth it for Kueue, as they would introduce temporary workarounds into the API. It is better to keep the current validations in Go code instead.
> 2. Optional Types for Simplifying CEL Rules
>    Even though the syntax is cleaner when using optional types, they are also expensive and easily exceed the CEL cost budget. Setting maxItems limits as recommended does not help. For example, adding a maxItems=16 constraint to the Conditions array in WorkloadStatus in v1beta1 did not help.
> 
> CEL cost-budget limitations have appeared before in related tasks such as [#1972](https://github.com/kubernetes-sigs/kueue/pull/1972) and [#2008](https://github.com/kubernetes-sigs/kueue/pull/2008). There are also further discussions here: [kubernetes/kubernetes#121162](https://github.com/kubernetes/kubernetes/issues/121162).
> 
> Therefore, I suggest closing this issue because, given the current CEL budget limitations, I don’t think it is possible to make any meaningful improvements.

SGTM, thank you for investigating that 👍
