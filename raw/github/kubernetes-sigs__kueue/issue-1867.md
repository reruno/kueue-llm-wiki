# Issue #1867: Rework implementation for multiple admissions per cycle

**Summary**: Rework implementation for multiple admissions per cycle

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1867

**Last updated**: 2024-08-13T14:30:43Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2024-03-18T19:31:42Z
- **Updated**: 2024-08-13T14:30:43Z
- **Closed**: 2024-08-13T14:30:42Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@gabesaba](https://github.com/gabesaba)
- **Comments**: 7

## Description

**What would you like to be cleaned**:

Re-design the logic that allows multiple admissions to happen per cycle without incurring in over admission.

I think a simpler approach would be along the lines of modifying the snapshot (add admitted workloads and remove preempted workloads within the cycle) and checking if the incoming workload still fits. There is a special case for workloads needing preemption where there are no candidates for preemption. I think we can add a smaller fake workload that reserves space for the workload without going beyond the nominal quotas.

**Why is this needed**:

The current logic has been reworked multiple times with various pros and cons.

- #1866
- #1399
- #1024
- #805
- #475

Now it's very hard to follow.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-03-18T19:32:39Z

cc @yaroslava-serdiuk

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-06-16T20:03:46Z

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

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-06-25T20:47:53Z

/remove-lifecycle stale

### Comment by [@gabesaba](https://github.com/gabesaba) — 2024-07-16T10:38:21Z

/cc

### Comment by [@gabesaba](https://github.com/gabesaba) — 2024-07-19T13:39:43Z

/assign

### Comment by [@gabesaba](https://github.com/gabesaba) — 2024-08-13T14:30:38Z

in #2641, we enhance and simplify multiple preemption logic, by using the snapshot to account for usage. After promotion to beta in 0.9, we can delete the old code in 0.10

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-08-13T14:30:42Z

@gabesaba: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1867#issuecomment-2286405680):

>in #2641, we enhance and simplify multiple preemption logic, by using the snapshot to account for usage. After promotion to beta in 0.9, we can delete the old code in 0.10
>
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
