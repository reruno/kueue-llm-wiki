# Issue #102: Set pending condition on QueuedWorkload with message

**Summary**: Set pending condition on QueuedWorkload with message

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/102

**Last updated**: 2022-03-29T20:15:18Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2022-03-08T19:33:20Z
- **Updated**: 2022-03-29T20:15:18Z
- **Closed**: 2022-03-29T20:15:16Z
- **Labels**: `kind/feature`
- **Assignees**: [@ArangoGutierrez](https://github.com/ArangoGutierrez)
- **Comments**: 14

## Description

A queued workload can be pending for several reasons:

- The Queue doesn't exist
- The ClusterQueue doesn't exist
- The QW's namespace is not allowed by the ClusterQueue
- The workload was attempted for scheduling but it didn't fit.

We need to find a way to set this information.

Probably the first 2 can happen in the queuedworkload_controller, after every update.
The other 2 should probably during scheduling.

/kind feature

## Discussion

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-03-08T21:00:59Z

I think this can help with #88 as well

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-03-08T21:20:04Z

/help

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-03-08T21:24:30Z

/assign

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-03-16T13:02:44Z

is this still in progress?

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-03-16T13:16:55Z

yes, will take back on this. I have been busy and #101 distracted me for a bit

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-03-16T13:17:34Z

sg, thanks, I will remove the help tag then.

/remove-help

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-03-17T15:27:25Z

Working on this today

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-03-17T15:52:39Z

Question:
Why  https://github.com/kubernetes-sigs/kueue/blob/main/api/v1alpha1/queuedworkload_types.go#L96 is a map and not an array?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-03-17T18:27:13Z

which field? I think the lines in the file moved.

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-03-17T19:01:59Z

```go
// QueuedWorkloadStatus defines the observed state of QueuedWorkload
type QueuedWorkloadStatus struct {
	// conditions hold the latest available observations of the QueuedWorkload
	// current state.
	// +optional
	// +listType=map
	// +listMapKey=type
	Conditions []QueuedWorkloadCondition `json:"conditions,omitempty"`
}
```
Why is a map, if we want to keep the conditions as an array in the order they occur

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-03-17T19:36:04Z

And we have been treating that var like an array in places where the conditions are set.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-03-17T20:09:21Z

The order shouldn't matter. Each condition has a timestamp.

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-03-29T20:15:05Z

https://github.com/kubernetes-sigs/kueue/pull/150 should be enough to close this one
/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2022-03-29T20:15:17Z

@ArangoGutierrez: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/102#issuecomment-1082331699):

>https://github.com/kubernetes-sigs/kueue/pull/150 should be enough to close this one
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
