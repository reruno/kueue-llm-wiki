# Issue #2937: Configurable mechanism for Resource Abstraction

**Summary**: Configurable mechanism for Resource Abstraction

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2937

**Last updated**: 2024-10-21T15:47:08Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@dgrove-oss](https://github.com/dgrove-oss)
- **Created**: 2024-08-30T00:58:56Z
- **Updated**: 2024-10-21T15:47:08Z
- **Closed**: 2024-10-21T15:47:06Z
- **Labels**: `kind/feature`
- **Assignees**: [@dgrove-oss](https://github.com/dgrove-oss)
- **Comments**: 8

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

The capability for a cluster admin to configure Kueue to customize the computation it does to derive the Resource requirements of a Workload from the Resource requests/limits in the PodSpecs of the submitted Job.  

**Why is this needed**:

Configurable Resource transformations would enable more flexible definitions of Quotas that can be both simpler and more powerful than those possible via simple mirroring of the PodSpec Resources of Jobs into Workloads.  It would support at least the following scenarios:

1. Reducing multiple complex related accelerator resources into a simpler resource that is more suitable for quota management.  The motivation example here is the various MIG resources created by the NVIDIA CPU Operator when it is operating in a mixed strategy.

2. Mapping multiple resources into an abstract currency that can be used to define quotas in terms of the relative cost of the resources (eg cheap vs. expensive GPUs or spot vs normal cloud VMs). 

Both scenarios were discussed in the Batch WG call of 8/29/24 (https://www.youtube.com/watch?v=5nb_Ut-PLac), resulting in a decision to open a KEP to refine a design for this capability.  The presentation is attached here:
[BatchWG-MIGResourceAbstraction.pdf](https://github.com/user-attachments/files/16818545/BatchWG-MIGResourceAbstraction.pdf)
 

**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [x] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2024-08-30T00:59:51Z

/assign
I'll work on a KEP next week.

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2024-10-01T18:26:50Z

Design Doc: #3013 
API Change: #3026 
Docs Update: #3175

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-21T14:00:33Z

/close 
IIUC all the parts are done. We can open a separate issue if there are bugs, or when we want to promote it to beta.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-10-21T14:00:39Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/2937#issuecomment-2426772909):

>/close 
>IIUC all the parts are done. We can open a separate issue if there are bugs, or when we want to promote it to beta.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-21T14:03:28Z

/reopen
I missed https://github.com/kubernetes-sigs/kueue/pull/3175 is not merged yet, let's wait for it.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-10-21T14:03:33Z

@mimowo: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/2937#issuecomment-2426780837):

>/reopen
>I missed https://github.com/kubernetes-sigs/kueue/pull/3175 is not merged yet, let's wait for it.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-21T15:47:02Z

/close 
as the docs are merged now 👍

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-10-21T15:47:06Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/2937#issuecomment-2427062215):

>/close 
>as the docs are merged now 👍 


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
