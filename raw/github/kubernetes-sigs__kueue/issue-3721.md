# Issue #3721: Resource flavor tolerations are not considered during scheduling

**Summary**: Resource flavor tolerations are not considered during scheduling

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3721

**Last updated**: 2024-12-03T14:23:01Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-12-03T13:27:34Z
- **Updated**: 2024-12-03T14:23:01Z
- **Closed**: 2024-12-03T14:23:01Z
- **Labels**: `kind/bug`
- **Assignees**: [@PBundyra](https://github.com/PBundyra)
- **Comments**: 1

## Description


**What happened**:

Resource flavor tolerations (in spec.tolerations) are not considered for scheduling in the flavor assigner -
only the tolerations which are already on the pod are considered (see [here](https://github.com/kubernetes-sigs/kueue/blob/86e8b0ba49f2ba5a50b90eb5e1f9c929c113eb6f/pkg/cache/tas_flavor_snapshot.go#L387-L389)).

As a consequence a workload which does not have the necessary tolerations is not scheduled against tainted nodes, even thought the RF would add the tolerations later on.

**What you expected to happen**:

The workload is admitted if the RF contains tolerations in spec.tolerations matching the nodeTaints.

**How to reproduce it (as minimally and precisely as possible)**:

Create a RF with the following structure:

```yaml
apiVersion: kueue.x-k8s.io/v1beta1
kind: ResourceFlavor
metadata:
  name: "default-flavor"
spec:
  nodeTaints:
  - key: key 
    value: value
    effect: NoExecute
  tolerations:
  - key: key 
    value: value
    effect: NoExecute
    operator: Equal
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: "cluster-queue"
spec:
  preemption:
    withinClusterQueue: LowerPriority
  namespaceSelector: {} # match all.
  resourceGroups:
  - coveredResources: ["cpu", "memory"]
    flavors:
    - name: "default-flavor"
      resources:
      - name: "cpu"
        nominalQuota: 9
      - name: "memory"
        nominalQuota: 36Gi
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: LocalQueue
metadata:
  namespace: "default"
  name: "user-queue"
spec:
  clusterQueue: "cluster-queue"
```
Then create the workload:
```yaml
apiVersion: batch/v1
kind: Job 
metadata:
  generateName: sample-job-
  namespace: default
  labels:
    kueue.x-k8s.io/queue-name: user-queue
spec:
  parallelism: 3
  completions: 3
  completionMode: Indexed
  suspend: true
  template:
    spec:
      containers:
      - name: dummy-job
        image: gcr.io/k8s-staging-perf-tests/sleep:v0.1.0
        args: ["300s"]
        resources:
          requests:
            cpu: "1" 
            memory: "200Mi"
      restartPolicy: Never
```
Issue: the workload does not get scheduled, even though the tolerations would be appended later on admission.

**Anything else we need to know?**:

This is a sibling issue to https://github.com/kubernetes-sigs/kueue/issues/3720

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-03T13:27:56Z

/assign @PBundyra 
/cc @tenzen-y @mwysokin
