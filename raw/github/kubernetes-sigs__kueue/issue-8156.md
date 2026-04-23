# Issue #8156: MultiKueue: Support label selector in MultiKueueConfig

**Summary**: MultiKueue: Support label selector in MultiKueueConfig

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8156

**Last updated**: 2026-04-18T09:13:56Z

---

## Metadata

- **State**: open
- **Author**: [@hdp617](https://github.com/hdp617)
- **Created**: 2025-12-09T19:25:44Z
- **Updated**: 2026-04-18T09:13:56Z
- **Closed**: —
- **Labels**: `kind/feature`, `priority/important-longterm`, `lifecycle/rotten`, `area/multikueue`
- **Assignees**: _none_
- **Comments**: 5

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
Currently, MultiKueueConfig requires a list of clusters. 
```
apiVersion: kueue.x-k8s.io/v1beta2
kind: MultiKueueConfig
metadata:
  name: multikueue-test
spec:
  clusters:
  - multikueue-test-worker1
  - multikueue-test-worker2
```

When a new cluster is created or a cluster is deleted, user needs to manually update MultiKueueConfig. This can be addressed with supporting label selectors. Example of what the API could look like:
```
apiVersion: kueue.x-k8s.io/v1beta1
kind: MultiKueueConfig
metadata:
  name: multikueue-test
spec:
  affinity:
    clusterAffinity:
      requiredDuringSchedulingRequiredDuringExecution:
        clusterSelectorTerms:
        - matchExpressions:
          - labelSelector:
              key: environment
              operator: In
              values:
              - production
```


**Why is this needed**:
This feature will address worker cluster inventory management.

**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [x] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-10T07:24:14Z

I think managing clusters with label selector is a good idea, but the clusterAffinity API looks like too complex for the use-case. IIUC this is by analogy to nodeAffinity in Pod.

So I would rather start with something lightweight like `clusterSelector` which is just a map labelKey -> labelValue, by analogy to Pod's nodeSelector.

In Pod we have both `nodeSelector` and `nodeAffinity`, but `nodeSelector` is preferred for simple use case like this one. If we have complex use cases we can later add `clusterAffinity`, but I don't see this justified yet.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-10T08:52:37Z

Instead of referencing directly ClusterProfile instances it seems to make sense to use MultiKueueCluster as the proxy layer where additional configuration can be added. 

I understand the desire to improve UX, but maybe better idea is to do https://github.com/kubernetes-sigs/kueue/issues/7716, because I imagine some users may want to use label selectors and use kubeconfigs via secrets instead of the ClusterProfiles.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T08:19:19Z

/area multikueue
/priority important-longterm

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-03-19T08:44:19Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-04-18T09:13:53Z

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
