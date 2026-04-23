# Issue #1558: Flaky Provisioning Request integration test

**Summary**: Flaky Provisioning Request integration test

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1558

**Last updated**: 2024-01-16T09:09:14Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2024-01-08T20:00:11Z
- **Updated**: 2024-01-16T09:09:14Z
- **Closed**: 2024-01-16T09:09:14Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mimowo](https://github.com/mimowo)
- **Comments**: 8

## Description

**What happened**:

Flaky test:

`Provisioning when A workload is using a provision admission check with retry Should retry when ProvisioningRequestConfig has MaxRetries>o, and every Provisioning request retry fails`

**How to reproduce it (as minimally and precisely as possible)**:

https://prow.k8s.io/view/gs/kubernetes-jenkins/logs/periodic-kueue-test-integration-main/1743668546505805824

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

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-01-08T20:01:39Z

/assign @mimowo
as author of #1351

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-01-09T00:02:01Z

/kind flake

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-01-09T00:03:10Z

/kind flake

### Comment by [@mimowo](https://github.com/mimowo) — 2024-01-15T13:40:25Z

ack

### Comment by [@mimowo](https://github.com/mimowo) — 2024-01-15T14:23:34Z

What looks in the logs wrong is that we have `wl-ac-prov-2` created twice. 

```
  2024-01-06T16:21:53.032984104Z	LEVEL(-3)	provisioning/controller.go:254	Creating ProvisioningRequest	{"controller": "workload", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Workload", "Workload": {"name":"wl","namespace":"provisioning-x5dvq"}, "namespace": "provisioning-x5dvq", "name": "wl", "reconcileID": "32d21a68-adb6-4615-8554-9521d3fddb7d", "requestName": "wl-ac-prov-2", "attempt": 2}
  2024-01-06T16:21:53.03908014Z	DEBUG	events	recorder/recorder.go:104	Created ProvisioningRequest: "wl-ac-prov-2"	{"type": "Normal", "object": {"kind":"Workload","namespace":"provisioning-x5dvq","name":"wl","uid":"207f9e17-41b5-463c-bc75-2d16e60db4a5","apiVersion":"kueue.x-k8s.io/v1beta1","resourceVersion":"397"}, "reason": "ProvisioningRequestCreated"}
  [1mSTEP:[0m Checking the admission check is rejected [38;5;243m@ 01/06/24 16:21:53.143[0m
  2024-01-06T16:21:53.154982982Z	LEVEL(-3)	provisioning/controller.go:478	Synchronizing admission check state based on provisioning request	{"controller": "workload", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Workload", "Workload": {"name":"wl","namespace":"provisioning-x5dvq"}, "namespace": "provisioning-x5dvq", "name": "wl", "reconcileID": "32d21a68-adb6-4615-8554-9521d3fddb7d", "wl": {"name":"wl","namespace":"provisioning-x5dvq"}, "check": "ac-prov", "prName": "wl-ac-prov-2", "failed": false, "accepted": false, "available": false}
  2024-01-06T16:21:53.155233353Z	LEVEL(-2)	provisioning/controller.go:112	Reconcile workload	{"controller": "workload", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Workload", "Workload": {"name":"wl","namespace":"provisioning-x5dvq"}, "namespace": "provisioning-x5dvq", "name": "wl", "reconcileID": "aa93259d-90c0-4751-b0c6-9f8cf9daa25e"}
  2024-01-06T16:21:53.24526822Z	LEVEL(-3)	provisioning/controller.go:254	Creating ProvisioningRequest	{"controller": "workload", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Workload", "Workload": {"name":"wl","namespace":"provisioning-x5dvq"}, "namespace": "provisioning-x5dvq", "name": "wl", "reconcileID": "aa93259d-90c0-4751-b0c6-9f8cf9daa25e", "requestName": "wl-ac-prov-2", "attempt": 2}
  2024-01-06T16:21:53.256297273Z	LEVEL(-3)	provisioning/controller.go:478	Synchronizing admission check state based on provisioning request	{"controller": "workload", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Workload", "Workload": {"name":"wl","namespace":"provisioning-x5dvq"}, "namespace": "provisioning-x5dvq", "name": "wl", "reconcileID": "aa93259d-90c0-4751-b0c6-9f8cf9daa25e", "wl": {"name":"wl","namespace":"provisioning-x5dvq"}, "check": "ac-prov", "prName": "wl-ac-prov-2", "failed": false, "accepted": false, "available": false}
  2024-01-06T16:21:53.256631426Z	DEBUG	events	recorder/recorder.go:104	Created ProvisioningRequest: "wl-ac-prov-2"	{"type": "Normal", "object": {"kind":"Workload","namespace":"provisioning-x5dvq","name":"wl","uid":"207f9e17-41b5-463c-bc75-2d16e60db4a5","apiVersion":"kueue.x-k8s.io/v1beta1","resourceVersion":"397"}, "reason": "ProvisioningRequestCreated"}
```
Then it seems the issue is that we set the `Failed` on a different instance than the one used for syncing the admission checks. I think the issue might be due to the fact that the informer (from which the instances are taken) does not yet know about the new instance created in the previous reconciliation cycle.

One idea for fixing this would be to have in-memory state expectations to mark the ProvisioningRequest is currently under creation, we do something similar in the Job controller in k8s, but I'm not sure this is the most "neat" solution. WDYT @alculquicondor ?

### Comment by [@mimowo](https://github.com/mimowo) — 2024-01-15T15:08:06Z

As discussed with Aldo offline, the second creation request should conflict and fail, so still some investigation is needed.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-01-15T15:09:53Z

Also, weirdly I repeated the test 380 times (with cpu stress) locally already and all passed, so it is rare...

### Comment by [@mimowo](https://github.com/mimowo) — 2024-01-15T15:21:27Z

Ok, got it reproduced locally!
