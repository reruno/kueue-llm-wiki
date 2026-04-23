# Issue #7032: Separate out the API as its own go module

**Summary**: Separate out the API as its own go module

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7032

**Last updated**: 2026-02-28T15:11:45Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@unmarshall](https://github.com/unmarshall)
- **Created**: 2025-09-29T05:14:55Z
- **Updated**: 2026-02-28T15:11:45Z
- **Closed**: 2026-02-28T15:11:44Z
- **Labels**: `kind/feature`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 9

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

* Separate out apis into its own go module. 
* Remove dependency on `component-base` as it brings in a LOT of dependencies along with it which we do not want to include as well.

**Why is this needed**:

Currently API is not a separate go module. We wanted to leverage only [TopologyLevel](https://github.com/kubernetes-sigs/kueue/blob/c171b5276c379e80bf22915ddeea6cdf9102c5bb/apis/kueue/v1beta1/topology_types.go#L110) API and do not wish to bring in the entire dependency graph of kueue into our project.

The intent is to make the API go module absolutely lean allowing for programmatic integration without the cost of its implementation dependencies.

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2025-09-30T22:03:54Z

To be honest, this sounds like overkill for Kueue.

The topology API is not standardized across cloud providers so I worry about Kueue supporting this as an API for downstream projects.

cc @mimowo @tenzen-y @gabesaba

### Comment by [@kannon92](https://github.com/kannon92) — 2025-09-30T23:09:58Z

Though on second thought as we aim to move API to v1 should we consider moving the API to its own repo?

I believe our goal is to make it more official with kube api reviews.

### Comment by [@unmarshall](https://github.com/unmarshall) — 2025-10-01T03:31:39Z

@kannon92 thanks for responding back. In its current shape and form `TopologyLevel` API (what we are interested in) is quite generic and is no way trying to define any levels on its own. The consumers of this API can define their levels. Therefore the API is not held ransom because there is no consistency or agreed upon common labels across providers.

Of course this is not the only API that Kueue defines. In general multi-module go projects are a norm and quite easy now and makes consumption lean. You should also think of dependency on`component-base` as it is becoming a dumping group for all things common and thus has a tendency to have a larger dependency graph.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-01T13:07:24Z

I see this being useful, and I think I'm open to decoupling, similarly as CA does. 

However, it might be extra effort that we need to include in prioritization. I'm wondering if there are community members willing to drive it.

cc @mwysokin @mwielgus

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-10-01T13:12:03Z

I'm open to this as well. But, this must contain the release associated automation mechanism.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-12-30T13:15:50Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-01-29T14:16:04Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-02-28T15:11:39Z

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

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-02-28T15:11:45Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/7032#issuecomment-3977290791):

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
