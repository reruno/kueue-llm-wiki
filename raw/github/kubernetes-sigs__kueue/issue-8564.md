# Issue #8564: MultiKueue: performance testing

**Summary**: MultiKueue: performance testing

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8564

**Last updated**: 2026-06-16T12:01:28Z

---

## Metadata

- **State**: open
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-01-13T16:35:01Z
- **Updated**: 2026-06-16T12:01:28Z
- **Closed**: —
- **Labels**: `kind/feature`, `priority/important-soon`, `lifecycle/rotten`, `area/multikueue`
- **Assignees**: _none_
- **Comments**: 4

## Description

**What would you like to be added**:

Performance test for MultiKueue . 

We would like to observe the rate of processing workloads assuming there are 3 (or so) worker clusters.

I imagine this is a dedicated CI job. It will be hard in OSS on kind to get beyond 3 clusters probably, or otherwise we will anyway saturate the resources of the host node running the CI job.



**Why is this needed**:

To allow detecting performance regressions in MultiKueue.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-14T13:31:01Z

/priority important-soon

### Comment by [@olekzabl](https://github.com/olekzabl) — 2026-02-16T10:50:32Z

/area multikueue

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-05-17T11:20:52Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-06-16T12:01:25Z

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
