# Issue #2154: Enhance troubleshooting to understand if a job is actually running

**Summary**: Enhance troubleshooting to understand if a job is actually running

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2154

**Last updated**: 2025-05-02T18:16:04Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2024-05-07T14:44:59Z
- **Updated**: 2025-05-02T18:16:04Z
- **Closed**: 2025-05-02T18:16:02Z
- **Labels**: `lifecycle/rotten`, `kind/documentation`
- **Assignees**: [@alculquicondor](https://github.com/alculquicondor), [@mwysokin](https://github.com/mwysokin)
- **Comments**: 12

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

This question just refers to whether the job is suspended https://kueue.sigs.k8s.io/docs/tasks/troubleshooting/troubleshooting_jobs/#is-my-job-running

In some cases, the suspend field can be false, while the pods are unschedulable.

It would be useful to make the distinction.

**Why is this needed**:

Users don't necessarily understand the separation of concerns between kueue and kube-scheduler or cluster-autoscaler. We need to direct them to ask the right questions.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-05-09T05:40:38Z

/remove-kind feature
/kind documentation

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-09T20:20:52Z

/assign

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-06-25T20:36:30Z

I wrote #2185, but I think it can still be improved by adding the question "Is my job running?" that somehow introduces the other questions.

### Comment by [@mwysokin](https://github.com/mwysokin) — 2024-07-02T14:55:05Z

/assign

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-09-30T15:05:26Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-10-01T17:33:40Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-12-30T17:48:00Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-01-01T16:40:09Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-04-02T14:49:22Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-05-02T15:39:54Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-02T18:15:58Z

Let's close this for now. We already have a lot of meaningful troubleshooting guide: https://kueue.sigs.k8s.io/docs/tasks/troubleshooting/


/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-05-02T18:16:02Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/2154#issuecomment-2847821046):

>Let's close this for now. We already have a lot of meaningful troubleshooting guide: https://kueue.sigs.k8s.io/docs/tasks/troubleshooting/
>
>
>/close
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
