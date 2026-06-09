# Issue #9183: Bump python from 3.12-slim to 3.14-slim in /hack/testing/ray

**Summary**: Bump python from 3.12-slim to 3.14-slim in /hack/testing/ray

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9183

**Last updated**: 2026-06-08T15:44:05Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-02-12T17:10:23Z
- **Updated**: 2026-06-08T15:44:05Z
- **Closed**: 2026-06-08T15:44:05Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@vladikkuzn](https://github.com/vladikkuzn)
- **Comments**: 8

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

To unblock upgrade by dependabot: https://github.com/kubernetes-sigs/kueue/pull/9148

**Why is this needed**:

To enable future upgrades by dependabot

## Discussion

### Comment by [@skools-here](https://github.com/skools-here) — 2026-02-16T17:47:02Z

/unassign

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2026-02-20T14:23:59Z

/assign

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2026-03-03T05:12:07Z

There's still no support in https://github.com/ray-project/ray

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-03T05:17:05Z

There is no support for what? Is it maybe already present on the main btanch, and we are waiting for release? 

If there is some library the kuberay needs to buno then please open an issue in KubeRay and work with the maintainers of the project. cc @vladikkuzn @mbobrovskyi

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2026-03-03T05:51:28Z

Python lib ray (which is built upon) currently supports all versions up to python 3.13, we must wait until they release it [here](https://pypi.org/project/ray/#files) for cPython314 interpreter. Kuberay already supports latest version of ray though, so I think we can bump to 3.13-slim

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2026-03-03T05:53:51Z

Here's the issue: https://github.com/ray-project/ray/issues/56434
They are actively working on it

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-06-01T06:49:47Z

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

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2026-06-05T21:27:12Z

/remove-lifecycle stale
