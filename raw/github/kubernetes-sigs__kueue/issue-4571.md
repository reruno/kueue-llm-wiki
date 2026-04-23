# Issue #4571: TAS: workloads with nodeSelectors are scheduled by TAS, but not kube-scheduler

**Summary**: TAS: workloads with nodeSelectors are scheduled by TAS, but not kube-scheduler

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4571

**Last updated**: 2025-04-24T10:34:37Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-03-12T14:49:03Z
- **Updated**: 2025-04-24T10:34:37Z
- **Closed**: 2025-04-24T10:34:37Z
- **Labels**: `kind/bug`
- **Assignees**: [@mwysokin](https://github.com/mwysokin)
- **Comments**: 14

## Description

**What happened**:

When using explicit nodeSelectors in the Job / Workload spec the pods might not be able to scheduled by kube-scheduler, even though they are scheduled by TAS.

**What you expected to happen**:

TAS will restrict the set of considered leaf domains (nodes) only to those which match the specified node selectors.
Similarly, as we restrict the set of considered nodes based on taints and tolerations.

**How to reproduce it (as minimally and precisely as possible)**:

Create the TAS setup:

```yaml
kind: ResourceFlavor
apiVersion: kueue.x-k8s.io/v1beta1
metadata:
  name: "tas-flavor"
spec:
  nodeLabels:
    kubernetes.io/os: "linux"
  topologyName: "default"
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: "tas-cluster-queue"
spec:
  namespaceSelector: {} # match all.
  resourceGroups:
  - coveredResources: ["cpu", "memory"]
    flavors:
    - name: "tas-flavor"
      resources:
      - name: "cpu"
        nominalQuota: 200 
      - name: "memory"
        nominalQuota: 200Gi
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: LocalQueue
metadata:
  namespace: "default"
  name: "tas-user-queue"
spec:
  clusterQueue: "tas-cluster-queue"
---
apiVersion: kueue.x-k8s.io/v1alpha1
kind: Topology
metadata:
  name: "default"
spec:
  levels:
  - nodeLabel: "kubernetes.io/hostname"
```
2. create a Job with a node selector, eg.

```yaml
apiVersion: batch/v1
kind: Job 
metadata:
  generateName: tas-sample-small-required-host-
  labels:
    kueue.x-k8s.io/queue-name: tas-user-queue
spec:
  parallelism: 2
  completions: 2
  completionMode: Indexed
  template:
    metadata:
      annotations:
        kueue.x-k8s.io/podset-required-topology: "kubernetes.io/hostname"
    spec:
      nodeSelector:
        kubernetes.io/hostname: "kind-worker3"
      containers:
      - name: dummy-job
        image: gcr.io/k8s-staging-perf-tests/sleep:v0.1.0
        args: ["1800s"]
        resources:
          requests:
            cpu: "1" 
            memory: "200Mi"
      restartPolicy: Never
```

Result, the workload is scheduled, but the pods remain suspended;

```
> k get pods -owide
NAME                                           READY   STATUS            RESTARTS   AGE     IP       NODE     NOMINATED NODE   READINESS GATES
tas-sample-small-required-host-t29tv-0-fldzf   0/1     SchedulingGated   0          4m35s   <none>   <none>   <none>           <none>
tas-sample-small-required-host-t29tv-1-2d97m   0/1     SchedulingGated   0          4m35s   <none>   <none>   <none>           <none>
```

**Anything else we need to know?**:

We already solve the similar problem for taints and tolerations. PTAL: https://github.com/kubernetes-sigs/kueue/blob/843e4df0a871cb83d0e1ed0b26bbe6f65e171a06/pkg/cache/tas_flavor_snapshot.go#L621-L628

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-12T14:49:25Z

cc @PBundyra @tenzen-y @mwysokin @mwielgus @mbobrovskyi

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-13T00:26:12Z

Is this not related to kube-scheduler? It looks like we forgot to clear the schedulingGate after TAS scheduling, right?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-13T06:57:50Z

I think in this case the topology_ungater was confused and didn't unschedule, because the node selector on workload was pointing to "kind-worker3" while TAS assigned "kind-worker". Ideally, the TAS assignment is correct and would only consider "kind-worker3" as the "matching" node. We already do such filtering for taints.

Also, consider more generic case, where you have a TAS nodepool, and a user wants to split it into two parts "A" and "B". To achieve this when may add labels to node, say "part: A", and "part: B". Then, add the nodeSelectors to the workloads.
For, example, a workload targeting part "A" has the selector "part: A", but currently TAS may assign it to "part B", because it considers the entire nodepool without any filtering.

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-03-13T09:06:11Z

Don't we have a similar issue when a workload has toleration assigned? In the code snippet you provided in the description we take into account tolerations, but those come from the resource flavor, not the job definition itself

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-13T09:15:04Z

> Don't we have a similar issue when a workload has toleration assigned? 

We had originally, but it was solved by the code snippet, I attached to show how it was solved. I think for node labels, we could analogously keep the node labels in the leafDomains, and for each workload check if it is matching. This way we can constrain the subset of leaf domains.

> In the code snippet you provided in the description we take into account tolerations, but those come from the resource flavor, not the job definition itself

It takes both places into account. When calling the function we append the tolerations here: https://github.com/kubernetes-sigs/kueue/blob/843e4df0a871cb83d0e1ed0b26bbe6f65e171a06/pkg/cache/tas_flavor_snapshot.go#L425

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-03-13T09:37:54Z

Ah right, I missed `podSetTolerations`

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-13T10:01:27Z

> I think in this case the topology_ungater was confused and didn't unschedule, because the node selector on workload was pointing to "kind-worker3" while TAS assigned "kind-worker". Ideally, the TAS assignment is correct and would only consider "kind-worker3" as the "matching" node. We already do such filtering for taints.
> 
> Also, consider more generic case, where you have a TAS nodepool, and a user wants to split it into two parts "A" and "B". To achieve this when may add labels to node, say "part: A", and "part: B". Then, add the nodeSelectors to the workloads. For, example, a workload targeting part "A" has the selector "part: A", but currently TAS may assign it to "part B", because it considers the entire nodepool without any filtering.

In that case, I think we can take A. we support all scheduling directives like nodeSelector, topologySpread, and so on B. we make Pod scheduling directives and TAS topology requirements as mutually exclusive, which means they can specify TAS topology only when they do not specify nodeSelector and so one manually.

I think B. is the easier way. In case of nodeSelector, we might be able to support it in TAS, but I guess users continue request full scheduling simulation rather than nodeSelector. So, for 0.11, we might want to take approach B. But, in the next and after the next release, we expand supporting scheduling directive step by step.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-13T10:07:48Z

Right, the north star for TAS is to make sure that all scheduling directives are supported. In other words, whenever TAS makes an assignment, then kube-scheduler is compatible with it. 

I think the best way to achieve full compatibility is to vendor kube-scheduler helper functions for checking the conditions. 

However, until then, supporting just nodeSelectors seems like a low hanging fruit, similarly as we did for taints.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-13T10:13:26Z

> Right, the north star for TAS is to make sure that all scheduling directives are supported. In other words, whenever TAS makes an assignment, then kube-scheduler is compatible with it.
> 
> I think the best way to achieve full compatibility is to vendor kube-scheduler helper functions for checking the conditions.
> 
> However, until then, supporting just nodeSelectors seems like a low hanging fruit, similarly as we did for taints.

IIUC, kube-scheduler has ClusterAutoscaler contacting package. But in the case of Kueue, I do not think that we can do that.
For now, let's support only nodeSelector by ourselves. 
After that, let's investigate which kube-scheduler codes must be exposed as staging for us, and propose it to sig-scheduling meeting.

I guess we need to do a lot of effort...

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-13T10:17:23Z

Yeah, vendoring kube-scheduler will be a lot of effort on its own, ticketed as: https://github.com/kubernetes-sigs/kueue/issues/3755. So, I'm thinking before that we can support nodeSelector by ourselves.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-03-26T14:45:20Z

/assign

### Comment by [@mwysokin](https://github.com/mwysokin) — 2025-04-15T21:49:06Z

@mbobrovskyi I had a free evening and decided to take a stab at this issue. Since you originally were interested in it it'd be really great if you could take a look at my attempt https://github.com/kubernetes-sigs/kueue/pull/4989 🙏

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-04-18T09:42:50Z

/unassign

### Comment by [@mwysokin](https://github.com/mwysokin) — 2025-04-18T14:59:45Z

/assign
