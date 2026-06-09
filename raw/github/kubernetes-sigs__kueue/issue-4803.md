# Issue #4803: Add `waitForPodsReady` to `Workload` API

**Summary**: Add `waitForPodsReady` to `Workload` API

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4803

**Last updated**: 2026-06-05T12:32:50Z

---

## Metadata

- **State**: open (reopened)
- **Author**: [@KPostOffice](https://github.com/KPostOffice)
- **Created**: 2025-03-26T20:01:24Z
- **Updated**: 2026-06-05T12:32:50Z
- **Closed**: —
- **Labels**: `kind/feature`, `lifecycle/rotten`
- **Assignees**: [@MaysaMacedo](https://github.com/MaysaMacedo)
- **Comments**: 19

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
`waitForPodsReady` per workload

**Why is this needed**:
I think it would be useful to be able to specify `waitForPodsReady` on a per Workload basis. Certain workloads may take longer to get to a ready state than others, so configuring this on at a cluster-wide scope feels awkward. These values can be propagated to the workload via annotations or labels maybe.

**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [x] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2025-03-26T21:10:59Z

https://github.com/kubernetes-sigs/kueue/tree/main/keps/349-all-or-nothing#more-granular-configuration-to-enable-the-mechanism

This was discussed briefly when this API was introduced.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-03-26T21:12:11Z

One issue is that workloads are not really exposed by Kueue so I think it would be labels/annotations on the Job objects that would get passed down to workload object once workload is created.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-06-25T06:09:14Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-07-25T06:24:54Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-25T06:34:48Z

/remove-lifecycle rotten

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-10-23T07:23:57Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-11-22T08:19:18Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-12-22T08:36:07Z

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

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-12-22T08:36:13Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4803#issuecomment-3681031678):

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

### Comment by [@kannon92](https://github.com/kannon92) — 2026-05-06T16:34:01Z

/reopen

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-05-06T16:34:07Z

@kannon92: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4803#issuecomment-4390111837):

>/reopen


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@kannon92](https://github.com/kannon92) — 2026-05-13T13:52:48Z

@mimowo @tenzen-y @PBundyra @amy 

WDYT of this? This came up as a feature request recently for us.

### Comment by [@amy](https://github.com/amy) — 2026-05-13T13:56:13Z

Not opposed. Probably also means you need a default number configured for the cluster though and not rely on users to remember to configure the number.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-05-13T14:45:18Z

I'm supportive for that 👍 

However, we need to iron out the details in the KEP. Some questions which come up to my mind:
1. should we enable that even if the global waitForPodsReady is disabled?
2. the API - probably a JSON-based annotation

### Comment by [@kannon92](https://github.com/kannon92) — 2026-05-13T14:52:50Z

cc @MaysaMacedo 
I followed up offline and she is interested in looking into this.

### Comment by [@MaysaMacedo](https://github.com/MaysaMacedo) — 2026-05-13T19:33:27Z

/assign

### Comment by [@PBundyra](https://github.com/PBundyra) — 2026-05-14T13:44:16Z

> I'm supportive for that 👍
> 
> However, we need to iron out the details in the KEP. Some questions which come up to my mind:
> 
> 1. should we enable that even if the global waitForPodsReady is disabled?
> 2. the API - probably a JSON-based annotation

+1 to all the above

### Comment by [@edmund-shi-arm](https://github.com/edmund-shi-arm) — 2026-06-03T15:34:03Z

really looking forward to this feature!!! what is the progress?

### Comment by [@kimminw00](https://github.com/kimminw00) — 2026-06-05T06:55:01Z

Heterogeneous workloads have very different readiness characteristics—large distributed jobs take much longer to become ready, while smaller jobs complete quickly. With `waitForPodsReady` configured globally, it is difficult to find a single value that fits all workloads in a congested, multi-tenant cluster. Short timeouts can cause premature eviction for large jobs, while long timeouts can delay smaller workloads and reduce overall efficiency. As a result, a one-size-fits-all configuration often leads to suboptimal scheduling behavior. For this reason, supporting `waitForPodsReady` at the Workload level is highly desirable and necessary to achieve efficient and reliable scheduling across diverse workloads.
