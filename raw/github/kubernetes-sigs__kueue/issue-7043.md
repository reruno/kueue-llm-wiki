# Issue #7043: Trainer v2 integration: Make the trainer_controller code Job-agnostic

**Summary**: Trainer v2 integration: Make the trainer_controller code Job-agnostic

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7043

**Last updated**: 2026-04-07T21:11:31Z

---

## Metadata

- **State**: open
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-09-29T10:48:08Z
- **Updated**: 2026-04-07T21:11:31Z
- **Closed**: —
- **Labels**: `kind/cleanup`
- **Assignees**: [@kaisoz](https://github.com/kaisoz)
- **Comments**: 6

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

I would like to make the trainer_controller Job agnostic as mentioned in the comment: https://github.com/kubernetes-sigs/kueue/pull/6997#discussion_r2377990539

To achieve that we may need to revisit the helpers exposed by the Trainer v2.

**Why is this needed**:

JobSet is just a "technical detail" of the Trainerv2 implementation, not user-facing.

In particular the future the Trainer v2 may use other runtime Jobs than Jobset. Also, Trainer v2 may want to use another version of the JobSet that we use in Kueue.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-29T10:48:23Z

cc @andreyvelich @tenzen-y @kaisoz

### Comment by [@kaisoz](https://github.com/kaisoz) — 2025-09-29T10:49:20Z

/assign

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-12-28T10:52:46Z

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

### Comment by [@kaisoz](https://github.com/kaisoz) — 2025-12-28T22:46:57Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-03-28T22:53:53Z

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

### Comment by [@kaisoz](https://github.com/kaisoz) — 2026-04-07T21:11:31Z

/remove-lifecycle stale
