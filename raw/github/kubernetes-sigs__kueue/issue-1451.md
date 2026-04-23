# Issue #1451: Unable to delete pod group before admission

**Summary**: Unable to delete pod group before admission

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1451

**Last updated**: 2024-03-08T15:37:14Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@achernevskii](https://github.com/achernevskii)
- **Created**: 2023-12-13T21:03:38Z
- **Updated**: 2024-03-08T15:37:14Z
- **Closed**: 2024-03-08T15:36:52Z
- **Labels**: `kind/bug`
- **Assignees**: [@alculquicondor](https://github.com/alculquicondor)
- **Comments**: 6

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

If I create 3 pods for a pod group of size 4 and then decide to delete it, there's no way for me to manually delete pods in the group, since all of the pods contain the finalizer.

**What you expected to happen**:

If all of the pods in the group have a deletion timestamp, the group is not finished, and there's no related workload, the pods should be finalized.

**How to reproduce it (as minimally and precisely as possible)**:

1. Create 3 pods with `kueue.x-k8s.io/pod-group-total-count=4`:
   ```yaml
   apiVersion: v1
   kind: Pod
   metadata:
     generateName: kueue-sleep-
     annotations:
       kueue.x-k8s.io/pod-group-total-count: "4"
     labels:
       kueue.x-k8s.io/queue-name: user-queue
       kueue.x-k8s.io/pod-group-name: example-group
   spec:
     containers:
       - name: sleep
          image: busybox
          command:
           - sleep
         args:
           - 5m
         resources:
           requests:
             cpu: 1m
   ```

2. Delete all pods in the group:
   ```
   kubectl delete -l kueue.x-k8s.io/pod-group-name=example-group -n default
   ```

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`): v1.28.3
- Kueue version (use `git describe --tags --dirty --always`): 
- Cloud provider or hardware configuration: 
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@achernevskii](https://github.com/achernevskii) — 2023-12-13T21:03:50Z

cc @alculquicondor

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-12-13T21:13:33Z

I think if a Pod is deleted before the number of pods equals the group size and a Workload doesn't exist, we might be ok finalizing it.

### Comment by [@achernevskii](https://github.com/achernevskii) — 2023-12-14T02:35:16Z

/assign

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-03-08T15:36:48Z

/close

Fixed by https://github.com/kubernetes-sigs/kueue/pull/1573

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-03-08T15:36:53Z

@alculquicondor: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1451#issuecomment-1985910352):

>/close
>
>Fixed by https://github.com/kubernetes-sigs/kueue/pull/1573


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-03-08T15:37:11Z

/unassign @achernevskii 
/assign
