# Issue #2747: Remove deprecated ProvisioningRequest annotations

**Summary**: Remove deprecated ProvisioningRequest annotations

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2747

**Last updated**: 2025-08-04T08:37:40Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2024-08-01T15:47:04Z
- **Updated**: 2025-08-04T08:37:40Z
- **Closed**: 2025-08-04T08:37:40Z
- **Labels**: `kind/cleanup`, `priority/important-longterm`
- **Assignees**: [@kannon92](https://github.com/kannon92)
- **Comments**: 16

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:
Since [this PR](https://github.com/kubernetes-sigs/kueue/pull/2726), we started supporting the new ProvisioningRequest annotations, but we did not remove deprecated annotations so that we can maintain backward compatibility with the previous ClusterAutoscaler versions.

So, based on the Kubernetes deprecation policy, as we discussed [here](https://github.com/kubernetes-sigs/kueue/pull/2726#discussion_r1697928601), we would like to stop using deprecated ProvisioningRequest annotations here:

https://github.com/kubernetes-sigs/kueue/blob/e34732589c27f1d82f4e90c0d15c59ebb5f05e28/pkg/controller/admissionchecks/provisioning/constants.go#L22-L23

**Why is this needed**:
Deprecated annotations will be removed in the future ClusterAutocaler version.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-08-01T15:48:15Z

cc: @PBundyra @yaroslava-serdiuk

### Comment by [@kannon92](https://github.com/kannon92) — 2024-08-01T21:52:48Z

/assign

Have https://github.com/kubernetes-sigs/kueue/pull/2753 up.

### Comment by [@kannon92](https://github.com/kannon92) — 2024-08-02T12:03:11Z

/priority important-long term

Deprecation should once 1.29 is out of support.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-08-02T12:03:14Z

@kannon92: The label(s) `priority/important-long, priority/term` cannot be applied, because the repository doesn't have them.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/2747#issuecomment-2265208732):

>/priority important-long term
>
>Deprecation should once 1.29 is out of support.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@kannon92](https://github.com/kannon92) — 2024-08-02T12:05:12Z

/priority important-longterm

### Comment by [@mimowo](https://github.com/mimowo) — 2024-08-02T12:32:18Z

IIUC https://github.com/kubernetes-sigs/kueue/pull/2753#issuecomment-2264632961, we should wait until 1.30.1 is EOL. 
This will take something like a year.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-08-05T16:44:10Z

> IIUC [#2753 (comment)](https://github.com/kubernetes-sigs/kueue/pull/2753#issuecomment-2264632961), we should wait until 1.30.1 is EOL. This will take something like a year.

I think so too.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-11-03T17:28:57Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-11-04T06:23:08Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-02-02T06:41:05Z

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

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-02-02T08:23:46Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-05-03T08:54:49Z

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

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-05-05T08:55:29Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-08-03T08:55:35Z

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

### Comment by [@kannon92](https://github.com/kannon92) — 2025-08-03T13:33:40Z

/remove-lifecycle stale

### Comment by [@kannon92](https://github.com/kannon92) — 2025-08-03T13:34:09Z

This is probably actionable now.

Opened https://github.com/kubernetes-sigs/kueue/pull/6381
