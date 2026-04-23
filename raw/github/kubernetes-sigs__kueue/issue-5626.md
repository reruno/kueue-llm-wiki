# Issue #5626: TAS: add docs page "Setup Topology Aware Scheduling" with hands on experience

**Summary**: TAS: add docs page "Setup Topology Aware Scheduling" with hands on experience

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5626

**Last updated**: 2026-04-09T05:30:32Z

---

## Metadata

- **State**: open
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-06-11T14:04:42Z
- **Updated**: 2026-04-09T05:30:32Z
- **Closed**: —
- **Labels**: `kind/documentation`
- **Assignees**: [@sohankunkerkar](https://github.com/sohankunkerkar)
- **Comments**: 10

## Description

/kind documentation

I would like to add some "hands on" page for TAS. The feature is quite complex, especially with the Provisioning and Hot Swap features added. I imagine this could be subpage to [Manage Kueue](https://kueue.sigs.k8s.io/docs/tasks/manage/), like "Setup Topology Aware Scheduling". 

As a starter it could be just basic TAS, and in follow ups we could show some kubectl commands and how they translate into behavior of the cluster and the workloads.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-11T14:06:32Z

cc @pajakd @gabesaba @PBundyra @mwysokin  @tenzen-y 

I think it is out of scope for https://github.com/kubernetes-sigs/kueue/pull/5621, but I think such a page will be useful for users for learning, as TAS itself, and the features on top have nuances which are tricky to capture in a single paragraph.

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2025-06-11T18:46:26Z

@mimowo I can help with this one if possible.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-12T07:09:20Z

This is great @sohankunkerkar 👍 Please don't hesitate to report any bugs you encounter, or consult about the shape of the doc.

/assign @sohankunkerkar

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-09-10T07:44:47Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-10T08:08:38Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-12-09T09:06:32Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-01-08T09:57:03Z

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

### Comment by [@PBundyra](https://github.com/PBundyra) — 2026-01-08T10:00:46Z

/remove-lifecycle rotten

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-04-08T10:04:22Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-04-09T05:30:29Z

/remove-lifecycle stale
