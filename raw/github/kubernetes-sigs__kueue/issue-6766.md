# Issue #6766: Do not update the RequeueAt field in ProvisioningRequest controller directly

**Summary**: Do not update the RequeueAt field in ProvisioningRequest controller directly

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6766

**Last updated**: 2026-04-08T17:03:45Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-09-09T09:17:15Z
- **Updated**: 2026-04-08T17:03:45Z
- **Closed**: 2026-04-08T17:03:44Z
- **Labels**: `kind/cleanup`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 9

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

I would like to use the mechanism proposed in https://github.com/kubernetes-sigs/kueue/pull/6210. So, the ProvisioningRequest controller instead of updateing the RequeueAt updates the AC speciifc RetryCount and requeueAfterSeconds.

**Why is this needed**:

The field requeueAt is overloaded with Kueue core controller updating it, and AC controllers. 

The KEP proposes a cleaner design we could use. 

Also, the count for the number of retries does not have a clear interpretation as it is bumped both for WaitForPodsReady and ProvisioningRequest controller. So, it may happen that a workload is deactivated by hitting the waitForPodsReady.backoffLimit even though it actually hit the ProvisioningRequest issues. I think this could be considered a bug.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-09T09:18:19Z

cc @PBundyra @dhenkel92 - ticketing so that we remember about it. It would be nice to fix before going to v1, preferrably before v1beta2.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-09-09T11:01:51Z

I fully agree with this proposal.
TBH, I didn't imagine that ProvReq relies on the requeueAt field when I designed the function.
Additionally, decoupling ProvReq semantic from requeueAt could resolve update conflicts.

### Comment by [@dhenkel92](https://github.com/dhenkel92) — 2025-09-09T12:52:55Z

I think it makes a lot of sense to migrate the ProvisioningRequest AC as soon as the new fields are available. Otherwise, they might get in each other’s way or behave unexpectedly.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-12-08T12:59:32Z

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

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-12-08T14:01:04Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-03-08T14:34:42Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-04-07T14:47:21Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-04-08T17:03:38Z

This was resolved as part of https://github.com/kubernetes-sigs/kueue/pull/7620.
/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-04-08T17:03:45Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/6766#issuecomment-4208016510):

>This was resolved as part of https://github.com/kubernetes-sigs/kueue/pull/7620.
>/close
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
