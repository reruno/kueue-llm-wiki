# Issue #486: Add pprof endpoint

**Summary**: Add pprof endpoint

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/486

**Last updated**: 2023-07-13T16:58:40Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2022-12-21T16:56:27Z
- **Updated**: 2023-07-13T16:58:40Z
- **Closed**: 2023-07-13T16:58:40Z
- **Labels**: `kind/feature`
- **Assignees**: [@stuton](https://github.com/stuton)
- **Comments**: 8

## Description

**What would you like to be added**:

Add an endpoint that allows to capture a profile.

Core Kuberentes components have this:
https://github.com/kubernetes/kubernetes/blob/407bd6a4afa5f7d7cb2a596dda09cacc30828f09/cmd/kube-scheduler/app/server.go#L282

Not sure if there is a way to do this via controller runtime https://github.com/kubernetes-sigs/controller-runtime/issues/1779

**Why is this needed**:

To inform performance improvements

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-12-21T20:37:05Z

There is WIP https://github.com/kubernetes-sigs/controller-runtime/pull/1943

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2023-03-21T21:25:06Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-03-22T05:28:10Z

/remove-lifecycle stale

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-04-12T19:43:42Z

The next release of controller-runtime should include this https://github.com/kubernetes-sigs/controller-runtime/pull/1943

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2023-07-11T20:40:48Z

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

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-07-12T12:09:53Z

/remove-lifecycle stale

### Comment by [@trasc](https://github.com/trasc) — 2023-07-12T12:22:26Z

It should be doable with kubernetes-sigs/controller-runtime#1779 , we just need to add support for this in the config.

### Comment by [@stuton](https://github.com/stuton) — 2023-07-12T12:55:53Z

/assign
