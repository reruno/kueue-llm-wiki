# Issue #1339: Plain Pod remains in Terminating state after deleting

**Summary**: Plain Pod remains in Terminating state after deleting

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1339

**Last updated**: 2023-11-17T16:15:21Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@nstogner](https://github.com/nstogner)
- **Created**: 2023-11-16T23:59:08Z
- **Updated**: 2023-11-17T16:15:21Z
- **Closed**: 2023-11-17T16:15:21Z
- **Labels**: `kind/bug`
- **Assignees**: [@tenzen-y](https://github.com/tenzen-y)
- **Comments**: 2

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

Deleting plain Pods managed by Kueue will hang in Terminating state forever.

**What you expected to happen**:

Expected Kueue to remove finalizer eventually and allow Pod to be deleted.

**How to reproduce it (as minimally and precisely as possible)**:

Follow this guide: https://kueue.sigs.k8s.io/docs/tasks/run_plain_pods/

Delete Pod before it completes.

**Anything else we need to know?**:

Example of Pod that is hanging:

```yaml
- apiVersion: v1
  kind: Pod
  metadata:
    creationTimestamp: "2023-11-16T22:10:10Z"
    deletionGracePeriodSeconds: 0
    deletionTimestamp: "2023-11-16T22:10:29Z"
    finalizers:
    - kueue.x-k8s.io/managed
    labels:
      kueue.x-k8s.io/managed: "true"
      kueue.x-k8s.io/queue-name: xyz
    name: abc
    namespace: default
```

Did not see any errors in controller (even when raising log level to 3).

**Environment**:
- Kubernetes version (use `kubectl version`):

```
Client Version: version.Info{Major:"1", Minor:"27", GitVersion:"v1.27.4", GitCommit:"fa3d7990104d7c1f16943a67f11b154b71f6a132", GitTreeState:"clean", BuildDate:"2023-07-19T12:20:54Z", GoVersion:"go1.20.6", Compiler:"gc", Platform:"darwin/amd64"}
Kustomize Version: v5.0.1
Server Version: version.Info{Major:"1", Minor:"27", GitVersion:"v1.27.3-gke.100", GitCommit:"6466b51b762a5c49ae3fb6c2c7233ffe1c96e48c", GitTreeState:"clean", BuildDate:"2023-06-23T09:27:28Z", GoVersion:"go1.20.5 X:boringcrypto", Compiler:"gc", Platform:"linux/amd64"}
```

- Kueue version (use `git describe --tags --dirty --always`):

`0.5.0`

- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-11-17T05:40:01Z

Uhm, that makes sense. This issue is reproducible.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-11-17T05:41:19Z

/assign
