# Issue #3103: Reevaluate the PodSpec equality factors

**Summary**: Reevaluate the PodSpec equality factors

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3103

**Last updated**: 2026-04-20T05:47:34Z

---

## Metadata

- **State**: open (reopened)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2024-09-19T21:18:25Z
- **Updated**: 2026-04-20T05:47:34Z
- **Closed**: —
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 20

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
We want to reevaluate the PodSpec equality factors and use only the necessary factors (fields) to identify the PodSpec.

https://github.com/kubernetes-sigs/kueue/blob/b9e173091c53456ae6858d9a10de81e6ba07ec62/pkg/util/equality/podset.go#L29-L37

**Why is this needed**:
The current approach sometimes causes unexpected update detection as we discussed in https://github.com/kubernetes-sigs/kueue/issues/3090.
So, it would be better to adopt the selective equality evaluation as opposed to the current nonselective equality.

Before we modify the actual equality function, we need to summarize the necessary fields for developers and users.

**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [ ] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-09-19T21:18:40Z

cc: @alculquicondor @dgrove-oss

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-09-23T17:26:53Z

Interestingly, I think we are missing some important fields, such as pod overhead.

But from within the containers, we just care about requests.

@mimowo anything else in the context of TAS?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-09-23T17:29:55Z

FYI: we need to be careful about pod group support, as we use the fields to build hashes. That list of fields will be harder to change. If we change the list and a pod group is running while there is a kueue upgrade, the new pods might be considered invalid.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-23T17:43:36Z

From the perspective of TAS I don't see a need to change this yet, but let me check my understanding.

There are 2 levels here: `PodSpec` and `Container`, and the current approach for comparing is mixed (based on the quoted `comparePodTemplate` function):
- selective at the level of PodSpec (only check Containers, InitContainers, and Tolerations), see the full list of fields [here](https://github.com/kubernetes/kubernetes/blob/851cf43a35862aeeafc4a0966f7d1e0836f675e4/pkg/apis/core/types.go#L3356)
- non-selective at the lower level of containers (the full list of fields [here](https://github.com/kubernetes/kubernetes/blob/851cf43a35862aeeafc4a0966f7d1e0836f675e4/pkg/apis/core/types.go#L2482))

So, the comment in code suggests to be less selective at the PodSpec level, while the issue here suggests to be more selective at the container level?

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2024-10-30T15:52:43Z

/assign dgrove-oss
I'll post a comment in the issue with the proposed fields to compare within the next week or so.  Assuming we converge on that, I can implement in time for 0.11.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-10-30T19:47:39Z

> From the perspective of TAS I don't see a need to change this yet, but let me check my understanding.
> 
> There are 2 levels here: `PodSpec` and `Container`, and the current approach for comparing is mixed (based on the quoted `comparePodTemplate` function):
> 
> * selective at the level of PodSpec (only check Containers, InitContainers, and Tolerations), see the full list of fields [here](https://github.com/kubernetes/kubernetes/blob/851cf43a35862aeeafc4a0966f7d1e0836f675e4/pkg/apis/core/types.go#L3356)
> * non-selective at the lower level of containers (the full list of fields [here](https://github.com/kubernetes/kubernetes/blob/851cf43a35862aeeafc4a0966f7d1e0836f675e4/pkg/apis/core/types.go#L2482))
> 
> So, the comment in code suggests to be less selective at the PodSpec level, while the issue here suggests to be more selective at the container level?

Actually, we aim to rework the comparative in both levels.
Anyway, I believe that @dgrove-oss can represent the direction later in this PR.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-01-28T20:10:51Z

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

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2025-01-28T20:14:30Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-04-28T20:16:47Z

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

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2025-04-28T20:35:18Z

/remove-lifecycle stale

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-07-01T15:26:13Z

A couple of observations about `comparePodTemplate`:

* It currently focuses on only three attributes:

  * `Tolerations` (excluded from comparison)
  * `Containers` and `InitContainers` (compared for equality)

Is that the intended scope? Based on the `// TODO` comment, I’m assuming it’s not.

I experimented with a more comprehensive `PodSpec` comparator and, during testing, observed the following:

* The production usage of `ComparePodSlices` is currently limited to:

  * `reconciler/EquivalentToWorkload`, all 3 invocations
  * `equality/TestComparePodSetSlices`, the remaining 1 invocation

* Regarding ignorable `PodSpec` fields:

  * It seems that `PodSpec` comparison (in the context of PodSets equality) is both:

    * **Workload state specific**, e.g., for admitted workloads we may want to ignore `Tolerations`, `NodeSelector`
    * **Integration-framework specific**, e.g., fields like `PodSchedulingReadinessGates` in pod-integration scenarios
  * Some fields appear to be universally ignorable across all frameworks, e.g., `PriorityClassName`
  * Some are specific to pod-integration, e.g., `SchedulingGates`
  * Some are conditionally ignorable only for **admitted** workloads, e.g., `Tolerations`, `NodeSelector`

**Questions:**

1. Is there a place, either in documentation or in code, that defines which `PodSpec` fields are considered mutable or ignorable in the context of PodSets equality?

   * Specifically:

     * Fields that are ignorable per workload state
     * Fields that are ignorable per job type/framework
     * Fields that are universally ignorable - for all frameworks + workload states.

2. Is there an effort (or interest) in generalizing this logic into a reusable, comprehensive `PodSpec` comparator with configurable field exclusions?

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2025-08-21T12:39:58Z

/unassign dgrove-oss

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-11-19T12:52:15Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-12-19T13:10:35Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-01-18T13:45:18Z

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

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-01-18T13:45:24Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3103#issuecomment-3765306939):

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-18T15:01:28Z

/reopen
/remove-lifecycle rotten

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-01-18T15:01:34Z

@tenzen-y: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3103#issuecomment-3765383658):

>/reopen
>/remove-lifecycle rotten


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-04-18T15:20:53Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-04-20T05:47:33Z

/remove-lifecycle stale
