# Issue #1136: Support Cluster-Autoscaler's ProvisioningRequest via two-stage admission

**Summary**: Support Cluster-Autoscaler's ProvisioningRequest via two-stage admission

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1136

**Last updated**: 2023-10-23T13:53:43Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@trasc](https://github.com/trasc)
- **Created**: 2023-09-19T11:01:11Z
- **Updated**: 2023-10-23T13:53:43Z
- **Closed**: 2023-10-23T13:53:43Z
- **Labels**: `kind/feature`
- **Assignees**: [@mwielgus](https://github.com/mwielgus), [@trasc](https://github.com/trasc)
- **Comments**: 7

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Use two-stage admission to support [Cluster-Autoscaler's ProvisioningRequest](https://github.com/kubernetes/autoscaler/blob/master/cluster-autoscaler/proposals/provisioning-request.md)

**Why is this needed**:

The ProvisioningRequest API allows to request new nodes without creating Pods. Kueue can use it to provide high guarantees that the admitted workloads will fit in the cluster.

**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [ ] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@trasc](https://github.com/trasc) — 2023-09-19T11:01:20Z

/assign

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-09-19T11:14:27Z

@trasc Could you update the issue description? I don't have any context as to why this feature is necessary.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-09-19T15:24:38Z

Sorry about that @tenzen-y. Updated the description.

There is a KEP coming. We are thinking of using the cmd/experimental folder to avoid tying this to the release of 0.5

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-09-19T15:29:09Z

/assign @mwielgus 
for design

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-09-19T16:06:46Z

> Sorry about that @tenzen-y. Updated the description.

@alculquicondor Alright. Thank you for the updates :)

> There is a KEP coming. We are thinking of using the cmd/experimental folder to avoid tying this to the release of 0.5

It makes sense. IIUC, ProvisioningRequest is not yet released.

### Comment by [@trasc](https://github.com/trasc) — 2023-10-11T06:13:32Z

/reopen
To continue tracking the implementation #1154

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-10-11T06:13:36Z

@trasc: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1136#issuecomment-1756869791):

>/reopen
>To continue tracking the implementation #1154 


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
