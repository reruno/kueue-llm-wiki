# Issue #6185: MultiKueue: remove the limitation that the external dispatches need to use kueue-admission field manager

**Summary**: MultiKueue: remove the limitation that the external dispatches need to use kueue-admission field manager

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6185

**Last updated**: 2026-04-20T09:20:51Z

---

## Metadata

- **State**: open
- **Author**: [@mszadkow](https://github.com/mszadkow)
- **Created**: 2025-07-25T13:08:34Z
- **Updated**: 2026-04-20T09:20:51Z
- **Closed**: —
- **Labels**: `kind/feature`, `priority/important-longterm`, `area/multikueue`
- **Assignees**: _none_
- **Comments**: 7

## Description

**What would you like to be added**:
Find a way to eliminate the need for external dispatchers to use Kueue-admission field manager.

**Why is this needed**:

As mentioned in the [comment](https://github.com/kubernetes-sigs/kueue/pull/5782#discussion_r2229169112)

The [External Dispatcher](https://kueue.sigs.k8s.io/docs/concepts/multikueue/#external-custom-implementation) is responsible for dispatching Workloads in MultiKueue. 
When it updates the `.status.nominatedClusterNames` field, it takes ownership of the field. 
This creates a conflict because Kueue, which is responsible for clearing the field after a workload secures a reservation on the nominated cluster, uses a different field manager to modify it. 
As a result, Kueue is unable to update or clear the field. 
Additionally, attempting to set a new owner and clear the field simultaneously is not feasible, as an empty value is ignored during the patch process.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-12T11:47:52Z

I synced with @mszadkow and the idea for the task is as in the new title:
/retitle MultiKueue: remove the limitation that the external dispatches need to use kueue-admission field manager

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-11-10T12:29:07Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-11-10T16:07:39Z

/remove-lifecycle stale

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T08:24:45Z

/area multikueue
/priority important-longterm

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-03-19T08:44:23Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-04-18T09:13:53Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-04-20T09:20:48Z

/remove-lifecycle rotten
