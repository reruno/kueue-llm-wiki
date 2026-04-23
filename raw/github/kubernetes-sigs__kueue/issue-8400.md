# Issue #8400: TAS resource flavor controller regularly reconciled by irrelevant node updates

**Summary**: TAS resource flavor controller regularly reconciled by irrelevant node updates

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8400

**Last updated**: 2026-01-08T17:05:05Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@Ladicle](https://github.com/Ladicle)
- **Created**: 2025-12-24T01:24:44Z
- **Updated**: 2026-01-08T17:05:05Z
- **Closed**: 2026-01-07T16:19:42Z
- **Labels**: `kind/bug`, `priority/important-soon`
- **Assignees**: _none_
- **Comments**: 12

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->

**What happened**:

`tas_resource_flavor_controller` already filters out some irrelevant node updates, but still some unnecessary status updates trigger the reconciliation. For example, `.status.runtimeHandler` randomly changes its order, `.status.images` changes whenever new images are loaded onto the node. Even when testing this with kind, the node's event updates occur only every few seconds. 

**What you expected to happen**:

Inadmissible workloads are re-evaluated only when the related events happen.

**How to reproduce it (as minimally and precisely as possible)**:

Add a log line after `checkNodeSchedulingPropertiesChanged(oldNode, newNode)` and check the object diffs.

**Anything else we need to know?**:

In our production env, we apply the following patches:

- Instead of filtering out unnecessary events, only extract the required events. e.g.
```
func nodeSchedulingPropertiesChange(newNode *v1.Node, oldNode *v1.Node) eventType {
	nodeChangeExtracters := []nodeChangeExtractor{
		extractNodeSpecUnschedulableChange,
		extractNodeAllocatableChange,
		extractNodeLabelsChange,
		extractNodeTaintsChange,
		extractNodeConditionsChange,
		extractNodeAnnotationsChange,
	}
	var at eventType
	for _, fn := range nodeChangeExtracters {
		at |= fn(newNode, oldNode)
	}
	return at
}
...
```

- Make the queueing interval customizable to ease requeue frequency. This prevents requeueing when a node's taint is continuously updated over a short period (e.g., due to hardware failure). This workaround might be unnecessary once https://github.com/kubernetes-sigs/kueue/issues/8339 is resolved.
:

```
func (h *nodeHandler) queueReconcileForNode(node *corev1.Node, q workqueue.TypedRateLimitingInterface[reconcile.Request]) {
	if node == nil {
		return
	}
	// trigger reconcile for TAS flavors affected by the node being created or updated
	for name, cache := range h.cache.CloneTASCache() {
		if nodeBelongsToFlavor(node, cache.NodeLabels(), cache.TopologyLevels()) {
			q.AddAfter(reconcile.Request{NamespacedName: types.NamespacedName{
				Name: string(name),
			}}, h.tasFlavorRequeuPeriod) // originally: `constants.UpdatesBatchPeriod` (1s)
		}
	}
}
```

**Environment**:

- Kubernetes version (use `kubectl version`): v1.34.2
- Kueue version (use `git describe --tags --dirty --always`): v1.15.2
- Cloud provider or hardware configuration: kind
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-12-24T02:59:02Z

@Ladicle, which TAS feature do you enable?

https://kueue.sigs.k8s.io/docs/installation/#feature-gates-for-alpha-and-beta-features

### Comment by [@Ladicle](https://github.com/Ladicle) — 2025-12-24T04:28:18Z

Ah, sorry. We only enable `TopologyAwareScheduling`.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-12-24T15:40:35Z

> Ah, sorry. We only enable `TopologyAwareScheduling`.

Thank you for letting us know that. At first glance, your filtering patch (`nodeSchedulingPropertiesChange`) looks like it is working correctly. But, we probably want to check if all TAS features (not only for TopologyAwareScheduling FG) can work well.

Anyway, I think it's worth creating a PR to ship the filters.

For queueing interval customization, let's track it in another issue as you mentioned if it is really needed.

@PBundyra @mimowo Any thoughts?

@kshalot Failure controller PoV, do you think the proposed node event filtering has an impact on the node failure controller behaviors? (I believe that we don't have such a problem, but let me check carefully).

### Comment by [@kshalot](https://github.com/kshalot) — 2026-01-07T10:09:35Z

@tenzen-y Sorry for the late response, I just got back from my holiday break.

The node event filtering/taint change rate limiting won't have an impact on the failure recovery controller. There is no dependency between those two controllers + IIUC all the changes proposed are "local" to `tas_resource_flavor_controller`.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-07T10:20:42Z

+1 for the proposal. The initial fix was only scoped for heartbeats: https://github.com/kubernetes-sigs/kueue/issues/8340, but filtering only what is needed is a much better approach. @Ladicle would you like to submit a PR?

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-07T10:21:11Z

> For queueing interval customization, let's track it in another issue as you mentioned if it is really needed.

+1

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-07T10:21:38Z

/priority important-soon

### Comment by [@Ladicle](https://github.com/Ladicle) — 2026-01-07T10:26:40Z

Yes, I'm happy to submit a PR for this.

### Comment by [@PBundyra](https://github.com/PBundyra) — 2026-01-07T10:56:52Z

+1 for this feature

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-07T16:22:22Z

> [@tenzen-y](https://github.com/tenzen-y) Sorry for the late response, I just got back from my holiday break.
> 
> The node event filtering/taint change rate limiting won't have an impact on the failure recovery controller. There is no dependency between those two controllers + IIUC all the changes proposed are "local" to `tas_resource_flavor_controller`.

No worries, thank you for checking that. That sounds reasonable 👍

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-08T17:03:14Z

@Ladicle @PBundyra @tenzen-y turns out part of the issues (unnecessary updates to runtimeHandlers) is already tracked as issue in the core k8s: https://github.com/kubernetes/kubernetes/issues/135357

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-08T17:05:05Z

> @Ladicle @PBundyra @tenzen-y turns out part of the issues (unnecessary updates to runtimeHandlers) is already tracked as issue in the core k8s: https://github.com/kubernetes/kubernetes/issues/135357

Thank you for xref here 👍
