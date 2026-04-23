# Issue #1164: [rayjob] status update not as timely as expected

**Summary**: [rayjob] status update not as timely as expected

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1164

**Last updated**: 2024-01-30T09:34:52Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kerthcet](https://github.com/kerthcet)
- **Created**: 2023-09-26T15:50:54Z
- **Updated**: 2024-01-30T09:34:52Z
- **Closed**: 2024-01-30T09:34:51Z
- **Labels**: `kind/feature`, `lifecycle/stale`
- **Assignees**: _none_
- **Comments**: 5

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

When rayjob is admitted, the status is not updated, it should be `Pending` I think.
Also, when rayjob is preempted and status transmit to `STOPPED`. Then when rayjob is `admitted` again, the status should transmit to `Pending` rather stays in `STOPPED`.

**Why is this needed**:

Better describe the job status.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-09-27T13:06:50Z

Isn't this on the rayjob side? the implementation of suspend?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-10-10T16:44:13Z

@achernevskii can you take this one?
It seems to me that this would be in kuberay side, not kueue.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-10-11T07:14:02Z

Sorry, I just recorded here in case of forgotten, sorry for the confusion, I will dig into the reason and close this if necessary.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-01-30T03:14:46Z

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

### Comment by [@kerthcet](https://github.com/kerthcet) — 2024-01-30T09:31:45Z

/close as not kueue's responsibility.
