# Issue #564: Failed to watch *v1.RuntimeClass

**Summary**: Failed to watch *v1.RuntimeClass

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/564

**Last updated**: 2023-02-14T20:08:05Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@jaym](https://github.com/jaym)
- **Created**: 2023-02-14T19:37:27Z
- **Updated**: 2023-02-14T20:08:05Z
- **Closed**: 2023-02-14T20:03:54Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 3

## Description

**What happened**:
When using GKE with sandboxed nodes, and attempting to schedule into a gvisor sandbox using `runtimeClassName=gvisor`, kueue starts reporting this error every 30 seconds:
```
"pkg/mod/k8s.io/client-go@v0.25.6/tools/cache/reflector.go:169: Failed to watch *v1.RuntimeClass: unknown (get runtimeclasses.node.k8s.io)"
```

**What you expected to happen**:
That error not to be printed

**How to reproduce it (as minimally and precisely as possible)**:
Create a job with `runtimeClassName` set to `gvisor` on a GKE cluster with a sandboxed node.

**Anything else we need to know?**:
Applying this manifest fixes things up:
```
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: kueue-manager-role-runtimeclass
rules:
- apiGroups:
  - node.k8s.io
  resources:
  - runtimeclasses
  verbs:
  - get
  - list
  - watch
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: kueue-manager-rolebinding-runtimeclass
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: kueue-manager-role-runtimeclass
subjects:
- kind: ServiceAccount
  name: kueue-controller-manager
  namespace: kueue-system
```

**Environment**:
- Kubernetes version (use `kubectl version`):
  ```
  Server Version: version.Info{Major:"1", Minor:"24", GitVersion:"v1.24.7-gke.900", GitCommit:"e35c4457f66187eff006dda6d2c0fe12144ef2ec", GitTreeState:"clean", BuildDate:"2022-10-26T09:25:34Z", GoVersion:"go1.18.7b7", Compiler:"gc", Platform:"linux/amd64"}
  ```
- Kueue version (use `git describe --tags --dirty --always`): `v0.3.0-devel-253-g2d3f81a`. Also happens on the released `v0.2.1`
- Cloud provider or hardware configuration:
  - GKE with Sandboxed node

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-02-14T19:43:44Z

Oh, yes, kueue needs to calculate the overhead of the RuntimeClass https://github.com/kubernetes-sigs/kueue/blob/8d06aa419af0a9e4add6e11f398e55961d0979e4/pkg/controller/core/workload_controller.go#L411

I think we just missed watch here:
https://github.com/kubernetes-sigs/kueue/blob/8d06aa419af0a9e4add6e11f398e55961d0979e4/pkg/controller/core/workload_controller.go#L125

This is the kind of issues that don't show up in integration tests, but we can't test this in `kind` E2E tests either :(

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-02-14T20:05:19Z

Thanks for the report! It's fixed in the main branch now.

We were not thinking on another 0.2 release for now, as we are focusing on 0.3. But if you find other problems please let us know and we can prioritize another release.

### Comment by [@jaym](https://github.com/jaym) — 2023-02-14T20:08:04Z

Thanks for the quick fix. I ended up switching to the main branch for now as it has other bug fixes I wanted
