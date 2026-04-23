# Issue #3899: Finalizer patch on the pod may overwrite other changes to the finalizer

**Summary**: Finalizer patch on the pod may overwrite other changes to the finalizer

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3899

**Last updated**: 2026-01-30T10:33:45Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@troychiu](https://github.com/troychiu)
- **Created**: 2024-12-20T23:33:55Z
- **Updated**: 2026-01-30T10:33:45Z
- **Closed**: 2026-01-30T10:33:45Z
- **Labels**: `kind/bug`
- **Assignees**: [@mykysha](https://github.com/mykysha)
- **Comments**: 11

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
In our cluster, I noticed that a change to the pod's finalizer was reverted when Kueue attempted to remove its own finalizer. I found we are using non-strict mode patch https://github.com/kubernetes-sigs/kueue/blob/18874ed4af7cb6b591002baef0f10d737b2cacf6/pkg/controller/jobs/pod/pod_controller.go#L514, resulting in the race condition.

**What you expected to happen**:
Kueue should not overwrite other changes to the finalizer.

**How to reproduce it (as minimally and precisely as possible)**:
Create a pod with finalizers in addition to Kueue's finalizer. However, this issue doesn't always occur.

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-12-23T09:25:34Z

/assign @mykysha

### Comment by [@troychiu](https://github.com/troychiu) — 2024-12-23T17:38:22Z

I can create a PR for this

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-12T10:56:42Z

@troychiu as we are working on the fix it turns out it has some pros & cons. PTAL at the initial [PR](https://github.com/kubernetes-sigs/kueue/pull/3912), and the comment in particular: https://github.com/kubernetes-sigs/kueue/pull/3912#issuecomment-2717468503.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-06-10T11:01:16Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-10T11:08:31Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-09-08T11:29:52Z

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

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-09-29T11:40:37Z

/remove-lifecycle stale

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-29T12:06:24Z

@troychiu does it remain an issue for you? How do you workaround it in the meanwhile?

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-12-28T12:52:45Z

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

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-12-28T13:09:30Z

/remove-lifecycle stale

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-12-28T13:10:18Z

This issue addressed on https://github.com/kubernetes-sigs/kueue/pull/3912. 

@mimowo @tenzen-y could you please take a look?
