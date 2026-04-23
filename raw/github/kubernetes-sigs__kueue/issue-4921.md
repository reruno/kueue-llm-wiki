# Issue #4921: Introduce some concept of graduation of new jobframework interfaces

**Summary**: Introduce some concept of graduation of new jobframework interfaces

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4921

**Last updated**: 2026-03-02T05:24:15Z

---

## Metadata

- **State**: open
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-04-10T15:00:26Z
- **Updated**: 2026-03-02T05:24:15Z
- **Closed**: —
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 9

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Introduce some form of graduation for new jobframework interfaces. 

For example:
1. keep new interfaces under "alpha_interfaces.go/internal_interfaces" file
2. more the new interfaces outside of the jobframework package (to move them to unexported package), similar idea to https://github.com/kubernetes-sigs/kueue/issues/4615
3. consolidate the existing interfaces into just "PodIntegration" interface (as most, if not all, of them are created for the needs of the Pod integration, which is very special)

**Why is this needed**:

TLDR: For long term maintainability of the project, to keep exported only what is needed. This is also related to the more general issue https://github.com/kubernetes-sigs/kueue/issues/4615.

Longer: Some interfaces are only introduced to support internal Kueue mechanics, and are not requested by users. We need more time to confirm the interfaces create the proper layer of abstraction. Withdrawing from a wrong layer of abstraction is difficult. 

Thus, reviewing new interfaces is much more involving, because we need to make sure they are named properly, and reflect the proper layer of abstraction, which would not be necessary if we considered the interfaces internal / alpha and free to change in the future. In many cases it is very hard to tell if they are correct, because we have only one implementation - Pod integration.

Examples of such interfaces are JobWithSkip, ComposableJob, JobWithFinalize, IsTopLevelJob (all are created just for Pod integration currently) , but many more we created over time. It is not clear if users use them. I raised this as a concern in https://github.com/kubernetes-sigs/kueue/pull/4824#discussion_r2032813446. For example, with the introduction of the support for serving workloads we may need to rename them "Job" -> Workload, or Job -> Task.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-04-10T15:00:43Z

cc @gabesaba @PBundyra @mbobrovskyi @tenzen-y @dgrove-oss

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2025-04-11T18:27:19Z

This proposal makes sense to me.  

As we progress on #4615 it definitely makes sense to move a little slower when promoting interfaces / functions from `internal` to `pkg`. 

I like the idea of consolidating all of the seemingly "general" interfaces that are only implemented by the Pod integration into an explicit`PodIntegration` interface instead.  Pods are special in our implementation and will be so for the foreseeable future. When we first started working on the AppWrapper integration, we went down a dead-end of trying to use the `ComposableJob` interface for AppWrapper (because an AppWrapper can contain multiple Kueue-managed children).  However, this didn't work because Composable really meant Pod... having that be clear in the code would have saved us time (and should save time in the future for people in similar circumstances looking to implement an integration for their own custom CRD).

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-07-10T18:45:48Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-08-09T19:39:02Z

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

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-09-01T12:23:08Z

/remove-lifecycle rotten

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-11-30T12:41:26Z

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

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-12-01T09:35:54Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-03-01T09:46:39Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-03-02T05:24:13Z

/remove-lifecycle stale
