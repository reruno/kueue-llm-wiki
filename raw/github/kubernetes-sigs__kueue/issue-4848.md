# Issue #4848: Handling of resources not defined in the list of coveredResource

**Summary**: Handling of resources not defined in the list of coveredResource

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4848

**Last updated**: 2025-04-01T09:11:03Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@atosatto](https://github.com/atosatto)
- **Created**: 2025-03-31T22:22:15Z
- **Updated**: 2025-04-01T09:11:03Z
- **Closed**: 2025-04-01T09:11:02Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 1

## Description

**What would you like to be added**:

Kueue is currently failing to admit workloads to a ClusterQueue in case one or more resources defined by the workload are not set in the list of the coveredResource in the ClusterQueue spec

```console
Warning  Pending  15s (x5 over 2m3s)   kueue-admission  couldn't assign flavors to pod set main: resource ephemeral-storage unavailable in ClusterQueue
```

However let's assume the following use-case where LimitRanges are used to ensure each Pod created agains the Kubernetes platform has some `ephemeral-storage` resources set (and some upper bounds) while no `ResourceQuota` is actually enforced at admission for ephemeral-storage at the Namespace level

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: kueue-example
---
apiVersion: v1
kind: ResourceQuota
metadata:
  name: p1
  namespace: kueue-example
spec:
  hard:
    limits.cpu: "1200m"
    limits.memory: 1200Mi
    requests.cpu: "1200m"
    requests.memory: 1200Mi
  scopeSelector:
    matchExpressions:
    - operator: In
      scopeName: PriorityClass
      values:
      - p1
---
apiVersion: v1
kind: LimitRange
metadata:
  name: default
  namespace: kueue-example
spec:
  limits:
  - default:
      cpu: 100m
      ephemeral-storage: 100Mi
      memory: 128Mi
    defaultRequest:
      cpu: 100m
      ephemeral-storage: 100Mi
      memory: 128Mi
    type: Container
  - max:
      ephemeral-storage: 10Gi
    type: Pod
```

When submitting the workload, if Kueue is not deployed in the cluster the workload is going to start regularly with the ephemeral-storage requests and limits being used to protect the host and eventually trigger Node-level eviction.

When modelling the same concept via Kueue

```yaml
apiVersion: kueue.x-k8s.io/v1beta1
kind: ResourceFlavor
metadata:
  name: "default-flavor"
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: "kueue-example"
spec:
  cohort: "kueue-example"
  resourceGroups:
  - coveredResources: ["cpu", "memory"]
    flavors:
    - name: "default-flavor"
      resources:
      - name: "cpu"
        nominalQuota: "0m"
        borrowingLimit: "1200m"
      - name: "memory"
        nominalQuota: 0Mi
        borrowingLimit: 1200Mi
  preemption:
    reclaimWithinCohort: Any
    borrowWithinCohort:
      policy: LowerPriority
      maxPriorityThreshold: 100000
    withinClusterQueue: LowerPriority
  namespaceSelector:
    matchExpressions:
    - key: kubernetes.io/metadata.name
      operator: In
      values: [ "kueue-example" ]
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: LocalQueue
metadata:
  name: "default"
  namespace: "kueue-example"
spec:
  clusterQueue: "kueue-example"
```

whenever a workload is submitted agains the default `LocalQueue` Kueue will refuse to admit if even if the `epheral-storage` resource is explicitly not included in the list of `coveredResources

```console
$ k -n kueue-example get workload job-new-job-d988d -o yaml | yq .status
conditions:
  - lastTransitionTime: "2025-03-31T21:34:34Z"
    message: 'couldn''t assign flavors to pod set main: resource ephemeral-storage unavailable in ClusterQueue'
    observedGeneration: 1
    reason: Pending
    status: "False"
    type: QuotaReserved
resourceRequests:
  - name: main
    resources:
      cpu: 100m
      ephemeral-storage: 100Mi
      memory: 100Mi
```

What we would like instead is for the workload to be admitted as this resource is not managed by the `ClusterQueue` retaining a similar behaviour to `ResourceQuota`.

**Why is this needed**:

There should be a way for Users to skip quota enforcement for certain resources (such as `resource-quota`) at scheduling time, in line with the current `ResourceQuota` behaviour without requiring them to start managing quota for these via the `ClusterQueue` resource groups.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@atosatto](https://github.com/atosatto) — 2025-04-01T09:11:02Z

Just closing this since I've noticed that adding `ephemeral-storage` to the list of [`excludeResourcePrefixes`](https://kueue.sigs.k8s.io/docs/reference/kueue-config.v1beta1/#Resources) in the Kueue configuration produces the intended behaviour.
