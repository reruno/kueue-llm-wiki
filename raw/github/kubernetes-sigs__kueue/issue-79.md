# Issue #79: Support for hierarchical ClusterQueues

**Summary**: Support for hierarchical ClusterQueues

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/79

**Last updated**: 2024-09-20T16:22:06Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@ahg-g](https://github.com/ahg-g)
- **Created**: 2022-02-26T21:14:09Z
- **Updated**: 2024-09-20T16:22:06Z
- **Closed**: 2024-09-20T16:22:04Z
- **Labels**: `kind/feature`, `priority/backlog`, `lifecycle/frozen`, `kind/grand-feature`
- **Assignees**: [@mwielgus](https://github.com/mwielgus), [@gabesaba](https://github.com/gabesaba)
- **Comments**: 7

## Description

Systems like Yarn allow creating a hierarchy of fair sharing, which allows modeling deeper organizational structures with fair-sharing. 

Kueue currently supports three organizational levels: Cohort (models a business unit), ClusterQueue (models divisions within a business unit), namespace (models teams within a division). However fair-sharing is only supported at one level, within a cohort.

We opted-out of supporting hierarchy from the beginning for two reasons: (1) it adds complexity to both the API and implementation; (2) it is also not clear that in practice customers need more than two levels of sharing which is what the current model enables and seems to work for other frameworks like Slurm and HTCondor.

As Kueue evolves we likely need to revisit this decision.

## Discussion

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-04-13T02:16:14Z

/kind grand-feature

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2022-07-12T14:23:11Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues and PRs.

This bot triages issues and PRs according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue or PR as fresh with `/remove-lifecycle stale`
- Mark this issue or PR as rotten with `/lifecycle rotten`
- Close this issue or PR with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-07-12T14:33:45Z

/lifecycle frozen

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-01-02T19:41:13Z

/assign @mwielgus

### Comment by [@gabesaba](https://github.com/gabesaba) — 2024-06-19T13:17:12Z

/assign

### Comment by [@gabesaba](https://github.com/gabesaba) — 2024-09-20T16:22:00Z

/close

Hierarchical Cohorts will be available as part of the 0.9 release.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-09-20T16:22:04Z

@gabesaba: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/79#issuecomment-2364086879):

>/close
>
>Hierarchical Cohorts will be available as part of the 0.9 release.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
