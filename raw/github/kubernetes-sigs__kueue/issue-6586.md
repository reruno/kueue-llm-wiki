# Issue #6586: ResourceFlavor quota usage tracking in overlapping node scenarios

**Summary**: ResourceFlavor quota usage tracking in overlapping node scenarios

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6586

**Last updated**: 2026-04-11T16:41:51Z

---

## Metadata

- **State**: open
- **Author**: [@ichekrygin](https://github.com/ichekrygin)
- **Created**: 2025-08-14T18:01:22Z
- **Updated**: 2026-04-11T16:41:51Z
- **Closed**: —
- **Labels**: `priority/important-longterm`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 8

## Description

## Description

Kueue’s [ResourceFlavor (RF)](https://kueue.sigs.k8s.io/docs/concepts/resource_flavor/) is a construct that defines available compute resources in a cluster, and enables fine-grained resource management by associating workloads with specific node types.

The primary purpose of an RF is to represent available resources from cluster nodes, grouping them into resource profiles in heterogeneous environments. A given RF can represent a subset of total nodes in the cluster. This grouping **does not need to be mutually exclusive**, meaning the same node (and its resources) can belong to multiple ResourceFlavors.

In homogeneous environments, Kueue allows the definition of “empty” ResourceFlavors that map all available nodes to a given RF. It is possible to define multiple RFs with partially or fully overlapping node sets, for example, creating more than one empty RF.

## Quota Tracking Behavior

At a high level, an RF’s quota representation is similar to Kubernetes `ResourceQuota`,
However, there is a key difference in quota usage tracking:

* Both RF and `ResourceQuota` allow overlapping definitions (e.g., overlapping node sets),
* **Unlike** `ResourceQuota`, RF **does not** track quota usage in overlapping scenarios. This can lead to situations where the actual available capacity is overestimated when RFs share nodes.

### ResourceQuota Use-Case

Example: Create two overlapping `ResourceQuota` objects referencing the same resource (CPU):

```bash
kubectl create resourcequota red --hard=cpu=2
kubectl create resourcequota blue --hard=cpu=3
```

Check initial usage:

```text
NAME  AGE  HARD   USED   REMAINING
blue  5s   cpu=3  cpu=0  cpu=3
red   17s  cpu=2  cpu=0  cpu=2
```

Create a pod requesting 1 CPU:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: test-1
  labels:
    kueue.x-k8s.io/queue-name: demo
spec:
  containers:
    - name: sleep
      image: gcr.io/k8s-staging-perf-tests/sleep:v0.1.0
      args: ["600s"]
      resources:
        requests:
          cpu: "1"
  restartPolicy: OnFailure
```

Quota usage is updated in **both** quotas:

```text
NAME  HARD   USED   REMAINING
blue  cpu=3  cpu=1  cpu=2
red   cpu=2  cpu=1  cpu=1
```

After creating a second pod (1 CPU):

```text
NAME  HARD   USED   REMAINING
blue  cpu=3  cpu=2  cpu=1
red   cpu=2  cpu=2  cpu=0
```

A third pod is blocked because quota `red` is depleted:

```text
Error from server (Forbidden): exceeded quota: red, requested: cpu=1, used: cpu=2, limited: cpu=2
```

---

### ResourceFlavor Use-Case

Replicating a similar setup with ResourceFlavors:

```text
kubectl get rf
NAME                 AGE
default-flavor       10d
overlapping-flavor   66m
```

Both flavors match the same node labels:

```yaml
nodeLabels:
  kubernetes.io/os: linux
topologyName: default
```

ClusterQueue flavor usage before workloads:

```yaml
flavorsUsage:
- name: default-flavor
  resources:
    - name: cpu
      total: "0"
- name: overlapping-flavor
  resources:
    - name: cpu
      total: "0"
```

Create a workload requesting 2 CPU total (2 pods × 1 CPU each):

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: demo-1
  namespace: demo
spec:
  parallelism: 2
  completions: 10
  template:
    metadata:
      labels:
        kueue.x-k8s.io/queue-name: demo
    spec:
      containers:
        - name: demo
          image: gcr.io/k8s-staging-perf-tests/sleep:v0.1.0
          args: ["600s"]
          resources:
            requests:
              cpu: "1"
              memory: "100Mi"
      nodeSelector:
        kubernetes.io/os: linux
      restartPolicy: Never
```

Re-check usage:

```yaml
flavorsUsage:
- name: default-flavor
  resources:
    - name: cpu
      total: "2"   # <-- updated
- name: overlapping-flavor
  resources:
    - name: cpu
      total: "0"   # <-- remains zero despite overlapping nodes
```

**Key observation:**
Only one RF used for admission tracks usage. The overlapping RF reports `0` CPU usage even though its node set is also being consumed, unlike `ResourceQuota` where usage is reflected across all overlapping quotas.

---

## Impact

* Overlapping RF definitions can misrepresent capacity, effectively **double-counting** available resources,
  * Note: "double-count” implies just two, but in reality the overstatement scales with the number of overlapping RFs, so if a node belongs to three RFs its capacity is effectively counted three times in quota.
* This can lead to over-admission and over-subscription,
* Kueue provides no safeguards to prevent overlapping RF definitions, so the responsibility falls entirely on users to avoid them.
* Even in partial overlap scenarios, RF usage is not reflected across flavors for the shared node. This means overlapping nodes in different RFs can be double-counted.

---

## Possible Options

If these findings are correct, we could consider:

1. **Documentation update**, explicitly warn about the behavior of overlapping RFs,
2. **Enhanced accounting**, implement shared usage tracking for overlapping RFs, similar to `ResourceQuota` behavior.

## Discussion

### Comment by [@amy](https://github.com/amy) — 2025-08-14T21:12:15Z

+1 to fixing this especially if you're using flavors to denote something like classes of service (rather than non-overlapping instance types).

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-11-12T21:50:09Z

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

### Comment by [@amy](https://github.com/amy) — 2025-11-14T18:45:15Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-02-12T19:18:04Z

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

### Comment by [@amy](https://github.com/amy) — 2026-03-11T21:14:51Z

/priority important-longterm

### Comment by [@kannon92](https://github.com/kannon92) — 2026-03-12T16:05:56Z

Has anyone looked into how ResourceQuota solves this?

### Comment by [@amy](https://github.com/amy) — 2026-03-12T16:16:30Z

ResourceQuota though is scoped to accounting. The tricky part I feel like is the flavor selection changes needed for this. @kannon92

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-04-11T16:41:48Z

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
