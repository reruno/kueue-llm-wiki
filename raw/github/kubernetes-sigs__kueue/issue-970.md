# Issue #970: Synchronize `batch/job.completions` with `parallelism` in case of partial admission

**Summary**: Synchronize `batch/job.completions` with `parallelism` in case of partial admission

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/970

**Last updated**: 2023-08-03T16:58:22Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@trasc](https://github.com/trasc)
- **Created**: 2023-07-11T10:08:43Z
- **Updated**: 2023-08-03T16:58:22Z
- **Closed**: 2023-08-03T16:58:22Z
- **Labels**: `kind/feature`
- **Assignees**: [@stuton](https://github.com/stuton)
- **Comments**: 6

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
Synchronize `batch/job.completions` with `parallelism` in case of partial admission
**Why is this needed**:

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@trasc](https://github.com/trasc) — 2023-07-11T10:28:24Z

#971 has a partial implementation for this, missing the k8s version check side.

For version check I see two possibilities:

1. Get the the version of the api server using client-go discovery.
2. Get the node name via downward API, get the node info from the cluster and extract the kubelet version.


With 2. we can consider the version to be the same for the full duration of the execution.
With 1. we might be required to get the version multiple times since we cannot grantee that the api-server is upadated before the kubelet managing the kueue's controller-manager.

cc: @alculquicondor

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-07-11T12:59:11Z

2 doesn't work, because the node version could be different from the control plane version. And validation happens in the control plane.

So it has to be 1. However, the API call should probably be done once at startup.

### Comment by [@trasc](https://github.com/trasc) — 2023-07-11T14:01:00Z

> 2 doesn't work, because the node version could be different from the control plane version. And validation happens in the control plane.
> 
> So it has to be 1. However, the API call should probably be done once at startup.

The problem is that there is no guarantee that the kueue's controller-manager is restarted when the control plane changes.

We could watch for nodes with `node-role.kubernetes.io/control-plane` label, and try to solve potential conflicts when multiple are present. This way we are also using the controller runtime cache.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-07-11T14:27:57Z

> We could watch for nodes with `node-role.kubernetes.io/control-plane` label, and try to solve potential conflicts when multiple are present. This way we are also using the controller runtime cache.

This is not always possible. In multiple cloud providers, the control-plane VMs are not visible in the API.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-07-11T14:45:06Z

On the other hand, a query every 10 minutes sounds like an acceptable compromise.

### Comment by [@stuton](https://github.com/stuton) — 2023-07-13T09:49:31Z

/assign
