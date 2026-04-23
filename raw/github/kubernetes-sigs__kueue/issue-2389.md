# Issue #2389: ProvisioningRequestNotSchedulableInNodepool for Pod with Generic Ephemeral Volume

**Summary**: ProvisioningRequestNotSchedulableInNodepool for Pod with Generic Ephemeral Volume

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2389

**Last updated**: 2025-03-06T12:40:00Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mruoss](https://github.com/mruoss)
- **Created**: 2024-06-10T13:52:18Z
- **Updated**: 2025-03-06T12:40:00Z
- **Closed**: 2024-06-25T21:16:20Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 4

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->

**What happened**:

We are using Kueue with GKE's [Dynamic Workload Scheduler](https://cloud.google.com/kubernetes-engine/docs/how-to/provisioningrequest). It works great but as soon as we try to attach a [generic ephemeral volume](https://cloud.google.com/kubernetes-engine/docs/how-to/provisioningrequest) to the pod, it won't get provisioned anymore.

Workload and a provisioning request are created. However, after a while, the provisioning request is marked as failed. Its status looks as follows. Note the error message `Provisioning Request's pods cannot be scheduled in the nodepool, affected nodepools: **REDACTED_LIST_OF_NODEPOOLS**`. 

```
Status:
  Conditions:
    Last Transition Time:  2024-06-10T11:17:32Z
    Message:               Provisioning Request wasn't accepted.
    Observed Generation:   1
    Reason:                NotAccepted
    Status:                False
    Type:                  Accepted
    Last Transition Time:  2024-06-10T11:17:32Z
    Message:               Provisioning Request wasn't provisioned.
    Observed Generation:   1
    Reason:                NotProvisioned
    Status:                False
    Type:                  Provisioned
    Last Transition Time:  2024-06-10T11:19:32Z
    Message:               Provisioning Request's pods cannot be scheduled in the nodepool, affected nodepools: **REDACTED_LIST_OF_NODEPOOLS**
    Observed Generation:   1
    Reason:                ProvisioningRequestNotSchedulableInNodepool
    Status:                True
    Type:                  Failed
Events:                    <none>
```

**What you expected to happen**:

If I remove the volume or create a PVC and replace the volume declaration with something like the following, a node gets provisioned and the pod gets scheduled. I would expect the same behaviour for pods with generic ephemeral volumes.

```yaml
volumes:
  - name: tmp-fs
    persistentVolumeClaim:
      claimName: myclaim
```

**How to reproduce it (as minimally and precisely as possible)**:

This is the Pod we're trying to get scheduled on a fresh `nvidia-l4` machine:

```yml
apiVersion: v1
kind: Pod
metadata:
  labels:
    kueue.x-k8s.io/queue-name: dws-local-queue
  name: kueue-test
  namespace: development
spec:
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: cloud.google.com/gke-accelerator
            operator: In
            values:
            - nvidia-l4
  containers:
  - name: main-container
    image: ubuntu:latest
    command: [ "/bin/bash", "-c", "--" ]
    args: [ "while true; do sleep 30; done;" ]
    resources:
      limits:
        cpu: "4"
        memory: 32Gi
        nvidia.com/gpu: "1"
      requests:
        cpu: "4"
        memory: 32Gi
        nvidia.com/gpu: "1"
    volumeMounts:
    - mountPath: /tmp
      name: tmp-fs
  tolerations:
  - effect: NoSchedule
    key: nvidia.com/gpu
    operator: Exists
  - effect: NoSchedule
    key: cloud.google.com/gke-queued
    operator: Equal
    value: "true"
  volumes:
  - name: tmp-fs
    ephemeral:
      volumeClaimTemplate:
        spec:
          accessModes:
          - ReadWriteOnce
          resources:
            requests:
              storage: 32Gi
          storageClassName: my-job-ephemeral-storage
          volumeMode: Filesystem
```

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`): `v1.29.4-gke.1043002`
- Kueue version (use `git describe --tags --dirty --always`): `v0.6.2`
- Cloud provider or hardware configuration: 
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@trasc](https://github.com/trasc) — 2024-06-11T06:17:30Z

This looks to be related to [cluster-autoscaler/provisioningrequest](https://github.com/kubernetes/autoscaler/tree/master/cluster-autoscaler/provisioningrequest).

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-06-25T21:16:16Z

Hi @mruoss, indeed Kueue is not responsible for satisfying the ProvisioningRequest.

In addition to the issue in cluster-autoscaler, I would suggest you reach out to your Google Cloud representative to file a feature request.

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-06-25T21:16:21Z

@alculquicondor: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/2389#issuecomment-2189984200):

>Hi @mruoss, indeed Kueue is not responsible for satisfying the ProvisioningRequest.
>
>In addition to the issue in cluster-autoscaler, I would suggest you reach out to your Google Cloud representative to file a feature request.
>
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mruoss](https://github.com/mruoss) — 2025-03-06T12:39:59Z

Some additional info: Here's the storageClass resource:

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: my-job-ephemeral-storage
allowVolumeExpansion: true
parameters:
  type: pd-ssd
  csi.storage.k8s.io/fstype: ext4
provisioner: pd.csi.storage.gke.io
reclaimPolicy: Delete
volumeBindingMode: WaitForFirstConsumer
```
