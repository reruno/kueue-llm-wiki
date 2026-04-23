# Issue #4545: workload.Usage type safety

**Summary**: workload.Usage type safety

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4545

**Last updated**: 2026-04-15T10:42:37Z

---

## Metadata

- **State**: open
- **Author**: [@gabesaba](https://github.com/gabesaba)
- **Created**: 2025-03-10T15:34:45Z
- **Updated**: 2026-04-15T10:42:37Z
- **Closed**: —
- **Labels**: `kind/cleanup`
- **Assignees**: [@iomarsayed](https://github.com/iomarsayed)
- **Comments**: 14

## Description

**What would you like to be cleaned**:
I would like to differentiate Usage before and after flavor assignment. Perhaps by defining a different type for the Usage that has empty flavor strings - or making this invalid. See this comment:

https://github.com/kubernetes-sigs/kueue/blob/ba7faec2950f8748c141a0ab2b866eed7a1b1b13/pkg/workload/workload.go#L251-L252

**Why is this needed**:
It is too easy to use this type incorrectly, as I found after spending 15 mins root causing a bug in my code to flavor being "".

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-10T16:03:45Z

Yeah, I agree, I also got into the time trap at some point working on TAS.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-06-08T16:42:14Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-09T06:56:48Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-09-07T07:24:50Z

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

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-09-08T12:54:30Z

/remove-lifecycle stale

### Comment by [@iomarsayed](https://github.com/iomarsayed) — 2025-10-13T08:40:25Z

/assign

### Comment by [@iomarsayed](https://github.com/iomarsayed) — 2025-10-16T13:46:34Z

@gabesaba @mimowo 

I have carefully reviewed the problem.

I can confirm that to invalidate/eliminate empty string flavor without model changes seems infeasible. Because empty string flavor accommodates for resources that are required by a workload but just not yet assigned to a flavor. Hence the solution is to change the model "resources.FlavorResourceQuantities" which is used to describe usage. But changing the model will impose many code changes as it is used widely.

I already have two possibilities for model changes to handle and provide different type for usage of yet-to-be-assigned flavors (empty string flavors), but want to make sure that amount of changes are acceptable.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-16T15:37:53Z

Thank you @iomarsayed for the summary, could you provide some more details into the possible proposals.

I indeed expect the amount of changes is going to be large, but I think it is better now than never. Using the empty string is very confusing here for debugging.

### Comment by [@iomarsayed](https://github.com/iomarsayed) — 2025-10-17T09:36:20Z

@mimowo Okay great, so what I am proposing and actually do prefer having a structure like this:

```
type ResourceUsage struct {
	Assigned       map[FlavorResource]int64 // an entry example: "flavor: on-demand, resource: cpu" -> 4
	Unassigned   map[ResourceName]int64 // an entry example: "resource: cpu" -> 8
}
```

For the reference here is the old one:
```
type ResourceUsage struct {
	alltogether     map[FlavorResource]int64 // an entry example: "flavor: "", resource: cpu" -> 4
}
```

This will cause minimal disruptions to the code, but will separate between what is assigned, and what is yet to be assigned and eliminate empty flavor strings.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-17T09:48:18Z

the proposal lgtm, would like to see it in practice

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-01-15T10:22:46Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-15T10:28:50Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-04-15T10:36:50Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2026-04-15T10:42:35Z

/remove-lifecycle stale
