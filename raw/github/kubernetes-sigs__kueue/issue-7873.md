# Issue #7873: Cloud provider specific documentation

**Summary**: Cloud provider specific documentation

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7873

**Last updated**: 2026-04-18T09:13:56Z

---

## Metadata

- **State**: open
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-11-25T10:02:27Z
- **Updated**: 2026-04-18T09:13:56Z
- **Closed**: —
- **Labels**: `priority/important-soon`, `lifecycle/rotten`, `kind/documentation`, `area/multikueue`
- **Assignees**: _none_
- **Comments**: 4

## Description

/kind documentation

I would like to introduce some documentation which is cloud-specific. The need is pretty clear with the recent features like ClusterProfiles where the API is vendor agnostic, but to make it working we need to provide vendor specific configuration. Similarly the labels for TopologyAwareScheduling differ cloud-to-cloud, so it would be good to have some copy-paste working examples.

We would like to separate the vendor-specific documentation from the code documentation. 

We only allow to add vendor specific-documentation if the generic one already is added.

The directory structure under https://kueue.sigs.k8s.io/docs/ could be:

Vendor-specific:
- aws
  - MultiKueue with ClusterProfiles
  - Topology-AwareScheduling
- gke:
  - MultiKueue with ClusterProfiles
  - Topology-AwareScheduling
- open-shift:
  - MultiKueue with ClusterProfiles
  - Topology-AwareScheduling
  - ...

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-25T10:06:11Z

cc @tenzen-y  @mwielgus @kannon92  who may be interested in the structure of the docs
cc @hdp617 who is working on ClusterProfiles and could follow up with GKE specific bits as part of  https://github.com/kubernetes-sigs/kueue/issues/7764 once the structure is set

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T08:20:22Z

/area multikueue
/priority important-soon

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-03-19T08:44:20Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-04-18T09:13:52Z

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
