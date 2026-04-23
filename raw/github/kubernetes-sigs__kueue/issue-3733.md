# Issue #3733: TAS: cache information is not updated when RF spec (nodeTaints or tolerations) is changed

**Summary**: TAS: cache information is not updated when RF spec (nodeTaints or tolerations) is changed

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3733

**Last updated**: 2026-03-01T08:34:14Z

---

## Metadata

- **State**: open (reopened)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-12-04T10:40:14Z
- **Updated**: 2026-03-01T08:34:14Z
- **Closed**: —
- **Labels**: `kind/bug`
- **Assignees**: [@PBundyra](https://github.com/PBundyra)
- **Comments**: 16

## Description


**What happened**:

When TAS RF is updated (e.g. nodeTaints or tolerations), then the cache information is not updated.

**What you expected to happen**:

Update the cache or fail the update. I think updating cache would be ideal, but it might be hard to deliever before 0.10, 
so we may just block updates for now (when topologyName is specified).

**How to reproduce it (as minimally and precisely as possible)**:

Create a TAS setup, and add the .spec.tolerations.
issue: the tolerations are not added to the newly admitted workloads.

**Anything else we need to know?**:

We had a similar decision about update to the levels and decided to block updates for now: https://github.com/kubernetes-sigs/kueue/issues/3614

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-04T10:40:29Z

/assign @PBundyra 
tentatievly
cc @mbobrovskyi

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-03-04T10:41:15Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-04T21:31:52Z

/remove-lifecycle stale

### Comment by [@qti-haeyoon](https://github.com/qti-haeyoon) — 2025-04-15T05:14:23Z

Hi @mimowo , do we have plan to make resource flavor spec mutable again? Moreover, it is currently not possible to remove `topologyName` from `ResourceFlavor` in case we want to not use TAS anymore. Is this intended behavior?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-04-15T05:19:49Z

Hi, we want to support mutating TAS RF spec long term, we just didn't have the capacity to do it right in the early phases. 

So disabling mutations was a conservative move to avoid bugs. There is no timeline to support mutations on our side but we can consider contributions. 

cc@mwielgus @mwysokin

### Comment by [@mimowo](https://github.com/mimowo) — 2025-04-15T05:34:55Z

cc @mwielgus

### Comment by [@xiongzubiao](https://github.com/xiongzubiao) — 2025-07-03T17:52:34Z

Any new plan to support mutation when topologyName is specified, by any chance?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-03T18:06:57Z

It is not prioritized at the moment, but I would welcome contributions.

I think mutating RF's .spec.tolerations should be relatively easy as it does not impact cached TAS usage (we can start here).

However, mutating spec.nodeLabels impacts cached TAS usage, so we need to choose:
1. drop the usage completely and start rebuilding from scratch
2. keep cache usage as if nothing happened
3. update cache usage by dropping usage for workloads which no longer match the new spec.nodeLabels

I think (1.) is problematic, because it will lead to overadmission of workloads. Probably (3.) is most accurate.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-10-01T19:03:20Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-10-31T19:57:04Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-11-30T20:26:25Z

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

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-11-30T20:26:30Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3733#issuecomment-3593300399):

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-01T07:30:46Z

/remove-lifecycle rotten
/reopen

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-12-01T07:30:52Z

@mimowo: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3733#issuecomment-3595018985):

>/remove-lifecycle rotten
>/reopen


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-03-01T07:46:40Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-03-01T08:34:11Z

/remove-lifecycle stale
