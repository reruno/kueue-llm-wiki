# Issue #3956: kueue-controller-manager not starting up

**Summary**: kueue-controller-manager not starting up

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3956

**Last updated**: 2025-06-09T15:25:20Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@kalki7](https://github.com/kalki7)
- **Created**: 2025-01-10T13:23:24Z
- **Updated**: 2025-06-09T15:25:20Z
- **Closed**: 2025-06-09T15:25:18Z
- **Labels**: `kind/bug`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 7

## Description

**What happened**: Kueue v0.10.0 had already been deployed and working as expected. Once I had enabled `enableClusterQueueResources: true` and redeployed the same version of kueue, the manager container in kueue-controller-manager was stuck in a CrashLoopBackoff with the following being the only logs we were able to retrieve

```
{
activity_type_name: "ViolationOpenEventv1"
policy_id: "6885206598817066570"
resource_name: "dev manager"
started_at: "1736511103"
terse_message: "Restart count for dev manager is above the threshold of 1.000 with a value of 2.000."
verbose_message: "Restart count for dev manager is above the threshold of 1.000 with a value of 2.000."
violation_id: "0.nng1d6n8dhxc"
}
```

```
{
activity_type_name: "ViolationAutoResolveEventv1"
policy_id: "6885206598817066570"
resolved_at: "1736511220"
resource_name: "dev manager"
terse_message: "Restart count for dev manager returned to normal with a value of 4.000."
verbose_message: "Restart count for dev manager returned to normal with a value of 4.000."
violation_id: "0.nng1d6n8dhxc"
}
```

```
{
activity_type_name: "ViolationOpenEventv1"
policy_id: "6885206598817066570"
resource_name: "dev manager"
started_at: "1736511257"
terse_message: "Restart count for dev manager is above the threshold of 1.000 with a value of 5.000."
verbose_message: "Restart count for dev manager is above the threshold of 1.000 with a value of 5.000."
violation_id: "0.nng1d6n8dhxc"
}
```

Followed by kube-rbac-proxy logging `received interrupt, shutting down`

**What you expected to happen**: kueue-controler-manager to start up

**How to reproduce it (as minimally and precisely as possible)**: Deploy kueue v0.10.0 using the manifest with `enableClusterQueueResources: true` enabled and kueue-controller-manager resource requests and limited increased to 8gb and 16gb for memory and 1 and 2 for cpu 

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`): 1.30.6-gke.1125000
- Kueue version (use `git describe --tags --dirty --always`): v.0.10.0
- Cloud provider or hardware configuration: GCP - Google Kubernetes Engine
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2025-01-10T13:28:23Z

Can you try and see if you get this problem on kind? 

I don't know what "dev manager" is so I worry this may be a GKE problem.

### Comment by [@kalki7](https://github.com/kalki7) — 2025-01-10T13:53:39Z

dev manager is the name of the GKE resource. However, I just disabled `enableClusterQueueResources` and it back to the previous working state. So I think it might have something to do with the `enableClusterQueueResources: true`. Where once its enabled, the manager container in the kueue-controller-manager deployment doesn't come up.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-01-10T13:59:02Z

cc @mimowo @mwielgus 

Anyone you can loop into this from the GKE side?

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-04-10T14:45:32Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-05-10T14:49:21Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-06-09T15:25:14Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues and PRs.

This bot triages issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Reopen this issue with `/reopen`
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/close not-planned

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-06-09T15:25:19Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3956#issuecomment-2956128148):

>The Kubernetes project currently lacks enough active contributors to adequately respond to all issues and PRs.
>
>This bot triages issues according to the following rules:
>- After 90d of inactivity, `lifecycle/stale` is applied
>- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
>- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed
>
>You can:
>- Reopen this issue with `/reopen`
>- Mark this issue as fresh with `/remove-lifecycle rotten`
>- Offer to help out with [Issue Triage][1]
>
>Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).
>
>/close not-planned
>
>[1]: https://www.kubernetes.dev/docs/guide/issue-triage/


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
