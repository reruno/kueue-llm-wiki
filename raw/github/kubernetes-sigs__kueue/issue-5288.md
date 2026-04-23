# Issue #5288: Kueue installation lacks permission to watch CronJobs

**Summary**: Kueue installation lacks permission to watch CronJobs

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5288

**Last updated**: 2025-06-04T07:45:27Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@planetA](https://github.com/planetA)
- **Created**: 2025-05-19T17:29:36Z
- **Updated**: 2025-06-04T07:45:27Z
- **Closed**: 2025-06-04T07:45:26Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 8

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

When submitting CronJobs, Kueue controller lacks permissions to handle them

**What you expected to happen**:

CronJobs must have Pods created

**How to reproduce it (as minimally and precisely as possible)**:


When I create a simple kind-base setup, submitted CronJobs do not work.

```
kind create cluster 
helm install kueue oci://registry.k8s.io/kueue/charts/kueue \
    --version=0.11.4 \
    --namespace  kueue-system \
    --create-namespace \
   --wait --timeout 300s
```

Submitted Job

```
apiVersion: batch/v1
kind: CronJob
metadata:
  name: hello
spec:
  schedule: "* * * * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: hello
            image: busybox:1.28
            imagePullPolicy: IfNotPresent
            command:
            - /bin/sh
            - -c
            - date; echo Hello from the Kubernetes cluster
          restartPolicy: OnFailure
```

I see following errors in the controller:

```
kubectl logs -n kueue-system --follow kueue-controller-manager-7b78c4484f-hlpqp
....
E0519 17:16:09.408870       1 reflector.go:166] "Unhandled Error" err="sigs.k8s.io/controller-runtime/pkg/cache/internal/informers.go:108: Failed to watch *v1.PartialObjectMetadata: failed to list *v1.PartialObjectMetadata: cronjobs.batch is forbidden: User \"system:serviceaccount:kueue-system:kueue-controller-manager\" cannot list resource \"cronjobs\" in API group \"batch\" at the cluster scope" logger="UnhandledError"
W0519 17:16:20.548892       1 reflector.go:569] sigs.k8s.io/controller-runtime/pkg/cache/internal/informers.go:108: failed to list *v1.PartialObjectMetadata: cronjobs.batch is forbidden: User "system:serviceaccount:kueue-system:kueue-controller-manager" cannot list resource "cronjobs" in API group "batch" at the cluster scope
E0519 17:16:20.548966       1 reflector.go:166] "Unhandled Error" err="sigs.k8s.io/controller-runtime/pkg/cache/internal/informers.go:108: Failed to watch *v1.PartialObjectMetadata: failed to list *v1.PartialObjectMetadata: cronjobs.batch is forbidden: User \"system:serviceaccount:kueue-system:kueue-controller-manager\" cannot list resource \"cronjobs\" in API group \"batch\" at the cluster scope" logger="UnhandledError"
W0519 17:16:36.654443       1 reflector.go:569] sigs.k8s.io/controller-runtime/pkg/cache/internal/informers.go:108: failed to list *v1.PartialObjectMetadata: cronjobs.batch is forbidden: User "system:serviceaccount:kueue-system:kueue-controller-manager" cannot list resource "cronjobs" in API group "batch" at the cluster scope
E0519 17:16:36.654509       1 reflector.go:166] "Unhandled Error" err="sigs.k8s.io/controller-runtime/pkg/cache/internal/informers.go:108: Failed to watch *v1.PartialObjectMetadata: failed to list *v1.PartialObjectMetadata: cronjobs.batch is forbidden: User \"system:serviceaccount:kueue-system:kueue-controller-manager\" cannot list resource \"cronjobs\" in API group \"batch\" at the cluster scope" logger="UnhandledError"
```

**Anything else we need to know?**:

There is a workaround. If I apply following config, Kueue works as expected:

```
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: kueue-cronjob-access
rules:
- apiGroups: ["batch"]
  resources: ["cronjobs"]
  verbs: ["list", "watch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: kueue-cronjob-access-binding
subjects:
- kind: ServiceAccount
  name: kueue-controller-manager
  namespace: kueue-system
roleRef:
  kind: ClusterRole
  name: kueue-cronjob-access
  apiGroup: rbac.authorization.k8s.io
```

**Environment**:
- Kubernetes version (use `kubectl version`):
```
kubectl version
Client Version: v1.33.0
Kustomize Version: v5.6.0
Server Version: v1.32.2
```
- Kueue version (use `git describe --tags --dirty --always`): 0.11.4
- Cloud provider or hardware configuration: kind cluster

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2025-05-19T17:56:09Z

There is a bug in the latest release of Kueue.

There is a fix in main/release-0.11 but there has not been a release for this yet.

When v0.11.5 is released, I think this bug will be resolved.

cc @mimowo @tenzen-y

### Comment by [@kannon92](https://github.com/kannon92) — 2025-05-19T17:56:37Z

https://github.com/kubernetes-sigs/kueue/issues/5235

### Comment by [@kannon92](https://github.com/kannon92) — 2025-05-19T17:57:24Z

https://github.com/kubernetes-sigs/kueue/issues/5233#issuecomment-2891174850

Potentially tomorrow actually.

### Comment by [@planetA](https://github.com/planetA) — 2025-05-19T17:59:04Z

Thanks for quick response :)

Would this fix make Kueue ignore CronJobs, or would it enable it to handle CronJobs?

### Comment by [@kannon92](https://github.com/kannon92) — 2025-05-19T19:55:45Z

> Thanks for quick response :)
> 
> Would this fix make Kueue ignore CronJobs, or would it enable it to handle CronJobs?

Kueue can manage CronJobs because Kueue already manages Jobs. So I would wait for new patch release and test again. All should be good.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-20T05:08:54Z

Thank you for reporting that. Yes, https://github.com/kubernetes-sigs/kueue/issues/5235 will fix your problem.
You can check with `kubectl -k https://github.com/kubernetes-sigs/kueue/releases/download/v0.12.0-rc.1/manifests.yaml` if the fixes are your expected one.

Note that RC is a very experimental version. So, you should avoid to install it to your production.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-06-02T16:09:38Z

0.11.5 was released so this should be fixed. @planetA would you be able to confirm this update fixes your usecase?

### Comment by [@planetA](https://github.com/planetA) — 2025-06-04T07:45:26Z

Thank you. It works.
