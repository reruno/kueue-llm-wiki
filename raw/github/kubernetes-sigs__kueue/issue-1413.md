# Issue #1413: Installation failed in kind cluster

**Summary**: Installation failed in kind cluster

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1413

**Last updated**: 2023-12-06T10:28:00Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kamalkraj](https://github.com/kamalkraj)
- **Created**: 2023-12-06T10:23:05Z
- **Updated**: 2023-12-06T10:28:00Z
- **Closed**: 2023-12-06T10:26:05Z
- **Labels**: `kind/support`
- **Assignees**: _none_
- **Comments**: 4

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
Installation `0.5.1` failed. `0.4.2` is installed propertly
cmd
```bash
kubectl apply -f https://github.com/kubernetes-sigs/kueue/releases/download/v0.5.0/manifests.yaml
```
```bash
namespace/kueue-system unchanged
customresourcedefinition.apiextensions.k8s.io/admissionchecks.kueue.x-k8s.io unchanged
customresourcedefinition.apiextensions.k8s.io/clusterqueues.kueue.x-k8s.io configured
customresourcedefinition.apiextensions.k8s.io/localqueues.kueue.x-k8s.io configured
customresourcedefinition.apiextensions.k8s.io/provisioningrequestconfigs.kueue.x-k8s.io unchanged
customresourcedefinition.apiextensions.k8s.io/resourceflavors.kueue.x-k8s.io configured
customresourcedefinition.apiextensions.k8s.io/workloadpriorityclasses.kueue.x-k8s.io unchanged
serviceaccount/kueue-controller-manager unchanged
role.rbac.authorization.k8s.io/kueue-leader-election-role unchanged
clusterrole.rbac.authorization.k8s.io/kueue-batch-admin-role unchanged
clusterrole.rbac.authorization.k8s.io/kueue-batch-user-role unchanged
clusterrole.rbac.authorization.k8s.io/kueue-clusterqueue-editor-role unchanged
clusterrole.rbac.authorization.k8s.io/kueue-clusterqueue-viewer-role unchanged
clusterrole.rbac.authorization.k8s.io/kueue-job-editor-role unchanged
clusterrole.rbac.authorization.k8s.io/kueue-job-viewer-role unchanged
clusterrole.rbac.authorization.k8s.io/kueue-jobset-editor-role unchanged
clusterrole.rbac.authorization.k8s.io/kueue-jobset-viewer-role unchanged
clusterrole.rbac.authorization.k8s.io/kueue-localqueue-editor-role unchanged
clusterrole.rbac.authorization.k8s.io/kueue-localqueue-viewer-role unchanged
clusterrole.rbac.authorization.k8s.io/kueue-manager-role configured
clusterrole.rbac.authorization.k8s.io/kueue-metrics-reader unchanged
clusterrole.rbac.authorization.k8s.io/kueue-mpijob-editor-role unchanged
clusterrole.rbac.authorization.k8s.io/kueue-mpijob-viewer-role unchanged
clusterrole.rbac.authorization.k8s.io/kueue-mxjob-editor-role unchanged
clusterrole.rbac.authorization.k8s.io/kueue-mxjob-viewer-role unchanged
clusterrole.rbac.authorization.k8s.io/kueue-paddlejob-editor-role unchanged
clusterrole.rbac.authorization.k8s.io/kueue-paddlejob-viewer-role unchanged
clusterrole.rbac.authorization.k8s.io/kueue-proxy-role unchanged
clusterrole.rbac.authorization.k8s.io/kueue-pytorchjob-editor-role unchanged
clusterrole.rbac.authorization.k8s.io/kueue-pytorchjob-viewer-role unchanged
clusterrole.rbac.authorization.k8s.io/kueue-rayjob-editor-role unchanged
clusterrole.rbac.authorization.k8s.io/kueue-rayjob-viewer-role unchanged
clusterrole.rbac.authorization.k8s.io/kueue-resourceflavor-editor-role unchanged
clusterrole.rbac.authorization.k8s.io/kueue-resourceflavor-viewer-role unchanged
clusterrole.rbac.authorization.k8s.io/kueue-tfjob-editor-role unchanged
clusterrole.rbac.authorization.k8s.io/kueue-tfjob-viewer-role unchanged
clusterrole.rbac.authorization.k8s.io/kueue-workload-editor-role unchanged
clusterrole.rbac.authorization.k8s.io/kueue-workload-viewer-role unchanged
clusterrole.rbac.authorization.k8s.io/kueue-xgboostjob-editor-role unchanged
clusterrole.rbac.authorization.k8s.io/kueue-xgboostjob-viewer-role unchanged
rolebinding.rbac.authorization.k8s.io/kueue-leader-election-rolebinding unchanged
clusterrolebinding.rbac.authorization.k8s.io/kueue-manager-rolebinding unchanged
clusterrolebinding.rbac.authorization.k8s.io/kueue-proxy-rolebinding unchanged
configmap/kueue-manager-config configured
secret/kueue-webhook-server-cert unchanged
service/kueue-controller-manager-metrics-service unchanged
service/kueue-webhook-service unchanged
deployment.apps/kueue-controller-manager configured
mutatingwebhookconfiguration.admissionregistration.k8s.io/kueue-mutating-webhook-configuration configured
validatingwebhookconfiguration.admissionregistration.k8s.io/kueue-validating-webhook-configuration configured
The CustomResourceDefinition "workloads.kueue.x-k8s.io" is invalid: metadata.annotations: Too long: must have at most 262144 bytes
``` 
**What you expected to happen**:
install without any error
**How to reproduce it (as minimally and precisely as possible)**:

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`): Client Version: v1.28.4 Kustomize Version: v5.0.4-0.20230601165947-6ce0bf390ce3 Server Version: v1.27.3
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration: kind local cluster,kind version 0.20.0
- OS (e.g: `cat /etc/os-release`): mac
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-12-06T10:25:23Z

@kamalkraj You can avoid the error in the following command:

```bash
kubectl apply --server-side -f https://github.com/kubernetes-sigs/kueue/releases/download/v0.5.1/manifests.yaml
```

https://kueue.sigs.k8s.io/docs/installation/#install-a-released-version

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-12-06T10:26:01Z

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-12-06T10:26:06Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1413#issuecomment-1842596178):

>/close
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-12-06T10:27:57Z

/remove-kind bug
/kind support
