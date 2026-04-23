# Issue #1769: Kueue 0.6.0 blocks deletion of namespaces

**Summary**: Kueue 0.6.0 blocks deletion of namespaces

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1769

**Last updated**: 2024-02-28T19:21:02Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@dgrove-oss](https://github.com/dgrove-oss)
- **Created**: 2024-02-26T15:50:08Z
- **Updated**: 2024-02-28T19:21:02Z
- **Closed**: 2024-02-28T19:21:00Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 5

## Description

**What happened**:

With kueue 0.6.0 deployed on a cluster, deletion of namespaces hangs.  
This is a regression from kueue 0.5.3 and from the conditions on the namespace being deleted 
seems to be related to the visibility changes introduced in kueue 0.6.0.

In more detail, I created a Kubernetes 1.27 cluster running on kind 0.19.  
I deployed Kueue 0.6.0 and then created and attempted to delete a namespace.
Deletion of the namespace hangs.

**What you expected to happen**:

I expect the namespace to be deleted successfully.

**How to reproduce it (as minimally and precisely as possible)**:
See transcript below:
```
dgrove@Dave's IBM Mac appwrapper % kind create cluster 
Creating cluster "kind" ...
 ✓ Ensuring node image (kindest/node:v1.27.1) 🖼
 ✓ Preparing nodes 📦  
 ✓ Writing configuration 📜 
 ✓ Starting control-plane 🕹️ 
 ✓ Installing CNI 🔌 
 ✓ Installing StorageClass 💾 
Set kubectl context to "kind-kind"
You can now use your cluster with:

kubectl cluster-info --context kind-kind

Not sure what to do next? 😅  Check out https://kind.sigs.k8s.io/docs/user/quick-start/
dgrove@Dave's IBM Mac appwrapper % kubectl apply --server-side -f https://github.com/kubernetes-sigs/kueue/releases/download/v0.6.0/manifests.yaml
namespace/kueue-system serverside-applied
customresourcedefinition.apiextensions.k8s.io/admissionchecks.kueue.x-k8s.io serverside-applied
customresourcedefinition.apiextensions.k8s.io/clusterqueues.kueue.x-k8s.io serverside-applied
customresourcedefinition.apiextensions.k8s.io/localqueues.kueue.x-k8s.io serverside-applied
customresourcedefinition.apiextensions.k8s.io/multikueueclusters.kueue.x-k8s.io serverside-applied
customresourcedefinition.apiextensions.k8s.io/multikueueconfigs.kueue.x-k8s.io serverside-applied
customresourcedefinition.apiextensions.k8s.io/provisioningrequestconfigs.kueue.x-k8s.io serverside-applied
customresourcedefinition.apiextensions.k8s.io/resourceflavors.kueue.x-k8s.io serverside-applied
customresourcedefinition.apiextensions.k8s.io/workloadpriorityclasses.kueue.x-k8s.io serverside-applied
customresourcedefinition.apiextensions.k8s.io/workloads.kueue.x-k8s.io serverside-applied
serviceaccount/kueue-controller-manager serverside-applied
role.rbac.authorization.k8s.io/kueue-leader-election-role serverside-applied
clusterrole.rbac.authorization.k8s.io/kueue-batch-admin-role serverside-applied
clusterrole.rbac.authorization.k8s.io/kueue-batch-user-role serverside-applied
clusterrole.rbac.authorization.k8s.io/kueue-clusterqueue-editor-role serverside-applied
clusterrole.rbac.authorization.k8s.io/kueue-clusterqueue-viewer-role serverside-applied
clusterrole.rbac.authorization.k8s.io/kueue-job-editor-role serverside-applied
clusterrole.rbac.authorization.k8s.io/kueue-job-viewer-role serverside-applied
clusterrole.rbac.authorization.k8s.io/kueue-jobset-editor-role serverside-applied
clusterrole.rbac.authorization.k8s.io/kueue-jobset-viewer-role serverside-applied
clusterrole.rbac.authorization.k8s.io/kueue-localqueue-editor-role serverside-applied
clusterrole.rbac.authorization.k8s.io/kueue-localqueue-viewer-role serverside-applied
clusterrole.rbac.authorization.k8s.io/kueue-manager-role serverside-applied
clusterrole.rbac.authorization.k8s.io/kueue-metrics-reader serverside-applied
clusterrole.rbac.authorization.k8s.io/kueue-mpijob-editor-role serverside-applied
clusterrole.rbac.authorization.k8s.io/kueue-mpijob-viewer-role serverside-applied
clusterrole.rbac.authorization.k8s.io/kueue-mxjob-editor-role serverside-applied
clusterrole.rbac.authorization.k8s.io/kueue-mxjob-viewer-role serverside-applied
clusterrole.rbac.authorization.k8s.io/kueue-paddlejob-editor-role serverside-applied
clusterrole.rbac.authorization.k8s.io/kueue-paddlejob-viewer-role serverside-applied
clusterrole.rbac.authorization.k8s.io/kueue-pending-workloads-cq-viewer-role serverside-applied
clusterrole.rbac.authorization.k8s.io/kueue-pending-workloads-lq-viewer-role serverside-applied
clusterrole.rbac.authorization.k8s.io/kueue-proxy-role serverside-applied
clusterrole.rbac.authorization.k8s.io/kueue-pytorchjob-editor-role serverside-applied
clusterrole.rbac.authorization.k8s.io/kueue-pytorchjob-viewer-role serverside-applied
clusterrole.rbac.authorization.k8s.io/kueue-rayjob-editor-role serverside-applied
clusterrole.rbac.authorization.k8s.io/kueue-rayjob-viewer-role serverside-applied
clusterrole.rbac.authorization.k8s.io/kueue-resourceflavor-editor-role serverside-applied
clusterrole.rbac.authorization.k8s.io/kueue-resourceflavor-viewer-role serverside-applied
clusterrole.rbac.authorization.k8s.io/kueue-tfjob-editor-role serverside-applied
clusterrole.rbac.authorization.k8s.io/kueue-tfjob-viewer-role serverside-applied
clusterrole.rbac.authorization.k8s.io/kueue-workload-editor-role serverside-applied
clusterrole.rbac.authorization.k8s.io/kueue-workload-viewer-role serverside-applied
clusterrole.rbac.authorization.k8s.io/kueue-xgboostjob-editor-role serverside-applied
clusterrole.rbac.authorization.k8s.io/kueue-xgboostjob-viewer-role serverside-applied
rolebinding.rbac.authorization.k8s.io/kueue-visibility-server-auth-reader serverside-applied
rolebinding.rbac.authorization.k8s.io/kueue-leader-election-rolebinding serverside-applied
clusterrolebinding.rbac.authorization.k8s.io/kueue-manager-rolebinding serverside-applied
clusterrolebinding.rbac.authorization.k8s.io/kueue-proxy-rolebinding serverside-applied
configmap/kueue-manager-config serverside-applied
secret/kueue-webhook-server-cert serverside-applied
service/kueue-controller-manager-metrics-service serverside-applied
service/kueue-visibility-server serverside-applied
service/kueue-webhook-service serverside-applied
deployment.apps/kueue-controller-manager serverside-applied
apiservice.apiregistration.k8s.io/v1alpha1.visibility.kueue.x-k8s.io serverside-applied
mutatingwebhookconfiguration.admissionregistration.k8s.io/kueue-mutating-webhook-configuration serverside-applied
validatingwebhookconfiguration.admissionregistration.k8s.io/kueue-validating-webhook-configuration serverside-applied
dgrove@Dave's IBM Mac appwrapper % kubectl create ns test
namespace/test created
dgrove@Dave's IBM Mac appwrapper % kubectl get ns 
NAME                 STATUS   AGE
default              Active   2m31s
kube-node-lease      Active   2m31s
kube-public          Active   2m31s
kube-system          Active   2m31s
kueue-system         Active   69s
local-path-storage   Active   2m27s
test                 Active   5s
dgrove@Dave's IBM Mac appwrapper % kubectl delete ns test 
namespace "test" deleted
```

The `kubectl delete` command hangs and the namespace is stuck in the Terminating state.  Details below:
```
dgrove@Dave's IBM Mac appwrapper % kubectl get ns test -o yaml 
apiVersion: v1
kind: Namespace
metadata:
  creationTimestamp: "2024-02-26T15:39:56Z"
  deletionTimestamp: "2024-02-26T15:40:10Z"
  labels:
    kubernetes.io/metadata.name: test
  name: test
  resourceVersion: "874"
  uid: feeae601-b014-461b-90d3-7725b4ef8608
spec:
  finalizers:
  - kubernetes
status:
  conditions:
  - lastTransitionTime: "2024-02-26T15:40:15Z"
    message: 'Discovery failed for some groups, 1 failing: unable to retrieve the
      complete list of server APIs: visibility.kueue.x-k8s.io/v1alpha1: stale GroupVersion
      discovery: visibility.kueue.x-k8s.io/v1alpha1'
    reason: DiscoveryFailed
    status: "True"
    type: NamespaceDeletionDiscoveryFailure
  - lastTransitionTime: "2024-02-26T15:40:15Z"
    message: All legacy kube types successfully parsed
    reason: ParsedGroupVersions
    status: "False"
    type: NamespaceDeletionGroupVersionParsingFailure
  - lastTransitionTime: "2024-02-26T15:40:15Z"
    message: All content successfully deleted, may be waiting on finalization
    reason: ContentDeleted
    status: "False"
    type: NamespaceDeletionContentFailure
  - lastTransitionTime: "2024-02-26T15:40:15Z"
    message: All content successfully removed
    reason: ContentRemoved
    status: "False"
    type: NamespaceContentRemaining
  - lastTransitionTime: "2024-02-26T15:40:15Z"
    message: All content-preserving finalizers finished
    reason: ContentHasNoFinalizers
    status: "False"
    type: NamespaceFinalizersRemaining
  phase: Terminating
```
**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`): 1.27.1
- Kueue version (use `git describe --tags --dirty --always`): 0.6.0 installed from release manifest
- Cloud provider or hardware configuration: kind 0.19 on macOS/arm64
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@astefanutti](https://github.com/astefanutti) — 2024-02-27T08:09:14Z

I think it's been fixed already in main with #1746, and should be fixed in v0.6.1 with #1764. 

Adding the `--feature-gates=VisibilityOnDemand=true` option to the Kueue deployment main container command should work around the issue in the meantime.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-02-27T18:39:11Z

> I think it's been fixed already in main with #1746, and should be fixed in v0.6.1 with #1764.
> 
> Adding the `--feature-gates=VisibilityOnDemand=true` option to the Kueue deployment main container command should work around the issue in the meantime.

Yeah, I believe so, too. 
@dgrove-oss Could you try to use manifests in the release-0.6 branch if we can avoid this issue?

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2024-02-28T18:20:39Z

I tested building from source on the release-0.6 branch (80adb72b) and confirmed that the issue is resolved.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-02-28T19:20:56Z

> I tested building from source on the release-0.6 branch ([80adb72](https://github.com/kubernetes-sigs/kueue/commit/80adb72ba5553e21fc9b43269fd231a256cd4c7a)) and confirmed that the issue is resolved.

Thanks for your confirmation! This is just a tip: you could also use the latest release-0.6 image using the following tags without building:

https://github.com/kubernetes-sigs/kueue/blob/80adb72ba5553e21fc9b43269fd231a256cd4c7a/config/components/manager/kustomization.yaml#L19-L20

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-02-28T19:21:00Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1769#issuecomment-1969685594):

>> I tested building from source on the release-0.6 branch ([80adb72](https://github.com/kubernetes-sigs/kueue/commit/80adb72ba5553e21fc9b43269fd231a256cd4c7a)) and confirmed that the issue is resolved.
>
>Thanks for your confirmation! This is just a tip: you could also use the latest release-0.6 image using the following tags without building:
>
>https://github.com/kubernetes-sigs/kueue/blob/80adb72ba5553e21fc9b43269fd231a256cd4c7a/config/components/manager/kustomization.yaml#L19-L20
>
>/close
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
