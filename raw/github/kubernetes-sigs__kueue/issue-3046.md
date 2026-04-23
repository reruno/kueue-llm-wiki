# Issue #3046: Merge the FlowSchema and PriorityLevelConfiguration v1 manifests into the installation manifests

**Summary**: Merge the FlowSchema and PriorityLevelConfiguration v1 manifests into the installation manifests

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3046

**Last updated**: 2025-04-18T15:29:16Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2024-09-13T18:17:19Z
- **Updated**: 2025-04-18T15:29:16Z
- **Closed**: 2025-04-18T15:29:16Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 5

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

As we discussed [here](https://github.com/kubernetes-sigs/kueue/pull/3043#discussion_r1764680475) and [here](https://github.com/kubernetes-sigs/kueue/pull/3043#discussion_r1764915102) we should merge the FlowSchema and PriorityLevelConfiguration v1 manifests into the installation manifests and remove v1beta3 manifests once the latest Kubernetes version (1.28) no longer supports v1beta3.

**Why is this needed**:

 - During the second iteration of [Graduation criteria](https://github.com/kubernetes-sigs/kueue/tree/3a428360818bab0f1618edcbdea26dd94b4ca6e5/keps/168-2-pending-workloads-visibility#beta) of visibility we need to merge manifests.

 - Due to flowcontrol.apiserver.k8s.io/v1beta3 FlowSchema is deprecated in v1.29+ and unavailable in v1.32+ we don't need to support v1beta3 anymore.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-16T10:01:07Z

Question regarding the support: https://github.com/kubernetes-sigs/kueue/pull/3043#discussion_r1760626660. I'm wondering what happens if 1.32 is released, so we release 0.10 Kueue according to the plan. IIUC this will complicate deployment of the latest Kueue on 1.31 which will be still used by majority of clusters at that point.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-09-18T15:43:10Z

@mbobrovskyi Could you update this issue to align with the latest decision?

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-12-18T08:22:49Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-18T08:24:13Z

/remove-lifecycle stale

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-28T11:04:01Z

As discussed in https://github.com/kubernetes-sigs/kueue/pull/3983#discussion_r1925026803 I prefer to keep the APF configuration as opt-in for a while longer after the last EOL release of Kubernetes. 

I'm ok some features of Kueue not working ideally on older versions, but not being to install at all is a flag,  because we claim Kueue can be at least installed on older versions (as in the main README: `A Kubernetes cluster with version 1.25 or newer is running. Learn how to [install the Kubernetes tools](https://kubernetes.io/docs/tasks/tools/).`. I would prefer to keep it that way, as the additional release will be very helpful for some users to migrate away for a version that just became EOL.

I propose to merge the configuration only when 1.30 gets EOL (+1 release). Then we update the README to claim Kueue installation is supported on 1.29+. 

Unless there are other ideas, or other factors at play.
