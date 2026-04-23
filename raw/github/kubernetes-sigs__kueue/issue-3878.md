# Issue #3878: Documentation page on using Kueue to run Notebook

**Summary**: Documentation page on using Kueue to run Notebook

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3878

**Last updated**: 2026-04-07T18:47:25Z

---

## Metadata

- **State**: open
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-12-18T06:17:43Z
- **Updated**: 2026-04-07T18:47:25Z
- **Closed**: —
- **Labels**: `lifecycle/rotten`, `kind/documentation`
- **Assignees**: _none_
- **Comments**: 13

## Description

**What would you like to be added**:

A documentation page under https://kueue.sigs.k8s.io/docs/tasks/run/ showing how to use Kueue to run Kubeflow Notebook.

Then we should also update the main README and reference the page from the "Features overview / Integrations" point.

This is a follow up to https://github.com/kubernetes-sigs/kueue/issues/3352

**Why is this needed**:

To showcase Kueue is supporting the running of Notebook. To guide users how to do it.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-18T06:19:18Z

cc @xiongzubiao  @varshaprasad96 @tenzen-y

### Comment by [@varshaprasad96](https://github.com/varshaprasad96) — 2025-01-29T20:51:21Z

Since the "kueue. x-k8s. io/ queue-name" label is not being added by the notebook-controller to STS, the notebook integration is not working out of the box.

Just tested it out, and looks like a small update in NB controller is needed.

I'll create a PR with NB controller to add NB CR labels to SS, and once it is done can create a doc PR in here.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-30T06:30:48Z

Awesome, thanks!

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-05T13:32:06Z

/kind documentation
/remove-kind feature

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-05-06T14:19:17Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-07T15:03:53Z

/remove-lifecycle stale

### Comment by [@kannon92](https://github.com/kannon92) — 2025-08-03T17:57:05Z

This is still relevant.

### Comment by [@jrleslie](https://github.com/jrleslie) — 2025-09-09T16:15:06Z

hi @varshaprasad96 @kannon92 - we're interested in the notebooks integration, but trying to understand where it stands. Does this integration work today or does the https://github.com/kubeflow/kubeflow/pull/7674 PR still need to be merged?

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-12-08T17:03:31Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-08T17:08:41Z

/remove-lifecycle stale

### Comment by [@kannon92](https://github.com/kannon92) — 2025-12-08T17:46:15Z

> hi [@varshaprasad96](https://github.com/varshaprasad96) [@kannon92](https://github.com/kannon92) - we're interested in the notebooks integration, but trying to understand where it stands. Does this integration work today or does the [kubeflow/kubeflow#7674](https://github.com/kubeflow/kubeflow/pull/7674) PR still need to be merged?

Sad. It seems that still needs to merge. I'll open that up.

Opened up https://github.com/kubeflow/notebooks/pull/788.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-03-08T18:38:43Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-04-07T18:47:21Z

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
