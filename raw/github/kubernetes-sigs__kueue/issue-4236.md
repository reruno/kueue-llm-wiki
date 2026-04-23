# Issue #4236: Prepare PartialAdmission for graduation to GA

**Summary**: Prepare PartialAdmission for graduation to GA

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4236

**Last updated**: 2026-01-25T10:22:54Z

---

## Metadata

- **State**: open
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-02-12T09:11:25Z
- **Updated**: 2026-01-25T10:22:54Z
- **Closed**: —
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 13

## Description

**What would you like to be added**:

Prepare Partial Admission for graduation to GA. We can keep it in Beta for another releases, but we need to drive it towards graduation. If all is done we can graduate the feature to GA.

In particular, 
- I would like to extend the coverage and API for all supported built-in Jobs. Note that currently it is only supported for batch Jobs.
- Solve the outstanding problem of interaction with reclaimable pods: https://github.com/kubernetes-sigs/kueue/issues/3141

For reference the KEP: https://github.com/kubernetes-sigs/kueue/tree/main/keps/420-partial-admission

**Why is this needed**:

- to simplify code, currently we need to maintain two paths in code depending on the feature enablement
- to make Kueue graduation process more trusted, keeping features in Beta for 6 or more releases does not make a good impression (it is beta since 0.5) (lead by the question in https://github.com/kubernetes-sigs/kueue/issues/4236)
- to provide the functionality for all Job types (not just batch Job)
- to provide the functionality to users in a reliable way

**Completion requirements**:

I would like to revisit the KEP and start with its update. Unfortunately currently it does not mention any requirements.

This enhancement requires the following artifacts:

- [x] Design doc
- [x] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-12T09:12:36Z

cc @tenzen-y @mwielgus @mwysokin

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-12T09:37:13Z

cc @dgrove-oss

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-12T13:16:10Z

+1

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2025-02-12T20:48:21Z

An implementation for AppWrapper would be similar to what we would do for #4237. Once it is implemented for a critical mass of other kinds it makes sense to implement for AppWrapper too.

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-02-20T08:18:35Z

/assign

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-05-21T08:26:51Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-21T08:38:29Z

/remove-lifecycle stale

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-21T08:47:07Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-08-19T09:10:54Z

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

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-08-19T09:16:05Z

/remove-lifecycle stale

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-10-27T09:07:07Z

/unassign

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-01-25T09:28:40Z

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

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-01-25T10:22:52Z

/remove-lifecycle stale
