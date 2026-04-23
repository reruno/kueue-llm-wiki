# Issue #8669: Show "failed to read rank information" error logs for Pod integrations when TAS is enabled

**Summary**: Show "failed to read rank information" error logs for Pod integrations when TAS is enabled

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8669

**Last updated**: 2026-01-20T15:14:34Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@Ladicle](https://github.com/Ladicle)
- **Created**: 2026-01-19T15:49:42Z
- **Updated**: 2026-01-20T15:14:34Z
- **Closed**: 2026-01-20T14:58:55Z
- **Labels**: `kind/bug`, `priority/important-soon`
- **Assignees**: [@IrvingMg](https://github.com/IrvingMg)
- **Comments**: 8

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

When `TopologyAwareSchedulin` (TAS) is enabled and the ResourceFlavor has a topology, the workload (using Pod framework) generates the error logs in the kueue controller. This is not 

The Pods themselves are scheduled and run successfully, but the controller repeatedly logs the following error:
```
"message": "failed to read rank information from Pods"
"error":"label not found: no label \"kueue.x-k8s.io/pod-group-pod-index\" for Pod \"...\""
```
https://github.com/kubernetes-sigs/kueue/blob/main/pkg/controller/tas/topology_ungater.go#L435

These error logs can be misleading, as they suggest an error state for workloads that are actually running healthily.

**What you expected to happen**:

According to [KEP-976](https://github.com/kubernetes-sigs/kueue/blob/main/keps/976-plain-pods/README.md#groups-of-pods-created-beforehand), my understanding is that the kueue.x-k8s.io/pod-group-pod-index label is optional.

Ideally, Kueue would handle the missing `pod-index` label gracefully for Pod integrations. Looking at the current code base, it seems to always attempt to set the `pod index` from the label.

https://github.com/kubernetes-sigs/kueue/blob/main/pkg/controller/jobs/pod/pod_controller.go#L698-L706
```go
	if features.Enabled(features.TopologyAwareScheduling) {
		topologyRequest, err := jobframework.NewPodSetTopologyRequest(
			&p.ObjectMeta).PodIndexLabel(
			ptr.To(kueue.PodGroupPodIndexLabel)).Build()
		if err != nil {
			return kueue.PodSet{}, err
		}
		podSet.TopologyRequest = topologyRequest
	}
```

**How to reproduce it (as minimally and precisely as possible)**:

- Enable `TopologyAwareScheduling`
- Configure a ClusterQueue and ResourceFlavor (with Topology enabled).
- Create a Workload using the Pod framework (e.g., Deployments, bare Pods)

<details>
```yaml
apiVersion: kueue.x-k8s.io/v1beta2
kind: Topology
metadata:
  name: default-topology
spec:
  levels:
  - nodeLabel: kubernetes.io/hostname
---
apiVersion: kueue.x-k8s.io/v1beta2
kind: ResourceFlavor
metadata:
  name: default-flavor
spec:
  nodeLabels:
    kubernetes.io/hostname: kind-control-plane
  topologyName: default-topology
---
apiVersion: kueue.x-k8s.io/v1beta2
kind: ClusterQueue
metadata:
  name: cluster-queue
spec:
  namespaceSelector: {}
  resourceGroups:
  - coveredResources: ["cpu", "memory"]
    flavors:
    - name: default-flavor
      resources:
      - name: cpu
        nominalQuota: 9
      - name: memory
        nominalQuota: 36Gi
```
</details>

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`): 1.34
- Kueue version (use `git describe --tags --dirty --always`): 0.15.2
- Cloud provider or hardware configuration: both production and kind cluster
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-19T15:53:43Z

This is likely related to https://github.com/kubernetes-sigs/kueue/issues/8558

Would it help if we just log it as debug without stracktrace?

### Comment by [@Ladicle](https://github.com/Ladicle) — 2026-01-19T16:04:16Z

Yes, it sounds good!

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-19T16:13:25Z

Would you like to submit a PR?

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-19T16:22:52Z

/priority important-soon

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-19T16:48:26Z

> This is likely related to [#8558](https://github.com/kubernetes-sigs/kueue/issues/8558)
> 
> Would it help if we just log it as debug without stracktrace?

I think moving this log to debug level V(5)+ would be better instead of completely omitting this one.

### Comment by [@Ladicle](https://github.com/Ladicle) — 2026-01-19T23:17:31Z

I agree that having debug logs is helpful. However, currently, the "label missing" log appears even for Pods that don't have podset-required-topology or podset-preferred-topology set.

https://github.com/kubernetes-sigs/kueue/blob/main/pkg/controller/jobframework/tas.go#L75

I might be missing something here, but it looks like `podSetTopologyRequestBuilder` relies on nil checks. However, the label is wrapped with `ptr.To` and it always returns a non-nil value. I was wondering if it would be better to omit it if it doesn't exist?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-20T15:14:19Z

> I agree that having debug logs is helpful. However, currently, the "label missing" log appears even for Pods that don't have podset-required-topology or podset-preferred-topology set.
> 
> https://github.com/kubernetes-sigs/kueue/blob/main/pkg/controller/jobframework/tas.go#L75
> 
> I might be missing something here, but it looks like `podSetTopologyRequestBuilder` relies on nil checks. However, the label is wrapped with `ptr.To` and it always returns a non-nil value. I was wondering if it would be better to omit it if it doesn't exist?

@Ladicle Sorry, this has been fixed as part of another associated problem by @IrvingMg in https://github.com/kubernetes-sigs/kueue/pull/8689.
The root cause was topology ungater didn't ignore the rank recognition error. Please let us know if the fix will not fix your problem.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-20T15:14:31Z

/assign @IrvingMg
