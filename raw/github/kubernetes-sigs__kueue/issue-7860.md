# Issue #7860: v1beta2: add ClusterProfile to v1beta1 becaue it is not persisted

**Summary**: v1beta2: add ClusterProfile to v1beta1 becaue it is not persisted

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7860

**Last updated**: 2025-11-25T00:48:37Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-11-24T18:56:42Z
- **Updated**: 2025-11-25T00:48:37Z
- **Closed**: 2025-11-25T00:48:37Z
- **Labels**: `kind/bug`
- **Assignees**: [@hdp617](https://github.com/hdp617)
- **Comments**: 4

## Description



**What happened**:

MultiKueueCluster does not currently support ClusterProfile after the recent changes, because we dropped it from v1beta1 which is used as storage: https://github.com/kubernetes-sigs/kueue/blob/930a474e8a7d4c2bcc80b2f424b8f5aa3f1cdb58/apis/kueue/v1beta1/multikueue_types.go#L61-L64

**What you expected to happen**:

ClusterProfile is not lost

**How to reproduce it (as minimally and precisely as possible)**:

Create 
```yaml
apiVersion: kueue.x-k8s.io/v1beta2
kind: MultiKueueCluster
metadata:
  name: multikueue-test-worker1
spec:
  kubeConfig:
    locationType: Secret
    location: worker1-secret
```
it results in  (spec dropped)
```yaml
apiVersion: v1
items:
- apiVersion: kueue.x-k8s.io/v1beta2
  kind: MultiKueueCluster
  metadata:
    creationTimestamp: "2025-11-24T18:24:10Z"
    generation: 1
    name: multikueue-test-worker1
    resourceVersion: "1764008650133327022"
    uid: 5fe176f7-d860-468c-88d6-9266644438cf
  status:
    conditions:
    - lastTransitionTime: "2025-11-24T18:24:10Z"
      message: 'load client config failed: kubeconfig reference is nil'
      observedGeneration: 1
      reason: BadKubeConfig
      status: "False"
      type: Active
kind: List
metadata:
  resourceVersion: ""
```

**Anything else we need to know?**:

This is in RC1. I will prepare RC2 once fixed.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-24T18:57:27Z

cc @hdp617 @mszadkow ptal

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-24T18:57:41Z

cc @tenzen-y

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-24T18:58:21Z

I think while it is ok to reorganize v1beta2 we still need to add the ClusterProfileRef to v1beta1 as a ptr, so that it can be stored, and not dropped.

### Comment by [@hdp617](https://github.com/hdp617) — 2025-11-24T19:19:35Z

/assign @hdp617
