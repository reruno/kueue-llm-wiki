# Issue #1401: Flaky: Provisioning when A workload is using a provision admission check with retry Should retry when ProvisioningRequestConfig has MaxRetries=2, the succeeded if the second Provisioning request succeeds

**Summary**: Flaky: Provisioning when A workload is using a provision admission check with retry Should retry when ProvisioningRequestConfig has MaxRetries=2, the succeeded if the second Provisioning request succeeds

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1401

**Last updated**: 2024-01-16T09:09:14Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2023-12-04T23:36:26Z
- **Updated**: 2024-01-16T09:09:14Z
- **Closed**: 2024-01-16T09:09:14Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mimowo](https://github.com/mimowo)
- **Comments**: 7

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

Failed "Provisioning admission check suite: [It] Provisioning when A workload is using a provision admission check with retry Should retry when ProvisioningRequestConfig has MaxRetries=2, the succeeded if the second Provisioning request succeeds"

**What you expected to happen**:

No error wouldn't happen

**How to reproduce it (as minimally and precisely as possible)**:
https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/1400/pull-kueue-test-integration-main/1731815899859521536

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-12-04T23:37:49Z

/kind flake

### Comment by [@kaisoz](https://github.com/kaisoz) — 2024-01-10T08:31:39Z

/assign

 I'll give it a chance @mimowo

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-01-10T10:32:01Z

/assign @kaisoz

### Comment by [@mimowo](https://github.com/mimowo) — 2024-01-15T14:26:06Z

I think this is the same issue as in https://github.com/kubernetes-sigs/kueue/issues/1558. In the logs we have actually as much as 3 instances of attempt 2 PR being created:

```
  2023-12-04T23:23:54.00071857Z	LEVEL(-3)	provisioning/controller.go:245	Creating ProvisioningRequest	{"controller": "workload", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Workload", "Workload": {"name":"wl","namespace":"provisioning-nn7mz"}, "namespace": "provisioning-nn7mz", "name": "wl", "reconcileID": "30543f86-67a3-4c84-b985-014e37cb24dd", "requestName": "wl-ac-prov-2", "attempt": 2}
  [1mSTEP:[0m Setting the provision request-2 as Provisioned [38;5;243m@ 12/04/23 23:23:54.006[0m
  2023-12-04T23:23:54.012068015Z	LEVEL(-3)	provisioning/controller.go:468	Synchronizing admission check state based on provisioning request	{"controller": "workload", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Workload", "Workload": {"name":"wl","namespace":"provisioning-nn7mz"}, "namespace": "provisioning-nn7mz", "name": "wl", "reconcileID": "30543f86-67a3-4c84-b985-014e37cb24dd", "wl": {"name":"wl","namespace":"provisioning-nn7mz"}, "check": "ac-prov", "prName": "wl-ac-prov-2", "failed": false, "accepted": false, "available": false}
  2023-12-04T23:23:54.012217006Z	LEVEL(-2)	provisioning/controller.go:103	Reconcile workload	{"controller": "workload", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Workload", "Workload": {"name":"wl","namespace":"provisioning-nn7mz"}, "namespace": "provisioning-nn7mz", "name": "wl", "reconcileID": "13aaf036-6760-4140-9309-d6080767f115"}
  [1mSTEP:[0m Checking the admission check is ready [38;5;243m@ 12/04/23 23:23:54.014[0m
  2023-12-04T23:23:54.018554812Z	LEVEL(-3)	provisioning/controller.go:245	Creating ProvisioningRequest	{"controller": "workload", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Workload", "Workload": {"name":"wl","namespace":"provisioning-nn7mz"}, "namespace": "provisioning-nn7mz", "name": "wl", "reconcileID": "13aaf036-6760-4140-9309-d6080767f115", "requestName": "wl-ac-prov-2", "attempt": 2}
  2023-12-04T23:23:54.026303246Z	LEVEL(-3)	provisioning/controller.go:468	Synchronizing admission check state based on provisioning request	{"controller": "workload", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Workload", "Workload": {"name":"wl","namespace":"provisioning-nn7mz"}, "namespace": "provisioning-nn7mz", "name": "wl", "reconcileID": "13aaf036-6760-4140-9309-d6080767f115", "wl": {"name":"wl","namespace":"provisioning-nn7mz"}, "check": "ac-prov", "prName": "wl-ac-prov-2", "failed": false, "accepted": false, "available": false}
  2023-12-04T23:23:54.026432107Z	LEVEL(-2)	provisioning/controller.go:103	Reconcile workload	{"controller": "workload", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Workload", "Workload": {"name":"wl","namespace":"provisioning-nn7mz"}, "namespace": "provisioning-nn7mz", "name": "wl", "reconcileID": "bb7b759a-5452-4642-9e05-f6a798ebe352"}
  2023-12-04T23:23:54.032374931Z	LEVEL(-3)	provisioning/controller.go:245	Creating ProvisioningRequest	{"controller": "workload", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Workload", "Workload": {"name":"wl","namespace":"provisioning-nn7mz"}, "namespace": "provisioning-nn7mz", "name": "wl", "reconcileID": "bb7b759a-5452-4642-9e05-f6a798ebe352", "requestName": "wl-ac-prov-2", "attempt": 2}
```

### Comment by [@mimowo](https://github.com/mimowo) — 2024-01-15T14:28:56Z

/assign 
I intend to work on the fix since it appears a bug (affecting prodution use, not just tests) in the logic I'm familiar with, if you don't mind @kaisoz

### Comment by [@kaisoz](https://github.com/kaisoz) — 2024-01-15T15:28:11Z

> /assign I intend to work on the fix since it appears a bug (affecting prodution use, not just tests) in the logic I'm familiar with, if you don't mind @kaisoz

Sure! Makes all the sense @mimowo

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-01-15T15:45:33Z

/unassign @kaisoz
