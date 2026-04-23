# Issue #2198: Reformat all imports using gci linter

**Summary**: Reformat all imports using gci linter

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2198

**Last updated**: 2024-09-30T07:10:04Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alexandear](https://github.com/alexandear)
- **Created**: 2024-05-14T18:25:53Z
- **Updated**: 2024-09-30T07:10:04Z
- **Closed**: 2024-09-30T07:10:04Z
- **Labels**: `lifecycle/stale`, `kind/cleanup`
- **Assignees**: _none_
- **Comments**: 8

## Description

**What would you like to be cleaned**:

Reformat all imports using [`gci`](https://golangci-lint.run/usage/linters/#gci) linter once the issue daixiang0/gci#135 is resolved.

Disable `goimports` because `gci` does the same work.

**Why is this needed**:

`gci` ensures consistency of the import order.

See discussions in #2069 and #2184.

## Discussion

### Comment by [@trasc](https://github.com/trasc) — 2024-05-14T19:52:02Z

Maybe I'm missing something, why do we need this `gci` ?

### Comment by [@alexandear](https://github.com/alexandear) — 2024-05-15T14:41:47Z

We need `gci` because it was introduced by PR #2069.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-06-25T20:34:14Z

If the PR merged, doesn't it mean that we have no violations?

### Comment by [@alexandear](https://github.com/alexandear) — 2024-06-27T09:02:03Z

> If the PR merged, doesn't it mean that we have no violations?

The PR #2069 didn't enable `gci` due to incorrect configuration, but the author and reviewers thought it was enabled. See the description in #2184 for a detailed explanation.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-06-27T13:29:44Z

gotcha, so we can't re-enable `gci` just yet.

OTOH, we don't really use kube-builder scaffolding.

How reliable is this `gci` linter? The fact that it belongs to a person's github instead of an organization seems a bit worrisome.

### Comment by [@alexandear](https://github.com/alexandear) — 2024-06-27T13:56:54Z

`gci` has been included in golangci-lint since [v1.30.0](https://github.com/golangci/golangci-lint/blob/a62f1f13aa0a2b355ddd4a94448f22cbe6c0534c/pkg/lint/lintersdb/builder_linter.go#L309-L310), so it's quite stable.

But let's ask the author of the original PR who wants to enable `gci`. @vladikkuzn, is it worth replacing `goimports` with `gci`?

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2024-06-30T22:22:33Z

My opinion is that if it's stable with comments (which is the issue I didn't caught unfortunately) and it won't cause any further problems, then yes. It would make imports ordered the way everybody orders them, but automatically

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-09-28T22:50:24Z

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
