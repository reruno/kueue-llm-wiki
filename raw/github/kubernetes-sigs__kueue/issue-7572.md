# Issue #7572: Document all Workload status condition types and their lifecycle transitions in Kueue API

**Summary**: Document all Workload status condition types and their lifecycle transitions in Kueue API

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7572

**Last updated**: 2026-04-18T12:16:56Z

---

## Metadata

- **State**: open
- **Author**: [@ichekrygin](https://github.com/ichekrygin)
- **Created**: 2025-11-07T01:41:15Z
- **Updated**: 2026-04-18T12:16:56Z
- **Closed**: —
- **Labels**: `priority/important-longterm`, `lifecycle/rotten`, `kind/documentation`
- **Assignees**: _none_
- **Comments**: 3

## Description

**What would you like to be added**
Complete documentation for all `Workload` status condition types in Kueue.

**Why is this needed**
The current [Kueue API Workload status conditions](https://kueue.sigs.k8s.io/docs/reference/kueue.v1beta1/#kueue-x-k8s-io-v1beta1-WorkloadStatus) documentation is incomplete and only lists three of eight defined conditions: `Admitted`, `Finished`, and `PodsReady`.
A full list with definitions, expected transitions, and semantics is needed for developers and users to correctly interpret Workload state and controller behavior.

**Scope**
The update should document all currently defined condition types, including but not limited to:

* `Admitted`
* `Finished`
* `PodsReady`
* `Preempted`
* `Evicted`
* `WaitingForAdmission`
* `Dequeued`
* `QuotaReserved`

For each condition type, include:

* Meaning and when it is set
* Typical transition points (e.g., who sets/unsets it)
* Expected combinations with other conditions

**Completion requirements**
This enhancement requires the following artifacts:

* [ ] Design document
* [ ] API change (if any new or renamed condition types are introduced)
* [x] Documentation update

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T10:36:05Z

/remove-kind feature
/kind documentation
/priority important-longterm

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-03-19T11:47:18Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-04-18T12:16:53Z

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
