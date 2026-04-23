# Issue #2260: MPIJobs can't run with ProvisioningRequest with DWS

**Summary**: MPIJobs can't run with ProvisioningRequest with DWS

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2260

**Last updated**: 2024-05-27T06:52:34Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2024-05-22T17:20:59Z
- **Updated**: 2024-05-27T06:52:34Z
- **Closed**: 2024-05-27T06:52:34Z
- **Labels**: `kind/bug`, `priority/important-soon`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 5

## Description

**What happened**:

For DWS, we use the following configuration:

```yaml
apiVersion: kueue.x-k8s.io/v1beta1
kind: ProvisioningRequestConfig
metadata:
  name: dws-config
spec:
  provisioningClassName: queued-provisioning.gke.io
  managedResources:
  - nvidia.com/gpu
```

This allows to create a ProvReq only for the workers of an MPIJob, but not the launcher.

However, when the ProvisioningRequest is satisfied, the Kueue provisioning controller only sets a `podSetUpdate` for the podset used in the provisioningRequest. This fails validation for the Workload status.

**What you expected to happen**:

Validation should pass for cases where `podSetUpdates` has less elements than `.spec.podSets` and the logic that handles the updates should not expect the slices to match.

**How to reproduce it (as minimally and precisely as possible)**:

- Configure a cluster using https://cloud.google.com/kubernetes-engine/docs/how-to/provisioningrequest#for_jobs_with_kueue
- Create an MPIJob where the workers requests GPUs, but the launcher doesn't.

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-22T17:21:06Z

/assign @trasc

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-22T17:47:03Z

/priority important-soon

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-05-24T18:38:35Z

If you get this issue from your customers, I think you can tell them `runLauncherAsWorker` as a temporary fix.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-24T19:47:37Z

That won't work either. Currently ProvisioningRequest only supports one podset.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-05-24T19:50:49Z

> That won't work either. Currently ProvisioningRequest only supports one podset.

Oh, I see...
