# Issue #6118: Dynamic Local/Remote Workload Placement in MultiKueue Using Resource Flavors

**Summary**: Dynamic Local/Remote Workload Placement in MultiKueue Using Resource Flavors

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6118

**Last updated**: 2026-04-18T09:13:58Z

---

## Metadata

- **State**: open
- **Author**: [@gbenhaim](https://github.com/gbenhaim)
- **Created**: 2025-07-21T13:41:01Z
- **Updated**: 2026-04-18T09:13:58Z
- **Closed**: —
- **Labels**: `kind/feature`, `priority/important-longterm`, `lifecycle/rotten`, `area/multikueue`
- **Assignees**: _none_
- **Comments**: 7

## Description

**What would you like to be added**:

Enhance the MultiKueue admission check controller to dynamically decide whether workloads should execute locally on the management cluster or remotely on worker clusters, based on resource flavor configuration and quota availability. This would enable users to configure a single ClusterQueue with mixed local and remote resource flavors, with automatic fallback from local to remote execution when local quota is exhausted.

The proposed enhancement includes:

1. **Resource Flavor-Based Placement**: Extend resource flavors to include placement labels that indicate whether the flavor represents local or remote cluster resources.

2. **Dynamic Scheduling Logic**: Modify the multikueue admission check to evaluate resource flavors in priority order, preferring local execution and falling back to remote clusters when local quota is unavailable.

3. **Mixed ClusterQueue Support**: Enable ClusterQueues to contain both local and remote resource flavors, allowing seamless workload distribution based on resource availability.

**Key Insight**: This enhancement requires **no changes to MultiKueueConfig** - it leverages existing cluster lists and adds dynamic placement through ResourceFlavor labels and ClusterQueue flavor ordering.

**Why is this needed**:

While users can currently configure multiple ClusterQueues (some for local execution, others for remote execution), this approach has limitations that a dynamic single-queue solution would address:

**Current Multi-ClusterQueue Approach Limitations**:

1. **Static Placement Decisions**: With separate ClusterQueues for local and remote execution, users must pre-decide where workloads should run. There's no dynamic fallback when the preferred queue runs out of quota.

2. **Manual Queue Selection**: Users must explicitly choose which queue (local or remote) to submit workloads to, requiring operational knowledge about resource availability.

3. **No Automatic Failover**: When a local ClusterQueue is full, workloads remain queued rather than automatically falling back to available remote capacity.

4. **Complex Operational Management**: Administrators must monitor and manage multiple queues, making resource utilization optimization more difficult.

5. **Workload Fragmentation**: Related workloads may end up in different queues, making it harder to manage priorities and dependencies across local/remote boundaries.

**Use Cases**:

1. **Hybrid Cloud Environments**: Organizations want to prefer on-premises execution for cost/compliance reasons but fall back to cloud clusters for burst capacity.

2. **Tiered Resource Allocation**: Critical workloads should run locally on high-performance clusters, while less critical workloads can be distributed to remote clusters.

3. **Cost Optimization**: Prefer cheaper local resources first, then fall back to more expensive cloud resources only when needed.

**Proposed Implementation**:

1. **Enhanced Resource Flavor Configuration**:
```yaml
apiVersion: kueue.x-k8s.io/v1beta1
kind: ResourceFlavor
metadata:
  name: local-flavor
  labels:
    kueue.x-k8s.io/multikueue-placement: "local"

---
apiVersion: kueue.x-k8s.io/v1beta1
kind: ResourceFlavor  
metadata:
  name: remote-flavor
  labels
    kueue.x-k8s.io/multikueue-placement: "remote"
```

2. **Mixed ClusterQueue Configuration**:

The enhancement leverages Kueue's existing flavor ordering behavior - flavors are tried in the order they appear in the ClusterQueue specification, with no additional priority annotations needed.

**Important**: ResourceFlavors only define resource characteristics (node labels, taints, etc.) and placement type (`local` vs `remote`). The actual mapping to specific clusters is handled by the MultiKueue controller based on which remote clusters can satisfy the flavor's resource requirements.

**Benefits of Label-Based Approach**: Using labels instead of annotations enables:
- **Easy querying**: `kubectl get resourceflavors -l kueue.x-k8s.io/multikueue-placement=remote`
- **Programmatic selection**: Controllers can use label selectors to find all remote flavors
- **Kubernetes-native filtering**: Integrates naturally with Kubernetes API patterns
- **Operational visibility**: Administrators can easily filter and manage placement types

```yaml
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: hybrid-pipeline-queue
spec:
  namespaceSelector: {}
  queueingStrategy: BestEffortFIFO
  admissionChecks:
  - dynamic-multikueue            # Required: enables dynamic placement
  resourceGroups:
  - coveredResources: ["cpu", "memory", "tekton.dev/pipelineruns"]
    flavors:
    # Flavors are tried in order - local flavors first, then remote fallbacks
    - name: local-flavor           # 1st priority: local execution
      resources:
      - name: "cpu"
        nominalQuota: 8
      - name: "memory"  
        nominalQuota: 16Gi
      - name: "tekton.dev/pipelineruns"
        nominalQuota: 5
    - name: remote-flavor          # 2nd priority: remote fallback
      resources:
      - name: "cpu"
        nominalQuota: 48           # Combined quota across remote clusters
      - name: "memory"
        nominalQuota: 96Gi  
      - name: "tekton.dev/pipelineruns"
        nominalQuota: 30
```

3. **Admission Check Configuration**:
```yaml
apiVersion: kueue.x-k8s.io/v1beta1
kind: AdmissionCheck
metadata:
  name: dynamic-multikueue
spec:
  controllerName: kueue.x-k8s.io/multikueue
  parameters:
    apiGroup: kueue.x-k8s.io
    kind: MultiKueueConfig
    name: existing-multikueue-config

---
# Uses existing MultiKueueConfig - no changes needed
apiVersion: kueue.x-k8s.io/v1beta1
kind: MultiKueueConfig
metadata:
  name: existing-multikueue-config
spec:
  clusters: ["cluster-a", "cluster-b", "cluster-c"]
  # No additional fields needed - the intelligence comes from:
  # 1. ResourceFlavor placement labels
  # 2. ClusterQueue flavor ordering  
  # 3. Existing cluster health and availability logic
```

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change (new ResourceFlavor label only)  
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2025-07-22T15:36:04Z

Reading this I am reminded of OCM + MK: https://github.com/open-cluster-management-io/ocm/tree/main/solutions/kueue-admission-check

cc @haoqing0110

Could there be a world OCM's placements could be used here?

### Comment by [@haoqing0110](https://github.com/haoqing0110) — 2025-07-23T11:00:53Z

With the [implementation](https://github.com/kubernetes-sigs/kueue/pull/5782) of [MultiKueue dispatcher API](https://github.com/kubernetes-sigs/kueue/issues/5141), I suppose we can do so with OCM's placements [decision group](https://open-cluster-management.io/docs/concepts/content-placement/placement/#decision-strategy) + MK. 

In one placement, you can define local and remote clusters into 2 groups, and the external controller (not the one in current OCM + MK solution) can schedule workload in the order of the group, like local first, and if it fails, then go to remote. In placement, you can organize the order according to any requirement, not limited to local and remote

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-10-21T11:05:55Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-11-20T12:01:17Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T08:25:10Z

/area multikueue
/priority important-longterm
/remove-lifecycle rotten

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-03-19T08:44:23Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-04-18T09:13:55Z

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
