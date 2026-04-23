# Issue #7787: v1beta2: Decouple FairSharingStatus from LocalQueue

**Summary**: v1beta2: Decouple FairSharingStatus from LocalQueue

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7787

**Last updated**: 2025-11-21T07:10:35Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-11-20T20:19:53Z
- **Updated**: 2025-11-21T07:10:35Z
- **Closed**: 2025-11-21T07:10:35Z
- **Labels**: `kind/feature`
- **Assignees**: [@tenzen-y](https://github.com/tenzen-y)
- **Comments**: 3

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
I would propose uncommonizing FaireSharingStatus: https://github.com/kubernetes-sigs/kueue/blob/8c3ed54cacceec656dea21fc615adf41e251e0c8/apis/kueue/v1beta2/fairsharing_types.go#L49-L63

So, my proposal is introducing the following typed:

1. The LocalQueueFairSharingStatus for LocalQueue.

```go
// LocalQueueFairSharingStatus contains the information about the current status of Fair Sharing.
type LocalQueueFairSharingStatus struct {
	// weightedShare represents the maximum of the ratios of usage
	// above nominal quota to the lendable resources in the
	// Cohort, among all the resources provided by the Node, and
	// divided by the weight.  If zero, it means that the usage of
	// the Node is below the nominal quota.  If the Node has a
	// weight of zero and is borrowing, this will return
	// 9223372036854775807, the maximum possible share value.
	// +required
	WeightedShare int64 `json:"weightedShare"`

	// admissionFairSharingStatus represents information relevant to the Admission Fair Sharing
	// +optional
	AdmissionFairSharingStatus *AdmissionFairSharingStatus `json:"admissionFairSharingStatus,omitempty"`
}
```

1. The FairSharingStatus for ClusterQueue and Cohort

```go
// FairSharingStatus contains the information about the current status of Fair Sharing.
type FairSharingStatus struct {
	// weightedShare represents the maximum of the ratios of usage
	// above nominal quota to the lendable resources in the
	// Cohort, among all the resources provided by the Node, and
	// divided by the weight.  If zero, it means that the usage of
	// the Node is below the nominal quota.  If the Node has a
	// weight of zero and is borrowing, this will return
	// 9223372036854775807, the maximum possible share value.
	// +required
	WeightedShare int64 `json:"weightedShare"`
}
```

**Why is this needed**:
Currently, LocalQueue, ClusterQueue, and Cohort use a commonized `FairSharingStatus` object, but in the ClusterQueue and Cohort cases, the `admissionFairSharingStatus` has never been used.

We should remove the never-used fields.
However, these fields have already been released for the v1beta1 API. So, we can work on this improvement only for v1beta2.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-11-20T20:20:13Z

cc @mimowo @PBundyra

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-11-20T20:25:11Z

The LocalQueue controller has AFS status involving mechanism in https://github.com/kubernetes-sigs/kueue/blob/8c3ed54cacceec656dea21fc615adf41e251e0c8/pkg/controller/core/localqueue_controller.go#L263-L274

But, ClusterQueue and Cohort controllers do not have such mechanisms:
https://github.com/kubernetes-sigs/kueue/blob/8c3ed54cacceec656dea21fc615adf41e251e0c8/pkg/controller/core/cohort_controller.go#L169-L177
https://github.com/kubernetes-sigs/kueue/blob/8c3ed54cacceec656dea21fc615adf41e251e0c8/pkg/controller/core/clusterqueue_controller.go#L564-L578
because AFS will be computed based on LocalQueue usage.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-11-20T21:05:48Z

tentatively
/assign
