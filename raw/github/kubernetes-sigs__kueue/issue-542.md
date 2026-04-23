# Issue #542: Report resource usage in LocalQueues

**Summary**: Report resource usage in LocalQueues

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/542

**Last updated**: 2023-05-08T17:23:42Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2023-02-01T22:40:32Z
- **Updated**: 2023-05-08T17:23:42Z
- **Closed**: 2023-05-08T17:23:42Z
- **Labels**: `kind/feature`
- **Assignees**: [@tenzen-y](https://github.com/tenzen-y)
- **Comments**: 11

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Add resource usage fields in the LocalQueueStatus. We currently only add the number of admitted and pending workloads.

**Why is this needed**:

To improve observability.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [x] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-03-14T12:33:35Z

@alculquicondor, Can I take this?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-03-14T13:38:31Z

I'm a bit hesitant to do this in 0.3, given that it would require a few changes in the cache. Unless it's rather small?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-03-14T14:05:11Z

> I'm a bit hesitant to do this in 0.3, given that it would require a few changes in the cache. Unless it's rather small?

IIRC, we plan to release v0.3 this week, right? If so, it might be better to stop adding this feature now.

However, it might be worth moving the discussion about API changes forward.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-03-14T14:37:12Z

sgtm

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-03-22T17:01:07Z

For now, I will move the API design forward in this issue. I will create a PR for implementation after we cut v0.3.
/assign

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-03-23T09:18:13Z

@alculquicondor  My API design proposal is here. Maybe, we have two options:

1. Create new APIs.

```go
// LocalQueueStatus defines the observed state of LocalQueue
type LocalQueueStatus struct {
...
	// queueUsage are the used quotas, by flavor currently in use by the
	// workloads assigned to this LocalQueue.
	// +listType=map
	// +listMapKey=name
	// +kubebuilder:validation:MaxItems=16
	// +optional
	QueueUsage []QueueUsage `json:"queueUsage"`  
}

type QueueUsage struct {
	// name of the flavor.
	Name ResourceFlavorReference `json:"name"`

	// resources lists the quota usage for the resources in this flavor.
	// +listType=map
	// +listMapKey=name
	// +kubebuilder:validation:MaxItems=16
	Resources []QueueResourceUsage `json:"resources"`
}

type QueueResourceUsage struct {
	// name of the resource
	Name corev1.ResourceName `json:"name"`

	// total is the total quantity of used quota.
	Total resource.Quantity `json:"total,omitempty"`
}
```

2. Reuse [FlavorUsage](https://github.com/kubernetes-sigs/kueue/blob/a974aa2216e972c64253b2bb80ce7beaade9b966/apis/kueue/v1beta1/clusterqueue_types.go#L207-L216), although we don't set any value to `flavorUsage.resources.borrowed`.

```go
// LocalQueueStatus defines the observed state of LocalQueue
type LocalQueueStatus struct {
...
	// flavorsUsage are the used quotas, by flavor, currently in use by the
	// workloads assigned to this LocalQueue.
	// +listType=map
	// +listMapKey=name
	// +kubebuilder:validation:MaxItems=16
	// +optional
	FlavorsUsage []FlavorUsage `json:"flavorsUsage"`  
}
```

wdyt?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-03-23T13:26:08Z

It makes sense to have a different set of structs because Borrowed doesn't make sense in LocalQueue. But I would still make all the field names match.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-03-23T14:26:32Z

> It makes sense to have a different set of structs because Borrowed doesn't make sense in LocalQueue. But I would still make all the field names match.

It sounds good. We can take the first option by matching field names with ClusterQueueStatus.

Note: Add 'Queue' to the name of structs as a prefix to avoid collision with ClusterQueueStatus.

```go
// LocalQueueStatus defines the observed state of LocalQueue
type LocalQueueStatus struct {
...
	// flavorUsage are the used quotas, by flavor currently in use by the
	// workloads assigned to this LocalQueue.
	// +listType=map
	// +listMapKey=name
	// +kubebuilder:validation:MaxItems=16
	// +optional
	FlavorUsage []QueueFlavorUsage `json:"flavorUsage"`
}

type QueueFlavorUsage struct {
	// name of the flavor.
	Name ResourceFlavorReference `json:"name"`

	// resources lists the quota usage for the resources in this flavor.
	// +listType=map
	// +listMapKey=name
	// +kubebuilder:validation:MaxItems=16
	Resources []QueueResourceUsage `json:"resources"`
}

type QueueResourceUsage struct {
	// name of the resource
	Name corev1.ResourceName `json:"name"`

	// total is the total quantity of used quota.
	Total resource.Quantity `json:"total,omitempty"`
}
```

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-03-23T14:31:21Z

make it `LocalQueue`

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-03-23T14:35:06Z

Updated.

```go
// LocalQueueStatus defines the observed state of LocalQueue
type LocalQueueStatus struct {
...
	// flavorUsage are the used quotas, by flavor currently in use by the
	// workloads assigned to this LocalQueue.
	// +listType=map
	// +listMapKey=name
	// +kubebuilder:validation:MaxItems=16
	// +optional
	FlavorUsage []LocalQueueFlavorUsage `json:"flavorUsage"`
}

type LocalQueueFlavorUsage struct {
	// name of the flavor.
	Name ResourceFlavorReference `json:"name"`

	// resources lists the quota usage for the resources in this flavor.
	// +listType=map
	// +listMapKey=name
	// +kubebuilder:validation:MaxItems=16
	Resources []LocalQueueResourceUsage `json:"resources"`
}

type LocalQueueResourceUsage struct {
	// name of the resource
	Name corev1.ResourceName `json:"name"`

	// total is the total quantity of used quota.
	Total resource.Quantity `json:"total,omitempty"`
}
```

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-03-23T14:36:15Z

LGTM
