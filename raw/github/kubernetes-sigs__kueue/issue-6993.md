# Issue #6993: Introduce a Gauge and Counter metrics to track the number of "Finished" workloads

**Summary**: Introduce a Gauge and Counter metrics to track the number of "Finished" workloads

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6993

**Last updated**: 2026-01-26T12:31:58Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-09-24T14:32:16Z
- **Updated**: 2026-01-26T12:31:58Z
- **Closed**: 2026-01-26T12:31:58Z
- **Labels**: `kind/feature`, `priority/important-soon`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 12

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Add metric to track the current number of Finished workloads.

**Why is this needed**:

For observability, for example it may help to decide on enabling the ObjectRetentionPolicy.

It may also help admins or oncallers to decide if ObjectRetentionPolicy for finished workloads should be enabled.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-24T14:32:50Z

cc @MichalZylinski @mwysokin @helayoty

### Comment by [@izturn](https://github.com/izturn) — 2025-10-16T09:42:37Z

I'd like to give it a try. @mimowo

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-16T09:43:35Z

👍

### Comment by [@izturn](https://github.com/izturn) — 2025-10-16T09:50:58Z

/assign

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-01-14T10:09:44Z

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

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-01-14T10:30:35Z

/remove-lifecycle stale

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-01-14T10:30:51Z

@izturn are you still working on it?

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-19T13:32:22Z

Let me unassign as no progress for a couple of months, and we have a user interested in this.
/unassign

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-19T13:32:33Z

/priority important-soon

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-19T13:33:08Z

/assign @mbobrovskyi 
tentatively

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-01-19T13:42:39Z

/unassign @izturn

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-19T16:19:01Z

/retitle Introduce a Guage and Counter metrics to track the number of "Finished" workloads 

We will also need a counter so that we can answer questions like "how many workloads finished in 1h".
