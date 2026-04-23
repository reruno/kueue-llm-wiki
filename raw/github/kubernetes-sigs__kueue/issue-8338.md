# Issue #8338: [Flaky E2E] StatefulSet integration when Workload deactivated, shouldn't delete deactivated Workload

**Summary**: [Flaky E2E] StatefulSet integration when Workload deactivated, shouldn't delete deactivated Workload

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8338

**Last updated**: 2026-01-13T17:55:24Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mykysha](https://github.com/mykysha)
- **Created**: 2025-12-18T16:38:50Z
- **Updated**: 2026-01-13T17:55:24Z
- **Closed**: 2026-01-13T17:55:23Z
- **Labels**: `kind/bug`, `priority/important-soon`, `kind/flake`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 9

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->

/kind flake

**What happened**:
StatefulSet integration when Workload deactivated [It] shouldn't delete deactivated Workload
```
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/statefulset_test.go:627 with:
  Expected
      <int32>: 0
  to equal
      <int32>: 3
  In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/statefulset_test.go:628 @ 12/18/25 16:17:33.655
```

**What you expected to happen**:
No errors

**How to reproduce it (as minimally and precisely as possible)**:
https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/8335/pull-kueue-test-e2e-main-1-34/2001681192595755008

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T08:29:57Z

/priority important-soon

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-12-23T12:06:21Z

/assign

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-12-31T12:01:01Z

So far not possible to reproduce locally - after 100 repeated attempts.
Logs analysis shows no visible source of the issue between the relevant timestamp: 16:16:34 - 16:17:33.

* Kubelet deletes initial pods but there is no `ADD` event after reactivation.
* Kube controller manager shows no error during time period, all objects seem to be present.

IMHO Kueue-controller-manager logs look totally fine:
```
2025-12-18T16:16:48.389983383Z stderr F 2025-12-18T16:16:48.38974884Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:894	Workload update event	{"replica-role": "follower", "workload": {"name":"statefulset-sts-18b6e","namespace":"sts-e2e-slbpz"}, "queue": "sts-lq", "status": "pending"}
2025-12-18T16:16:48.390794311Z stderr F 2025-12-18T16:16:48.390651179Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:183	Reconcile Workload	{"replica-role": "leader", "namespace": "sts-e2e-slbpz", "name": "statefulset-sts-18b6e", "reconcileID": "664d853d-c121-47b5-ac2d-ce0c28258987"}
2025-12-18T16:16:48.391424757Z stderr F 2025-12-18T16:16:48.390454877Z	LEVEL(-2)	v1_pod	jobframework/reconciler.go:418	Reconciling Job	{"replica-role": "leader", "namespace": "group/sts-e2e-slbpz", "name": "statefulset-sts-18b6e", "reconcileID": "0eff2e76-f5b3-413c-95a9-49b0cd2bc38e", "job": "group/sts-e2e-slbpz/statefulset-sts-18b6e", "gvk": "/v1, Kind=Pod"}
2025-12-18T16:16:48.391436587Z stderr F 2025-12-18T16:16:48.391269375Z	LEVEL(-3)	v1_pod	jobframework/reconciler.go:533	reclaimable pods are up-to-date	{"replica-role": "leader", "namespace": "group/sts-e2e-slbpz", "name": "statefulset-sts-18b6e", "reconcileID": "0eff2e76-f5b3-413c-95a9-49b0cd2bc38e", "job": "group/sts-e2e-slbpz/statefulset-sts-18b6e", "gvk": "/v1, Kind=Pod"}
2025-12-18T16:16:48.391441367Z stderr F 2025-12-18T16:16:48.391312826Z	LEVEL(-3)	v1_pod	jobframework/reconciler.go:570	Handling a job with evicted condition	{"replica-role": "leader", "namespace": "group/sts-e2e-slbpz", "name": "statefulset-sts-18b6e", "reconcileID": "0eff2e76-f5b3-413c-95a9-49b0cd2bc38e", "job": "group/sts-e2e-slbpz/statefulset-sts-18b6e", "gvk": "/v1, Kind=Pod"}
2025-12-18T16:16:48.391453877Z stderr F 2025-12-18T16:16:48.390140954Z	LEVEL(-2)	multikueue-workload	multikueue/workload.go:152	Reconcile Workload	{"replica-role": "leader", "namespace": "sts-e2e-slbpz", "name": "statefulset-sts-18b6e", "reconcileID": "a65f8afb-dbbd-49ce-b349-5727590dd04e"}
2025-12-18T16:16:48.391539538Z stderr F 2025-12-18T16:16:48.391434467Z	LEVEL(-2)	multikueue-workload	multikueue/workload.go:178	Skip Workload	{"replica-role": "leader", "namespace": "sts-e2e-slbpz", "name": "statefulset-sts-18b6e", "reconcileID": "a65f8afb-dbbd-49ce-b349-5727590dd04e", "isDeleted": false}
2025-12-18T16:16:48.391549198Z stderr F 2025-12-18T16:16:48.390892271Z	LEVEL(-3)	scheduler	queue/manager.go:675	Obtained ClusterQueue heads	{"replica-role": "follower", "schedulingCycle": 177, "count": 0}
2025-12-18T16:16:48.422416029Z stderr F 2025-12-18T16:16:48.422170697Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:894	Workload update event	{"replica-role": "follower", "workload": {"name":"statefulset-sts-18b6e","namespace":"sts-e2e-slbpz"}, "queue": "sts-lq", "status": "pending"}
2025-12-18T16:16:48.4225565Z stderr F 2025-12-18T16:16:48.422445119Z	LEVEL(-2)	v1_pod	jobframework/reconciler.go:418	Reconciling Job	{"replica-role": "leader", "namespace": "group/sts-e2e-slbpz", "name": "statefulset-sts-18b6e", "reconcileID": "d2d0f2ed-2f88-4492-9ff6-1155bb275f3a", "job": "group/sts-e2e-slbpz/statefulset-sts-18b6e", "gvk": "/v1, Kind=Pod"}
2025-12-18T16:16:48.422687472Z stderr F 2025-12-18T16:16:48.42253627Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:183	Reconcile Workload	{"replica-role": "leader", "namespace": "sts-e2e-slbpz", "name": "statefulset-sts-18b6e", "reconcileID": "930c653c-b729-4c9e-8e2d-09173d491bf5"}
2025-12-18T16:16:48.422716122Z stderr F 2025-12-18T16:16:48.422614471Z	LEVEL(-3)	v1_pod	jobframework/reconciler.go:533	reclaimable pods are up-to-date	{"replica-role": "leader", "namespace": "group/sts-e2e-slbpz", "name": "statefulset-sts-18b6e", "reconcileID": "d2d0f2ed-2f88-4492-9ff6-1155bb275f3a", "job": "group/sts-e2e-slbpz/statefulset-sts-18b6e", "gvk": "/v1, Kind=Pod"}
2025-12-18T16:16:48.422805313Z stderr F 2025-12-18T16:16:48.422651141Z	LEVEL(-3)	v1_pod	jobframework/reconciler.go:570	Handling a job with evicted condition	{"replica-role": "leader", "namespace": "group/sts-e2e-slbpz", "name": "statefulset-sts-18b6e", "reconcileID": "d2d0f2ed-2f88-4492-9ff6-1155bb275f3a", "job": "group/sts-e2e-slbpz/statefulset-sts-18b6e", "gvk": "/v1, Kind=Pod"}
2025-12-18T16:16:48.422823503Z stderr F 2025-12-18T16:16:48.422210267Z	LEVEL(-2)	multikueue-workload	multikueue/workload.go:152	Reconcile Workload	{"replica-role": "leader", "namespace": "sts-e2e-slbpz", "name": "statefulset-sts-18b6e", "reconcileID": "07fba866-f84a-4b2a-b5d2-e69267096921"}
2025-12-18T16:16:48.422839893Z stderr F 2025-12-18T16:16:48.422732602Z	LEVEL(-2)	multikueue-workload	multikueue/workload.go:178	Skip Workload	{"replica-role": "leader", "namespace": "sts-e2e-slbpz", "name": "statefulset-sts-18b6e", "reconcileID": "07fba866-f84a-4b2a-b5d2-e69267096921", "isDeleted": false}
2025-12-18T16:16:48.422851873Z stderr F 2025-12-18T16:16:48.422768753Z	LEVEL(-3)	scheduler	queue/manager.go:675	Obtained ClusterQueue heads	{"replica-role": "follower", "schedulingCycle": 177, "count": 1}
2025-12-18T16:16:48.423001755Z stderr F 2025-12-18T16:16:48.422881864Z	LEVEL(-3)	scheduler	scheduler/fair_sharing_iterator.go:69	Returning workload from ClusterQueue without Cohort	{"replica-role": "follower", "schedulingCycle": 177, "clusterQueue": {"name":"sts-cq"}, "workload": {"name":"statefulset-sts-18b6e","namespace":"sts-e2e-slbpz"}}
2025-12-18T16:16:48.423012195Z stderr F 2025-12-18T16:16:48.422936434Z	LEVEL(-2)	scheduler	scheduler/scheduler.go:265	Attempting to schedule workload	{"replica-role": "follower", "schedulingCycle": 177, "workload": {"name":"statefulset-sts-18b6e","namespace":"sts-e2e-slbpz"}, "clusterQueue": {"name":"sts-cq"}}
2025-12-18T16:16:48.423094316Z stderr F 2025-12-18T16:16:48.422995195Z	LEVEL(-2)	scheduler	scheduler/scheduler.go:697	Workload assumed in the cache	{"replica-role": "follower", "schedulingCycle": 177, "workload": {"name":"statefulset-sts-18b6e","namespace":"sts-e2e-slbpz"}, "clusterQueue": {"name":"sts-cq"}}
2025-12-18T16:16:48.423121686Z stderr F 2025-12-18T16:16:48.423042875Z	LEVEL(-3)	scheduler	scheduler/logging.go:42	Workload evaluated for admission	{"replica-role": "follower", "schedulingCycle": 177, "workload": {"name":"statefulset-sts-18b6e","namespace":"sts-e2e-slbpz"}, "clusterQueue": {"name":"sts-cq"}, "status": "assumed", "reason": ""}
2025-12-18T16:16:48.423130506Z stderr F 2025-12-18T16:16:48.423090486Z	LEVEL(-3)	scheduler	queue/manager.go:675	Obtained ClusterQueue heads	{"replica-role": "follower", "schedulingCycle": 178, "count": 0}
2025-12-18T16:16:48.45526286Z stderr F 2025-12-18T16:16:48.455015457Z	LEVEL(-2)	scheduler	scheduler/scheduler.go:660	Workload successfully admitted and assigned flavors	{"replica-role": "follower", "schedulingCycle": 177, "workload": {"name":"statefulset-sts-18b6e","namespace":"sts-e2e-slbpz"}, "clusterQueue": {"name":"sts-cq"}, "assignments": [{"name":"5a154bb6","flavors":{"cpu":"sts-rf"},"resourceUsage":{"cpu":"600m"},"count":3}]}
2025-12-18T16:16:48.45530728Z stderr F 2025-12-18T16:16:48.455113278Z	DEBUG	events	recorder/recorder.go:104	Quota reserved in ClusterQueue sts-cq, wait time since queued was 0s	{"type": "Normal", "object": {"kind":"Workload","namespace":"sts-e2e-slbpz","name":"statefulset-sts-18b6e","uid":"544c98bf-5c8d-454c-8596-8fb97ca5c559","apiVersion":"kueue.x-k8s.io/v1beta2","resourceVersion":"15471"}, "reason": "QuotaReserved"}
2025-12-18T16:16:48.4553124Z stderr F 2025-12-18T16:16:48.455141138Z	DEBUG	events	recorder/recorder.go:104	Admitted by ClusterQueue sts-cq, wait time since reservation was 0s	{"type": "Normal", "object": {"kind":"Workload","namespace":"sts-e2e-slbpz","name":"statefulset-sts-18b6e","uid":"544c98bf-5c8d-454c-8596-8fb97ca5c559","apiVersion":"kueue.x-k8s.io/v1beta2","resourceVersion":"15471"}, "reason": "Admitted"}
2025-12-18T16:16:48.455590343Z stderr F 2025-12-18T16:16:48.455230919Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:894	Workload update event	{"replica-role": "follower", "workload": {"name":"statefulset-sts-18b6e","namespace":"sts-e2e-slbpz"}, "queue": "sts-lq", "status": "admitted", "prevStatus": "pending", "clusterQueue": "sts-cq"}
2025-12-18T16:16:48.455601393Z stderr F 2025-12-18T16:16:48.455469502Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:183	Reconcile Workload	{"replica-role": "leader", "namespace": "sts-e2e-slbpz", "name": "statefulset-sts-18b6e", "reconcileID": "5387776b-565e-47ac-9b62-9656bdf5fcc2"}
2025-12-18T16:16:48.455835535Z stderr F 2025-12-18T16:16:48.455659624Z	LEVEL(-2)	multikueue-workload	multikueue/workload.go:152	Reconcile Workload	{"replica-role": "leader", "namespace": "sts-e2e-slbpz", "name": "statefulset-sts-18b6e", "reconcileID": "71e0081e-9f0c-4f29-81ff-5e632eb47b2b"}
2025-12-18T16:16:48.455858045Z stderr F 2025-12-18T16:16:48.455705444Z	LEVEL(-2)	v1_pod	jobframework/reconciler.go:418	Reconciling Job	{"replica-role": "leader", "namespace": "group/sts-e2e-slbpz", "name": "statefulset-sts-18b6e", "reconcileID": "9e130b4b-8544-4c96-96ac-0dc8ee7acb69", "job": "group/sts-e2e-slbpz/statefulset-sts-18b6e", "gvk": "/v1, Kind=Pod"}
2025-12-18T16:16:48.455979477Z stderr F 2025-12-18T16:16:48.455811465Z	LEVEL(-3)	v1_pod	jobframework/reconciler.go:533	reclaimable pods are up-to-date	{"replica-role": "leader", "namespace": "group/sts-e2e-slbpz", "name": "statefulset-sts-18b6e", "reconcileID": "9e130b4b-8544-4c96-96ac-0dc8ee7acb69", "job": "group/sts-e2e-slbpz/statefulset-sts-18b6e", "gvk": "/v1, Kind=Pod"}
2025-12-18T16:16:48.455988097Z stderr F 2025-12-18T16:16:48.455873876Z	LEVEL(-2)	v1_pod	jobframework/reconciler.go:602	Job admitted, unsuspending	{"replica-role": "leader", "namespace": "group/sts-e2e-slbpz", "name": "statefulset-sts-18b6e", "reconcileID": "9e130b4b-8544-4c96-96ac-0dc8ee7acb69", "job": "group/sts-e2e-slbpz/statefulset-sts-18b6e", "gvk": "/v1, Kind=Pod"}
2025-12-18T16:16:48.456002497Z stderr F 2025-12-18T16:16:48.455720854Z	LEVEL(-2)	multikueue-workload	multikueue/workload.go:178	Skip Workload	{"replica-role": "leader", "namespace": "sts-e2e-slbpz", "name": "statefulset-sts-18b6e", "reconcileID": "71e0081e-9f0c-4f29-81ff-5e632eb47b2b", "isDeleted": false}
2025-12-18T16:16:49.168742686Z stderr F 2025-12-18T16:16:49.168427213Z	LEVEL(-2)	v1_pod	jobframework/reconciler.go:418	Reconciling Job	{"replica-role": "leader", "namespace": "group/sts-e2e-slbpz", "name": "statefulset-sts-18b6e", "reconcileID": "3ee00555-3dd0-4b3a-9c35-4c7882c9328e", "job": "group/sts-e2e-slbpz/statefulset-sts-18b6e", "gvk": "/v1, Kind=Pod"}
2025-12-18T16:16:49.168787376Z stderr F 2025-12-18T16:16:49.168586324Z	LEVEL(-3)	v1_pod	jobframework/reconciler.go:533	reclaimable pods are up-to-date	{"replica-role": "leader", "namespace": "group/sts-e2e-slbpz", "name": "statefulset-sts-18b6e", "reconcileID": "3ee00555-3dd0-4b3a-9c35-4c7882c9328e", "job": "group/sts-e2e-slbpz/statefulset-sts-18b6e", "gvk": "/v1, Kind=Pod"}
2025-12-18T16:16:49.168847997Z stderr F 2025-12-18T16:16:49.168640405Z	LEVEL(-2)	v1_pod	jobframework/reconciler.go:602	Job admitted, unsuspending	{"replica-role": "leader", "namespace": "group/sts-e2e-slbpz", "name": "statefulset-sts-18b6e", "reconcileID": "3ee00555-3dd0-4b3a-9c35-4c7882c9328e", "job": "group/sts-e2e-slbpz/statefulset-sts-18b6e", "gvk": "/v1, Kind=Pod"}
2025-12-18T16:16:49.175011287Z stderr F 2025-12-18T16:16:49.174783935Z	LEVEL(-2)	clusterqueue-reconciler	core/clusterqueue_controller.go:157	Reconcile ClusterQueue	{"replica-role": "leader", "name": "sts-cq", "reconcileID": "85ef59ce-ce3e-4a96-9834-e7b0eac33d65"}
2025-12-18T16:16:49.175044527Z stderr F 2025-12-18T16:16:49.174831875Z	LEVEL(-2)	localqueue-reconciler	core/localqueue_controller.go:163	Reconcile LocalQueue	{"replica-role": "leader", "namespace": "sts-e2e-slbpz", "name": "sts-lq", "reconcileID": "6e6a016d-ca8e-4be3-be33-3912ffb806d3"}
2025-12-18T16:16:49.179232908Z stderr F 2025-12-18T16:16:49.178985736Z	LEVEL(-2)	v1_pod	jobframework/reconciler.go:418	Reconciling Job	{"replica-role": "leader", "namespace": "group/sts-e2e-slbpz", "name": "statefulset-sts-18b6e", "reconcileID": "d37d3e15-c90b-4041-8a63-701832542bc7", "job": "group/sts-e2e-slbpz/statefulset-sts-18b6e", "gvk": "/v1, Kind=Pod"}
2025-12-18T16:16:49.179530231Z stderr F 2025-12-18T16:16:49.17938693Z	LEVEL(-3)	v1_pod	jobframework/reconciler.go:533	reclaimable pods are up-to-date	{"replica-role": "leader", "namespace": "group/sts-e2e-slbpz", "name": "statefulset-sts-18b6e", "reconcileID": "d37d3e15-c90b-4041-8a63-701832542bc7", "job": "group/sts-e2e-slbpz/statefulset-sts-18b6e", "gvk": "/v1, Kind=Pod"}
2025-12-18T16:16:49.179541441Z stderr F 2025-12-18T16:16:49.17943456Z	LEVEL(-2)	v1_pod	jobframework/reconciler.go:602	Job admitted, unsuspending	{"replica-role": "leader", "namespace": "group/sts-e2e-slbpz", "name": "statefulset-sts-18b6e", "reconcileID": "d37d3e15-c90b-4041-8a63-701832542bc7", "job": "group/sts-e2e-slbpz/statefulset-sts-18b6e", "gvk": "/v1, Kind=Pod"}
2025-12-18T16:16:49.182884524Z stderr F 2025-12-18T16:16:49.182686032Z	LEVEL(-2)	localqueue-reconciler	core/localqueue_controller.go:250	Queue update event	{"replica-role": "follower", "localQueue": {"name":"sts-lq","namespace":"sts-e2e-slbpz"}}
2025-12-18T16:16:49.182920034Z stderr F 2025-12-18T16:16:49.182849223Z	LEVEL(-2)	localqueue-reconciler	core/localqueue_controller.go:163	Reconcile LocalQueue	{"replica-role": "leader", "namespace": "sts-e2e-slbpz", "name": "sts-lq", "reconcileID": "43ce2981-2aef-4e01-8499-51788e8cf9f1"}
2025-12-18T16:16:49.183672191Z stderr F 2025-12-18T16:16:49.183464229Z	LEVEL(-2)	cluster-queue-reconciler	core/clusterqueue_controller.go:334	ClusterQueue update event	{"replica-role": "follower", "clusterQueue": {"name":"sts-cq"}}
2025-12-18T16:16:49.184219817Z stderr F 2025-12-18T16:16:49.184051915Z	LEVEL(-2)	clusterqueue-reconciler	core/clusterqueue_controller.go:157	Reconcile ClusterQueue	{"replica-role": "leader", "name": "sts-cq", "reconcileID": "924db3c0-3e8f-45a6-9f86-77ad00532670"}
```

then they are silent for the timeout of 45 seconds and then test fails:
```
2025-12-18T16:17:33.683173015Z stderr F 2025-12-18T16:17:33.682864992Z	LEVEL(-3)	jobframework/reconciler.go:779	stop walking up as the owner is not found	{"currentObj": {"name":"sts","namespace":"sts-e2e-slbpz"}}
2025-12-18T16:17:33.683207755Z stderr F 2025-12-18T16:17:33.683013933Z	LEVEL(-2)	statefulset	statefulset/statefulset_reconciler.go:74	Reconcile StatefulSet	{"replica-role": "leader", "namespace": "sts-e2e-slbpz", "name": "sts", "reconcileID": "51a2e906-04e9-447d-97f6-1bb839de27c6"}
2025-12-18T16:17:33.683420537Z stderr F 2025-12-18T16:17:33.683241645Z	LEVEL(-3)	statefulset	statefulset/statefulset_reconciler.go:117	Finalizing pod in group	{"replica-role": "leader", "namespace": "sts-e2e-slbpz", "name": "sts", "reconcileID": "51a2e906-04e9-447d-97f6-1bb839de27c6", "pod": {"name":"sts-0","namespace":"sts-e2e-slbpz"}, "group": "statefulset-sts-18b6e"}
2025-12-18T16:17:33.683598029Z stderr F 2025-12-18T16:17:33.683401727Z	LEVEL(-3)	statefulset	statefulset/statefulset_reconciler.go:117	Finalizing pod in group	{"replica-role": "leader", "namespace": "sts-e2e-slbpz", "name": "sts", "reconcileID": "51a2e906-04e9-447d-97f6-1bb839de27c6", "pod": {"name":"sts-1","namespace":"sts-e2e-slbpz"}, "group": "statefulset-sts-18b6e"}
2025-12-18T16:17:33.695761518Z stderr F 2025-12-18T16:17:33.695416015Z	LEVEL(-2)	localqueue-reconciler	core/localqueue_controller.go:242	LocalQueue delete event	{"replica-role": "follower", "localQueue": {"name":"sts-lq","namespace":"sts-e2e-slbpz"}}
2025-12-18T16:17:33.695802709Z stderr F 2025-12-18T16:17:33.695581066Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:183	Reconcile Workload	{"replica-role": "leader", "namespace": "sts-e2e-slbpz", "name": "statefulset-sts-18b6e", "reconcileID": "fc580596-9b74-42c1-b9ac-50a86e121f16"}
```

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-08T08:25:18Z

Looking at the Kube-scheduler logs there were no Pods scheduled after re-admission (at `16:16:48.389`) in the namespace `sts-e2e-slbpz`: https://storage.googleapis.com/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/8335/pull-kueue-test-e2e-main-1-34/2001681192595755008/artifacts/run-test-e2e-singlecluster-1.34.0/kind-control-plane/pods/kube-system_kube-scheduler-kind-control-plane_14095e8558fd689c940f507d032d4780/kube-scheduler/0.log

Looking at the kube-apiserver logs the replacement pods were not created at all: https://storage.googleapis.com/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/8335/pull-kueue-test-e2e-main-1-34/2001681192595755008/artifacts/run-test-e2e-singlecluster-1.34.0/kind-control-plane/pods/kube-system_kube-apiserver-kind-control-plane_e0a0bab2abb3f66b7ca6766a308fe1e1/kube-apiserver/0.log.20251218-161920

I think this is likely because we re-admitted while the old Pods were not deleted fully (just not Ready, but still terminating). This likely triggered a race condition bug in our StatefulSet integration).

If this is correct I can see two paths forward:
1. plumb the test for now awaiting for the complete deletion of old Pods before re-activating the workload
2. fixing of the StatefulSet controller

It would be great to investigate if (2.) is possible, maybe this is not too hard.

cc @mbobrovskyi @sohankunkerkar who may have some ideas how to fix it properly. Otherwise I'm ok with (1.) and opening a follow up issue for (2.).

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-08T14:22:49Z

https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-release-0-15-1-32/2009256512270110720

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-01-08T22:08:54Z

>I think this is likely because we re-admitted while the old Pods were not deleted fully (just not Ready, but still terminating). This likely triggered a race condition bug in our StatefulSet integration).

I suspect the bug is in the `StatefulSet` controller's pod event handler. Looking at pkg/controller/jobs/statefulset/statefulset_reconciler.go, the `podHandler.Update` method was empty. This means when pods transition from `Running → Succeeded/Failed (terminating)`, no reconciliation is triggered. so finalizers (`kueue.x-k8s.io/managed`) are never removed until some other event triggers reconciliation. I feel adding the logic in `Update` make sense bc it's event-driven and reacts immediately when pods terminate, triggering only on valid transitions.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-09T16:55:43Z

Thank you for reporting, I propose:
1. very short term: merge https://github.com/kubernetes-sigs/kueue/pull/8268 as it already addresses most of the race window
2. short term address the follow up proposed here to add handling in Update for Pods
3. long/mid term address https://github.com/kubernetes-sigs/kueue/issues/8497

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-13T17:55:18Z

/close 
As https://github.com/kubernetes-sigs/kueue/pull/8530 is merged and we are cherrypicking

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-01-13T17:55:24Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/8338#issuecomment-3745649154):

>/close 
>As https://github.com/kubernetes-sigs/kueue/pull/8530 is merged and we are cherrypicking


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
