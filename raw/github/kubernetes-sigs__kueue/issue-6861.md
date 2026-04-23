# Issue #6861: Preemption cycling detection / instrumentation

**Summary**: Preemption cycling detection / instrumentation

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6861

**Last updated**: 2026-03-20T06:54:27Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@amy](https://github.com/amy)
- **Created**: 2025-09-16T16:16:17Z
- **Updated**: 2026-03-20T06:54:27Z
- **Closed**: 2026-03-20T06:54:26Z
- **Labels**: `kind/feature`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 13

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
I'd like some mechanism to determine if a workload is entering cyclical preemptions. 

**Why is this needed**:
Seeing workloads that get preempted over 100 times using burst. I identified that some of these preemptions are due to cyclical preemptions. Regardless of the causes, I want to be able to differentiate cyclical preemptions vs "valid" preemptions. Here's the upstream reasons that could be causing this for context:
- admission candidate selection: https://github.com/kubernetes-sigs/kueue/pull/6846
- non-deterministic preemption targets selection: https://github.com/kubernetes-sigs/kueue/pull/6764
- Precision issues: https://github.com/kubernetes-sigs/kueue/issues/6774

(Less interested in fixing the causes for this issue scope. More interested in the detection part.)

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@amy](https://github.com/amy) — 2025-09-16T16:16:37Z

cc/ @PBundyra @gabesaba

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-16T16:19:25Z

Cyclic preemptions are due to bugs, so ideally once we solve all the bugs there would be no way to see the observability code works :)

### Comment by [@amy](https://github.com/amy) — 2025-09-16T16:26:12Z

@mimowo Perhaps, but how can we externally validate that these fixes are comprehensive and that there's no more cycles? A high rate of preemption could be just a normal busy cluster, or it could be preemption cycling. Digging into each workload to determine the reasoning is a lot of effort. 

For validation, purely for testing we make the changes on an old version with cycles. Repro the issue, and see if the metrics works is one suggestion.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-16T16:53:19Z

> how can we externally validate that these fixes are comprehensive and that there's no more cycles?

Good question. There are various approaches probably like log analysis, or watching for the stream of events.  Then, we could look for pairs of workloads which are interleaving preemption and admission. They would be mentioning each others UIDs in their condition messages for example.

### Comment by [@amy](https://github.com/amy) — 2025-09-16T17:03:47Z

Let's brainstorm! 🧠⛈️ The mechanism needs to be comprehensive for existing cycles today (ie did the fixes work?). And also be able to alert for cycles should they occur from future code changes.

Basically, what I don't want, is for a customer to tell me something wrong is happening in the burst space. I'd like to be proactively alerted and fix the issue ahead of time.

`There are various approaches probably like log analysis, or watching for the stream of events. Then, we could look for pairs of workloads which are interleaving preemption and admission.`
^ this is one type of cycle.

For this one: https://github.com/kubernetes-sigs/kueue/pull/6846
The cycling workload had a lot of different preemptors with drs value 1. Its because CQ with same DRS is ordered by timestamp in FIFO. This is another type.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-12-15T17:27:10Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-01-14T18:17:43Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-02-13T19:16:05Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues and PRs.

This bot triages issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Reopen this issue with `/reopen`
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/close not-planned

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-02-13T19:16:12Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/6861#issuecomment-3898931974):

>The Kubernetes project currently lacks enough active contributors to adequately respond to all issues and PRs.
>
>This bot triages issues according to the following rules:
>- After 90d of inactivity, `lifecycle/stale` is applied
>- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
>- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed
>
>You can:
>- Reopen this issue with `/reopen`
>- Mark this issue as fresh with `/remove-lifecycle rotten`
>- Offer to help out with [Issue Triage][1]
>
>Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).
>
>/close not-planned
>
>[1]: https://www.kubernetes.dev/docs/guide/issue-triage/


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@amy](https://github.com/amy) — 2026-02-18T06:14:03Z

/reopen

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-02-18T06:14:09Z

@amy: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/6861#issuecomment-3918940663):

>/reopen


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-03-20T06:54:20Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues and PRs.

This bot triages issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Reopen this issue with `/reopen`
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/close not-planned

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-03-20T06:54:27Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/6861#issuecomment-4096054354):

>The Kubernetes project currently lacks enough active contributors to adequately respond to all issues and PRs.
>
>This bot triages issues according to the following rules:
>- After 90d of inactivity, `lifecycle/stale` is applied
>- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
>- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed
>
>You can:
>- Reopen this issue with `/reopen`
>- Mark this issue as fresh with `/remove-lifecycle rotten`
>- Offer to help out with [Issue Triage][1]
>
>Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).
>
>/close not-planned
>
>[1]: https://www.kubernetes.dev/docs/guide/issue-triage/


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
