# Issue #1439: ClusterQueue namespace selector docs is not clear

**Summary**: ClusterQueue namespace selector docs is not clear

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1439

**Last updated**: 2024-05-07T01:42:06Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@moficodes](https://github.com/moficodes)
- **Created**: 2023-12-11T22:35:34Z
- **Updated**: 2024-05-07T01:42:06Z
- **Closed**: 2024-05-07T01:42:06Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 3

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Example / Clarification on how to select on specific namespace either using `matchLabel` or `matchExpressions` for `ClusterQueue`.

**Why is this needed**:

From the docs its not clear how users can target a specific namespace in clusterqueue.

**Completion requirements**:

Examples of targeting a specific namespace or a list of namespace in the clusterqueue docs.

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

@alizaidis

## Discussion

### Comment by [@alizaidis](https://github.com/alizaidis) — 2023-12-11T22:38:15Z

Example for matchLabels:

```
namespaceSelector:
    matchLabels:
      kubernetes.io/metadata.name: team-a
```

Example for matchExpressions:

```
matchExpressions:
    - key: kubernetes.io/metadata.name
      operator: In
      values:
      - team-a
      - team-b
      - team-c
```

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-03-10T23:10:57Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-03-10T23:12:34Z

/remove-lifecycle stale
