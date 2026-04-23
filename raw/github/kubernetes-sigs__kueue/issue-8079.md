# Issue #8079: CornerCase: Kueue blocks scheduling of workloads if they request "0" or resource not present in CQ definition

**Summary**: CornerCase: Kueue blocks scheduling of workloads if they request "0" or resource not present in CQ definition

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8079

**Last updated**: 2026-01-26T11:41:11Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-12-04T16:27:08Z
- **Updated**: 2026-01-26T11:41:11Z
- **Closed**: 2026-01-26T11:41:11Z
- **Labels**: `kind/bug`
- **Assignees**: [@IrvingMg](https://github.com/IrvingMg)
- **Comments**: 5

## Description

**What happened**:

Kueue would not admit workloads which request "0" of a resource which is not defined in the ClusterQueue, for example

**What you expected to happen**:

Kueue would admit workloads which request "0" of some resource, even if not declared in CQ.

I expect that because the vanilla kubernetes schedules Pods which request 0 nvidia.com/gpu, even if Node does not provide GPU.

**How to reproduce it (as minimally and precisely as possible)**:

```yaml
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: "cluster-queue"
spec:
  namespaceSelector: {} # match all.
  resourceGroups:
  - coveredResources: ["memory"]
    flavors:
    - name: "default-flavor"
      resources:
      - name: "memory"
        nominalQuota: 36Gi
```
and Job 
```yaml
apiVersion: batch/v1
kind: Job
metadata:
  generateName: sample-job
  namespace: default
  labels:
    kueue.x-k8s.io/queue-name: user-queue
spec:
  parallelism: 3
  completions: 3
  completionMode: Indexed
  template:
    spec:
      containers:
      - name: dummy-job
        image: gcr.io/k8s-staging-perf-tests/sleep:v0.1.0
        args: ["10s"]
        resources:
          limits:
            "nvidia.com/gpu": 0
          requests:
            "nvidia.com/gpu": 0
            memory: "200Mi"
      restartPolicy: Never
```
Will fail workload scheduling with:

```yaml
  status:
    conditions:
    - lastTransitionTime: "2025-12-04T16:23:57Z"
      message: 'couldn''t assign flavors to pod set main: resource nvidia.com/gpu
        unavailable in ClusterQueue'
      observedGeneration: 1
      reason: Pending
      status: "False"
      type: QuotaReserved
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-04T16:27:53Z

cc @tenzen-y @kannon92  as I may lack context if this is a bug or a deliberate decision, but I think we should aim for compatibility with the kube-scheduler, wdyt?

### Comment by [@kannon92](https://github.com/kannon92) — 2025-12-05T00:40:54Z

This reminds me of https://github.com/kubernetes-sigs/kueue/issues/7513.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-12-05T00:41:57Z

0 value is weird but typically Kueue blocks on anything that isn't in CQ or excludeResourcePrefixes.

So if gpu is not present in excludeResourcePrefixes I expect this to fail scheduling due to that "feature".

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2025-12-15T08:38:19Z

/assign

### Comment by [@MaysaMacedo](https://github.com/MaysaMacedo) — 2025-12-19T11:25:50Z

@kannon92 @mimowo Is this issue tracking the same problem defined in [this other issue?](https://github.com/kubernetes-sigs/kueue/issues/7513)
