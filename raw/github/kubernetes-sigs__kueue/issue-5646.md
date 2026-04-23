# Issue #5646: Consider moving the global configuration from ConfigMap to a singleton CRD

**Summary**: Consider moving the global configuration from ConfigMap to a singleton CRD

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5646

**Last updated**: 2026-04-02T17:44:17Z

---

## Metadata

- **State**: open (reopened)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-06-13T16:45:09Z
- **Updated**: 2026-04-02T17:44:17Z
- **Closed**: —
- **Labels**: `kind/feature`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 13

## Description

**What would you like to be added**:

Move the configuration from the configMap to a singleton CRD.

**Why is this needed**:

To improve admin experience for upgrading Kueue. Currently the configmap is a big text blob, so when an admin makes manual changes to the configuration, then they get overwritten by the new configuration provided by Kueue. If this was a CRD the changes affecting different names would merge using `kubectl apply --server-side`.

It would also allow us to write defaulting and validating rules using kubebuilder directives rather than code as currently.

**Completion requirements**:

I think this work requires a KEP due to its hidden complexity and potentially breaking changes. In particular, the KEP should
- research what other controllers do, what are the pros and cons of moving to CRD from the perspective of projects which completed the migration process.
- design the migration process from the currently used ConfigMap to CRD (likely following other projects which went this path)

Quick check this path was chosen by some k8s projects, such as:
- MetalLB, see [issue](https://github.com/metallb/metallb/issues/196), which even provides some tooling for it which we could consider using https://metallb.universe.tf/configuration/migration_to_crds/
- Argo CD, see [issue](https://github.com/argoproj/argo-cd/issues/5436)
We may also learn on Istio, cert-manager, or Linkerd which seem to follow the configuration pattern

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-13T16:46:35Z

For consideration
cc @tenzen-y @mwielgus @mwysokin @dgrove-oss @kannon92 @alaypatel07

### Comment by [@kannon92](https://github.com/kannon92) — 2025-06-13T16:54:09Z

We have done this for our openshift kueue operator work actually. 

https://github.com/openshift/kueue-operator/blob/release-1.0/pkg/apis/kueueoperator/v1/types.go.

Though I would ask if we should consider an operator..

cc @sohankunkerkar @MaysaMacedo

### Comment by [@kannon92](https://github.com/kannon92) — 2025-06-13T17:15:55Z

This has a really subtle problem though where the config is needed to start the kueue controller manager to start processing the CRD.

config map contains information to start the controllers.

I think if the config map could be VAP or MAP than it would be possible to create this without having the kueue-controller-manager but not sure how complicated the defaulting logic gets.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-09-11T17:52:36Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-10-11T18:38:43Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-11-10T19:19:07Z

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

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-11-10T19:19:14Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/5646#issuecomment-3513510670):

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-11-10T19:33:08Z

/reopen

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-11-10T19:33:14Z

@tenzen-y: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/5646#issuecomment-3513554437):

>/reopen
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@kannon92](https://github.com/kannon92) — 2025-12-03T16:56:42Z

/remove-lifecycle rotten

### Comment by [@kannon92](https://github.com/kannon92) — 2025-12-03T16:56:48Z

cc @rphillips

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-03-03T17:17:38Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-04-02T17:44:13Z

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
