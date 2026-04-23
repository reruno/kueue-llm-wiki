# Issue #6383: [Dashboard] Use kueue go bindings rather than dynamic client

**Summary**: [Dashboard] Use kueue go bindings rather than dynamic client

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6383

**Last updated**: 2025-12-10T10:37:31Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kannon92](https://github.com/kannon92)
- **Created**: 2025-08-03T17:51:36Z
- **Updated**: 2025-12-10T10:37:31Z
- **Closed**: 2025-12-10T10:37:31Z
- **Labels**: `kind/cleanup`, `lifecycle/rotten`, `area/dashboard`
- **Assignees**: _none_
- **Comments**: 6

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

Kueue publishes golang clients and we can use those versus dynamic client.

See [client-go](https://github.com/kubernetes-sigs/kueue/tree/main/client-go/clientset/versioned)

**Why is this needed**:

The backend golang code for Kueue Viz could have some bugs due to marshaling and not type checking.

It will also be easier to unit test the backend as we can use the fake client.

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2025-08-03T17:51:49Z

/area dashboard

### Comment by [@kannon92](https://github.com/kannon92) — 2025-08-03T17:53:11Z

ref: https://github.com/kubernetes-sigs/kueue/issues/5331

### Comment by [@samzong](https://github.com/samzong) — 2025-08-04T01:38:45Z

I know some issues with the current implementation, it seems we need to try to refactor kubeviz/backend?

### Comment by [@kannon92](https://github.com/kannon92) — 2025-08-04T02:03:40Z

I fixed https://github.com/kubernetes-sigs/kueue/pull/5330 which was related to bad typing.

If you know of other issues please file a bug.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-11-02T03:02:05Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-12-02T03:52:26Z

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
