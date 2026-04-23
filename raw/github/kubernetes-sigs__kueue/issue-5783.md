# Issue #5783: Add support for CronJob resources in Kueue Manifests

**Summary**: Add support for CronJob resources in Kueue Manifests

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5783

**Last updated**: 2025-08-24T19:39:52Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@ighosh98](https://github.com/ighosh98)
- **Created**: 2025-06-26T18:56:32Z
- **Updated**: 2025-08-24T19:39:52Z
- **Closed**: 2025-08-24T19:39:52Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 5

## Description

**What would you like to be added**: 
We want to allow users to have the capability to schedule CronJobs in their GKE clusters. 

**Why is this needed**:
We have a use case where we would like to schedule  a periodic job in our kubernetes cluster. For now, we made [a change in our manifest](https://github.com/GoogleCloudPlatform/cluster-toolkit/blob/develop/modules/management/kubectl-apply/manifests/kueue-v0.11.4.yaml#L11429-L11436) to support this use case but would appreciate it if Kueue can support this capability as well. 

**Completion requirements**:
Customers can schedule cronjobs on their kubernetes cluster when Kueue is installed.

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@ishitachail](https://github.com/ishitachail) — 2025-06-27T05:07:00Z

While deploying the cronjob we were getting this error
 `Warning  FailedCreate  6s (x8 over 77s)  cronjob-controller  Error creating job: Internal error occurred: failed calling webhook "mjob.kb.io": failed to call webhook: Post "https://kueue-webhook-service.kueue-system.svc:443/mutate-batch-v1-job?timeout=10s": context deadline exceeded`
```
(myproject) ishitachail@ishitachail:~/Desktop/cluster-toolkit$ kubectl get pods -n kueue-system
NAME                                        READY   STATUS    RESTARTS   AGE
kueue-controller-manager-7647678dcc-pm4pk   0/1     Pending   0          17h
kueue-controller-manager-7bfccd975c-bhdwl   1/1     Running   0          17h
```
On further debugging found the following error in logs of the pending kueue-controller-manager- pod:

```
W0623 11:00:00.257566       1 reflector.go:569] [sigs.k8s.io/controller-runtime/pkg/cache/internal/informers.go:108](http://sigs.k8s.io/controller-runtime/pkg/cache/internal/informers.go:108): failed to list *v1.PartialObjectMetadata: cronjobs.batch is forbidden: User "system:serviceaccount:kueue-system:kueue-controller-manager" cannot list resource "cronjobs" in API group "batch" at the cluster scope
E0623 11:00:00.257671       1 reflector.go:166] "Unhandled Error" err="[sigs.k8s.io/controller-runtime/pkg/cache/internal/informers.go:108](http://sigs.k8s.io/controller-runtime/pkg/cache/internal/informers.go:108): Failed to watch *v1.PartialObjectMetadata: failed to list *v1.PartialObjectMetadata: cronjobs.batch is forbidden: User \"system:serviceaccount:kueue-system:kueue-controller-manager\" cannot list resource \"cronjobs\" in API group \"batch\" at the cluster scope" logger="UnhandledError"
```

The error was due to the ServiceAccount kueue-controller-manager in the kueue-system namespace, is being denied permission by Kubernetes to list (and watch) CronJobs.

Tried ` kubectl describe clusterrole kueue-manager-role` cmd and saw that the cronjobs.batch resource is NOT listed under PolicyRule with list or watch verbs

Therefore the following permissions need to be added:
```
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  labels:
    app.kubernetes.io/component: controller
    app.kubernetes.io/name: kueue
    control-plane: controller-manager
  name: kueue-manager-role
rules:
- apiGroups:
    - batch
  resources:
    - cronjobs 
  verbs:
    - get
    - list
    - watch
```
 _The kueue-manager-role needs get, list, and watch permissions on CronJobs within the batch API group._

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-27T06:16:40Z

This looks like the issue https://github.com/kubernetes-sigs/kueue/issues/5235, it was already fixed and cherry-picked into [0.11.5](https://github.com/kubernetes-sigs/kueue/releases/tag/v0.11.5 ), so please upgrade and verify. The fix is also part of the 0.12 release line.

### Comment by [@ighosh98](https://github.com/ighosh98) — 2025-06-27T13:29:10Z

Thanks. We will try this out and update the thread

### Comment by [@kannon92](https://github.com/kannon92) — 2025-08-24T19:39:47Z

I believe this is no longer relevant.

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-08-24T19:39:52Z

@kannon92: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/5783#issuecomment-3218328593):

>I believe this is no longer relevant.
>
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
