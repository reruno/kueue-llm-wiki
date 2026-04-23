# Issue #7259: Missing validation for AdmissionCheckStrategy.OnFlavors

**Summary**: Missing validation for AdmissionCheckStrategy.OnFlavors

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7259

**Last updated**: 2026-04-10T09:30:29Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-10-14T08:41:55Z
- **Updated**: 2026-04-10T09:30:29Z
- **Closed**: 2026-04-10T09:30:29Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 5

## Description

**What happened**:

There is no validation for AdmissionCheckStrategy.OnFlavors  to check that the specified flavors are listed in quota. 

This is a follow up to discussion: https://github.com/kubernetes-sigs/kueue/pull/6785/files#r2428241242

As part of this task I would like to first summarize the status quo of what happens in that case. 

If this is not working at all, then we probably can add validation as a bugfix. 

If it works, but assumes "infinite quota" for the flavor, then it might be trickier if some users are using it.

**What you expected to happen**:

I would expect such CQ configuration to fail fast.

**How to reproduce it (as minimally and precisely as possible)**:

Create a CQ without flavors, but with AC specifiying some flavor in admissionCheckStrategy.OnFlavors.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-14T08:42:05Z

cc @PBundyra @ganczak-commits

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-01-12T08:51:21Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-12T08:57:35Z

/remove-lifecycle stale

### Comment by [@ShaanveerS](https://github.com/ShaanveerS) — 2026-04-08T07:20:21Z

While working on this I ran into one compatibility question.
For preexisting ClusterQueues, do we want to reject any update if they contain any invalid onFlavors refs, or only updates that change those refs?

### Comment by [@mimowo](https://github.com/mimowo) — 2026-04-08T07:41:01Z

@ShaanveerS good question. Ideally, if there is a pre-existing CLusterQueue with the invalid onFlavors, then we still allow updates to the unrelated fields. This is the common practice in the core k8s to allow graceful handling of some environments.
