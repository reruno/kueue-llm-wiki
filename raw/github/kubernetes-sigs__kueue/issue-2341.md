# Issue #2341: Support MultiKueue for Plain Pod Integration

**Summary**: Support MultiKueue for Plain Pod Integration

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2341

**Last updated**: 2025-02-19T12:10:28Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2024-06-03T04:59:49Z
- **Updated**: 2025-02-19T12:10:28Z
- **Closed**: 2025-02-19T12:10:28Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 11

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
I'd like to support the MultiKueue for the plain pod the same as the Job and JobSet.

**Why is this needed**:
In general multi tenant clusters not for ML/HPC, we deploy applications (~=Deplyment/Knative Service) and jobs such for DB batch processing into mixed multiple clusters. In such clusters, I'd like to manage quotas in all workloads by the Kueue.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-06-03T11:42:39Z

There was also some interest and initial discussion on [wg-batch Slack](https://kubernetes.slack.com/archives/C032ZE66A2X/p1716561964644989)

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-06-03T14:40:47Z

> There was also some interest and initial discussion on [wg-batch Slack](https://kubernetes.slack.com/archives/C032ZE66A2X/p1716561964644989)

Thank you for pointing this out! Let me check it.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-09-01T15:26:28Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-09-02T18:59:52Z

/remove-lifecycle stale

### Comment by [@rochaporto](https://github.com/rochaporto) — 2024-11-13T14:28:13Z

Adding our interest in this as well.

Two examples:
* We're integrating ContainerSSH with Kueue/MultiKueue (https://github.com/ContainerSSH/ContainerSSH) to offer an ssh service on top of kubernetes. It relies on plain Pods.
* The GitLab CI Kubernetes executor also uses Pods for the execution (https://docs.gitlab.com/runner/executors/kubernetes/)

It could be they can be changed to rely on Jobs as well - but if Pod support is added they would work out of the box.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-02-11T14:58:08Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-11T15:43:53Z

/remove-lifecycle stale

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-11T15:44:46Z

Actually the baseline support is already done in 0.11 by https://github.com/kubernetes-sigs/kueue/pull/4034

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-13T08:51:04Z

Before we close the issue, I would like to add some documentation in https://kueue.sigs.k8s.io/docs/tasks/run/multikueue/. Also, showing how to use it in the context of Deployments. 
cc @Bobbins228 @mszadkow are you up to?

### Comment by [@Bobbins228](https://github.com/Bobbins228) — 2025-02-13T09:20:33Z

Sure thing @mimowo I can get working on it tomorrow 👍

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-13T09:21:58Z

> Sure thing [@mimowo](https://github.com/mimowo) I can get working on it tomorrow 👍

Thank you!
