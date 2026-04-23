# Issue #6128: [Flaky E2E] ObjectRetentionPolicies should delete the Workload after enabling the ObjectRetentionPolicies feature gate

**Summary**: [Flaky E2E] ObjectRetentionPolicies should delete the Workload after enabling the ObjectRetentionPolicies feature gate

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6128

**Last updated**: 2025-08-04T09:05:48Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2025-07-22T07:19:03Z
- **Updated**: 2025-08-04T09:05:48Z
- **Closed**: 2025-08-04T09:05:48Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 1

## Description

/kind flake

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
End To End Custom Configs handling Suite: kindest/node:v1.33.1: [It] ObjectRetentionPolicies should delete the Workload after enabling the ObjectRetentionPolicies feature gate

```
{Timed out after 10.000s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/customconfigs/objectretentionpolicies_test.go:122 with:
Error matcher expects an error.  Got:
    <nil>: nil failed [FAILED] Timed out after 10.000s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/customconfigs/objectretentionpolicies_test.go:122 with:
Error matcher expects an error.  Got:
    <nil>: nil
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/customconfigs/objectretentionpolicies_test.go:123 @ 07/21/25 15:26:07.068

There were additional failures detected after the initial failure. These are visible in the timeline
}
```

**What you expected to happen**:
No errors

**How to reproduce it (as minimally and precisely as possible)**:
https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/6114/pull-kueue-test-e2e-customconfigs-main/1947314745077927936

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-22T12:29:09Z

I looked up the issue at bit, it seems it manifests a real issue with handling Kueue restart (which we know is not ideal).

The namespace in question is `orp-kmqzh`. The leading Kueue replicas are on worker2, first `kueue-controller-manager-648fff78c5-rwcjq`, and after restart `kueue-controller-manager-cd7f485c7-88bzk`.

Here are the logs grepped by the namespace:

before restart:
```
2025-07-21T15:25:07.558707354Z stderr F 2025-07-21T15:25:07.558534271Z	LEVEL(-2)	localqueue-reconciler	core/localqueue_controller.go:193	LocalQueue create event	{"localQueue": {"name":"lq","namespace":"orp-kmqzh"}}
2025-07-21T15:25:30.05590468Z stderr F 2025-07-21T15:25:30.055651316Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:671	Workload create event	{"workload": {"name":"job-job-4e743","namespace":"orp-kmqzh"}, "queue": "lq", "status": "pending"}
2025-07-21T15:25:30.068234336Z stderr F 2025-07-21T15:25:30.067962482Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:750	Workload update event	{"workload": {"name":"job-job-4e743","namespace":"orp-kmqzh"}, "queue": "lq", "status": "pending"}
2025-07-21T15:25:30.079787769Z stderr F 2025-07-21T15:25:30.079463064Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:750	Workload update event	{"workload": {"name":"job-job-4e743","namespace":"orp-kmqzh"}, "queue": "lq", "status": "admitted", "prevStatus": "pending", "clusterQueue": "cq"}
2025-07-21T15:25:30.095846453Z stderr F 2025-07-21T15:25:30.095602869Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:750	Workload update event	{"workload": {"name":"job-job-4e743","namespace":"orp-kmqzh"}, "queue": "lq", "status": "admitted", "clusterQueue": "cq"}
2025-07-21T15:25:30.101101246Z stderr F 2025-07-21T15:25:30.100865163Z	LEVEL(-3)	admission	jobframework/reconciler.go:734	stop walking up as the owner is not found{"object": {"name":"","namespace":"orp-kmqzh"}, "namespace": "orp-kmqzh", "name": "", "resource": {"group":"","version":"v1","resource":"pods"}, "user": "system:serviceaccount:kube-system:job-controller", "requestID": "023f0c69-fef6-4eb3-828c-ded07886700d", "currentObj": {"name":"job","namespace":"orp-kmqzh"}}
2025-07-21T15:25:30.148147743Z stderr F 2025-07-21T15:25:30.147880459Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:750	Workload update event	{"workload": {"name":"job-job-4e743","namespace":"orp-kmqzh"}, "queue": "lq", "status": "pending", "prevStatus": "admitted", "prevClusterQueue": "cq"}
2025-07-21T15:25:30.148186174Z stderr F 2025-07-21T15:25:30.148054812Z	LEVEL(-3)	workload-reconciler	core/workload_controller.go:809	Workload to be requeued after backoff	{"workload": {"name":"job-job-4e743","namespace":"orp-kmqzh"}, "queue": "lq", "status": "pending", "prevStatus": "admitted", "prevClusterQueue": "cq", "backoff": "851.977439ms", "requeueAt": "2025-07-21T15:25:31Z"}
2025-07-21T15:25:31.000840045Z stderr F 2025-07-21T15:25:31.000644602Z	LEVEL(-3)	workload-reconciler	core/workload_controller.go:817	Workload requeued after backoff	{"workload": {"name":"job-job-4e743","namespace":"orp-kmqzh"}, "queue": "lq", "status": "pending", "prevStatus": "admitted", "prevClusterQueue": "cq"}
2025-07-21T15:25:31.026260418Z stderr F 2025-07-21T15:25:31.026040724Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:750	Workload update event	{"workload": {"name":"job-job-4e743","namespace":"orp-kmqzh"}, "queue": "lq", "status": "pending"}
2025-07-21T15:25:31.059043308Z stderr F 2025-07-21T15:25:31.058848745Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:750	Workload update event	{"workload": {"name":"job-job-4e743","namespace":"orp-kmqzh"}, "queue": "lq", "status": "admitted", "prevStatus": "pending", "clusterQueue": "cq"}
2025-07-21T15:25:31.068337766Z stderr F 2025-07-21T15:25:31.068121832Z	LEVEL(-2)	localqueue-reconciler	core/localqueue_controller.go:226	Queue update event	{"localQueue": {"name":"lq","namespace":"orp-kmqzh"}}
2025-07-21T15:25:31.07806489Z stderr F 2025-07-21T15:25:31.077893117Z	LEVEL(-3)	admission	jobframework/reconciler.go:734	stop walking up as the owner is not found{"object": {"name":"","namespace":"orp-kmqzh"}, "namespace": "orp-kmqzh", "name": "", "resource": {"group":"","version":"v1","resource":"pods"}, "user": "system:serviceaccount:kube-system:job-controller", "requestID": "c4acfb32-cc04-427e-94ca-81d21ee2bf11", "currentObj": {"name":"job","namespace":"orp-kmqzh"}}
2025-07-21T15:25:31.084864348Z stderr F 2025-07-21T15:25:31.084646714Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:750	Workload update event	{"workload": {"name":"job-job-4e743","namespace":"orp-kmqzh"}, "queue": "lq", "status": "admitted", "clusterQueue": "cq"}
2025-07-21T15:25:31.113601113Z stderr F 2025-07-21T15:25:31.113369809Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:750	Workload update event	{"workload": {"name":"job-job-4e743","namespace":"orp-kmqzh"}, "queue": "lq", "status": "admitted", "clusterQueue": "cq"}
2025-07-21T15:25:31.113628023Z stderr F 2025-07-21T15:25:31.113479361Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:759	Workload will not be queued because the workload is not active	{"workload": {"name":"job-job-4e743","namespace":"orp-kmqzh"}, "queue": "lq", "status": "admitted", "clusterQueue": "cq"}
2025-07-21T15:25:31.137552263Z stderr F 2025-07-21T15:25:31.137299319Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:750	Workload update event	{"workload": {"name":"job-job-4e743","namespace":"orp-kmqzh"}, "queue": "lq", "status": "admitted", "clusterQueue": "cq"}
2025-07-21T15:25:31.137577133Z stderr F 2025-07-21T15:25:31.137409171Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:759	Workload will not be queued because the workload is not active	{"workload": {"name":"job-job-4e743","namespace":"orp-kmqzh"}, "queue": "lq", "status": "admitted", "clusterQueue": "cq"}
2025-07-21T15:25:31.544720819Z stderr F 2025-07-21T15:25:31.544476835Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:750	Workload update event	{"workload": {"name":"job-job-4e743","namespace":"orp-kmqzh"}, "queue": "lq", "status": "pending", "prevStatus": "admitted", "prevClusterQueue": "cq"}
2025-07-21T15:25:31.54475777Z stderr F 2025-07-21T15:25:31.544577937Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:759	Workload will not be queued because the workload is not active	{"workload": {"name":"job-job-4e743","namespace":"orp-kmqzh"}, "queue": "lq", "status": "pending", "prevStatus": "admitted", "prevClusterQueue": "cq"}
```

after restart `kueue-controller-manager-cd7f485c7-88bzk`:
```
2025-07-21T15:25:35.414008827Z stderr F 2025-07-21T15:25:35.413171974Z	LEVEL(-2)	localqueue-reconciler	core/localqueue_controller.go:193	LocalQueue create event	{"localQueue": {"name":"lq","namespace":"orp-kmqzh"}}
2025-07-21T15:25:35.414012797Z stderr F 2025-07-21T15:25:35.413747033Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:671	Workload create event	{"workload": {"name":"job-job-4e743","namespace":"orp-kmqzh"}, "queue": "lq", "status": "pending"}
2025-07-21T15:25:35.414049538Z stderr F 2025-07-21T15:25:35.413839654Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:688	ClusterQueue for workload didn't exist; ignored for now	{"workload": {"name":"job-job-4e743","namespace":"orp-kmqzh"}, "queue": "lq", "status": "pending"}
2025-07-21T15:26:07.18400243Z stderr F 2025-07-21T15:26:07.183711465Z	LEVEL(-2)	localqueue-reconciler	core/localqueue_controller.go:218	LocalQueue delete event	{"localQueue": {"name":"lq","namespace":"orp-kmqzh"}}
2025-07-21T15:26:07.287607383Z stderr F 2025-07-21T15:26:07.28739927Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:750	Workload update event	{"workload": {"name":"job-job-4e743","namespace":"orp-kmqzh"}, "queue": "lq", "status": "pending"}
2025-07-21T15:26:07.287642573Z stderr F 2025-07-21T15:26:07.287515431Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:759	Workload will not be queued because the workload is not active	{"workload": {"name":"job-job-4e743","namespace":"orp-kmqzh"}, "queue": "lq", "status": "pending"}
2025-07-21T15:26:07.353311025Z stderr F 2025-07-21T15:26:07.353048771Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:701	Workload delete event	{"workload": {"name":"job-job-4e743","namespace":"orp-kmqzh"}, "queue": "lq", "status": "pending"}
```
It seems all the logs before restart are fine, but it surprises me there are no logs from reconciler.go for the Job after restart.  I suppose it might be related to "Workload will not be queued because the workload is not active", but I'm not sure.
