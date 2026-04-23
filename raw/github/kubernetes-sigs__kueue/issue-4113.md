# Issue #4113: [Flaky test] Pod controller when manageJobsWithoutQueueName is disabled when Using pod group Should ungate pods with prebuild workload

**Summary**: [Flaky test] Pod controller when manageJobsWithoutQueueName is disabled when Using pod group Should ungate pods with prebuild workload

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4113

**Last updated**: 2025-02-20T16:48:29Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-01-31T10:29:36Z
- **Updated**: 2025-02-20T16:48:29Z
- **Closed**: 2025-02-20T16:48:29Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 2

## Description

/kind flake

**What happened**:

The test failed on periodic build of main branch: https://testgrid.k8s.io/sig-scheduling#periodic-kueue-test-integration-main

![Image](https://github.com/user-attachments/assets/27bf8458-927b-4ae2-a344-b7bc4d3ce6f4)

**What you expected to happen**:

No failures

**How to reproduce it (as minimally and precisely as possible)**:

Run CI

**Anything else we need to know?**:

This is a new test introduced in https://github.com/kubernetes-sigs/kueue/pull/4023

```
{Timed out after 10.001s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/util/util.go:767 with:
Expected
    <[]v1.PodSchedulingGate | len:1, cap:1>: [
        {
            Name: "kueue.x-k8s.io/admission",
        },
    ]
not to contain element matching
    <v1.PodSchedulingGate>: {
        Name: "kueue.x-k8s.io/admission",
    } failed [FAILED] Timed out after 10.001s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/util/util.go:767 with:
Expected
    <[]v1.PodSchedulingGate | len:1, cap:1>: [
        {
            Name: "kueue.x-k8s.io/admission",
        },
    ]
not to contain element matching
    <v1.PodSchedulingGate>: {
        Name: "kueue.x-k8s.io/admission",
    }
In [It] at: /home/prow/go/src/kubernetes-sigs/kueue/test/integration/singlecluster/controller/jobs/pod/pod_controller_test.go:1655 @ 01/30/25 18:22:28.131
}
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-31T10:29:50Z

/assign @mbobrovskyi
PTAL

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-11T09:21:54Z

I'm looking at the [failure](https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-integration-main/1885028152829284352). Downloaded the build-log and grep it by `grep -e s7lrj -e STEP` I see:

```
  2025-01-30T18:22:17.028121219Z	LEVEL(-2)	localqueue-reconciler	core/localqueue_controller.go:139	LocalQueue create event	{"localQueue": {"name":"lq","namespace":"pod-s7lrj"}}
  STEP: Creating first pod @ 01/30/25 18:22:17.028
  2025-01-30T18:22:17.028601379Z	LEVEL(-2)	core/localqueue_controller.go:109	Reconciling LocalQueue	{"controller": "localqueue", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "LocalQueue", "LocalQueue": {"name":"lq","namespace":"pod-s7lrj"}, "namespace": "pod-s7lrj", "name": "lq", "reconcileID": "150aaa02-200c-45c6-97ea-5613aac1b0d3", "localQueue": {"name":"lq","namespace":"pod-s7lrj"}}
  2025-01-30T18:22:17.03573695Z	LEVEL(-2)	core/localqueue_controller.go:109	Reconciling LocalQueue	{"controller": "localqueue", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "LocalQueue", "LocalQueue": {"name":"lq","namespace":"pod-s7lrj"}, "namespace": "pod-s7lrj", "name": "lq", "reconcileID": "85c4f2be-59c9-4d27-9da1-d953dd7f9bd1", "localQueue": {"name":"lq","namespace":"pod-s7lrj"}}
  2025-01-30T18:22:17.037355864Z	LEVEL(-2)	localqueue-reconciler	core/localqueue_controller.go:184	Queue update event	{"localQueue": {"name":"lq","namespace":"pod-s7lrj"}}
  2025-01-30T18:22:17.041139243Z	ERROR	controller/controller.go:316	Reconciler error	{"controller": "localqueue", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "LocalQueue", "LocalQueue": {"name":"lq","namespace":"pod-s7lrj"}, "namespace": "pod-s7lrj", "name": "lq", "reconcileID": "85c4f2be-59c9-4d27-9da1-d953dd7f9bd1", "error": "Operation cannot be fulfilled on localqueues.kueue.x-k8s.io \"lq\": the object has been modified; please apply your changes to the latest version and try again"}
  2025-01-30T18:22:17.041510131Z	LEVEL(-2)	core/localqueue_controller.go:109	Reconciling LocalQueue	{"controller": "localqueue", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "LocalQueue", "LocalQueue": {"name":"lq","namespace":"pod-s7lrj"}, "namespace": "pod-s7lrj", "name": "lq", "reconcileID": "9a8f7b7c-0a80-476b-b7c2-c1f5c4a3f4da", "localQueue": {"name":"lq","namespace":"pod-s7lrj"}}
  STEP: Creating prebuild workload @ 01/30/25 18:22:17.045
  2025-01-30T18:22:17.045867293Z	LEVEL(-2)	jobframework/reconciler.go:355	Reconciling Job	{"controller": "v1_pod", "namespace": "group/pod-s7lrj", "name": "test-group", "reconcileID": "d5a098d4-1468-4385-be53-97e8743712e0", "job": "group/pod-s7lrj/test-group", "gvk": "/v1, Kind=Pod"}
  2025-01-30T18:22:17.046003256Z	LEVEL(-3)	jobframework/reconciler.go:423	The workload is nil, handle job with no workload	{"controller": "v1_pod", "namespace": "group/pod-s7lrj", "name": "test-group", "reconcileID": "d5a098d4-1468-4385-be53-97e8743712e0", "job": "group/pod-s7lrj/test-group", "gvk": "/v1, Kind=Pod"}
  2025-01-30T18:22:17.046109518Z	ERROR	jobframework/reconciler.go:433	Handling job with no workload	{"controller": "v1_pod", "namespace": "group/pod-s7lrj", "name": "test-group", "reconcileID": "d5a098d4-1468-4385-be53-97e8743712e0", "job": "group/pod-s7lrj/test-group", "gvk": "/v1, Kind=Pod", "error": "prebuild workload not found"}
  2025-01-30T18:22:17.046356503Z	ERROR	controller/controller.go:316	Reconciler error	{"controller": "v1_pod", "namespace": "group/pod-s7lrj", "name": "test-group", "reconcileID": "d5a098d4-1468-4385-be53-97e8743712e0", "error": "prebuild workload not found"}
  2025-01-30T18:22:17.049642293Z	LEVEL(-2)	core/localqueue_controller.go:109	Reconciling LocalQueue	{"controller": "localqueue", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "LocalQueue", "LocalQueue": {"name":"lq","namespace":"pod-s7lrj"}, "namespace": "pod-s7lrj", "name": "lq", "reconcileID": "c4c520f6-3191-437d-91e2-d25ba1ba250b", "localQueue": {"name":"lq","namespace":"pod-s7lrj"}}
  2025-01-30T18:22:17.050286626Z	LEVEL(-2)	localqueue-reconciler	core/localqueue_controller.go:184	Queue update event	{"localQueue": {"name":"lq","namespace":"pod-s7lrj"}}
  2025-01-30T18:22:17.052763548Z	LEVEL(-2)	jobframework/reconciler.go:355	Reconciling Job	{"controller": "v1_pod", "namespace": "group/pod-s7lrj", "name": "test-group", "reconcileID": "421f6273-0b6a-42e9-a219-e3cbd84e2eaa", "job": "group/pod-s7lrj/test-group", "gvk": "/v1, Kind=Pod"}
  2025-01-30T18:22:17.052914432Z	LEVEL(-3)	jobframework/reconciler.go:423	The workload is nil, handle job with no workload	{"controller": "v1_pod", "namespace": "group/pod-s7lrj", "name": "test-group", "reconcileID": "421f6273-0b6a-42e9-a219-e3cbd84e2eaa", "job": "group/pod-s7lrj/test-group", "gvk": "/v1, Kind=Pod"}
  2025-01-30T18:22:17.053006394Z	ERROR	jobframework/reconciler.go:433	Handling job with no workload	{"controller": "v1_pod", "namespace": "group/pod-s7lrj", "name": "test-group", "reconcileID": "421f6273-0b6a-42e9-a219-e3cbd84e2eaa", "job": "group/pod-s7lrj/test-group", "gvk": "/v1, Kind=Pod", "error": "prebuild workload not found"}
  2025-01-30T18:22:17.053193038Z	ERROR	controller/controller.go:316	Reconciler error	{"controller": "v1_pod", "namespace": "group/pod-s7lrj", "name": "test-group", "reconcileID": "421f6273-0b6a-42e9-a219-e3cbd84e2eaa", "error": "prebuild workload not found"}
  2025-01-30T18:22:17.054666089Z	ERROR	controller/controller.go:316	Reconciler error	{"controller": "localqueue", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "LocalQueue", "LocalQueue": {"name":"lq","namespace":"pod-s7lrj"}, "namespace": "pod-s7lrj", "name": "lq", "reconcileID": "c4c520f6-3191-437d-91e2-d25ba1ba250b", "error": "Operation cannot be fulfilled on localqueues.kueue.x-k8s.io \"lq\": the object has been modified; please apply your changes to the latest version and try again"}
  2025-01-30T18:22:17.054999216Z	LEVEL(-2)	core/localqueue_controller.go:109	Reconciling LocalQueue	{"controller": "localqueue", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "LocalQueue", "LocalQueue": {"name":"lq","namespace":"pod-s7lrj"}, "namespace": "pod-s7lrj", "name": "lq", "reconcileID": "02f79704-76de-44c1-9ac3-ebe2c4c841cd", "localQueue": {"name":"lq","namespace":"pod-s7lrj"}}
  2025-01-30T18:22:17.062849971Z	LEVEL(-2)	core/localqueue_controller.go:109	Reconciling LocalQueue	{"controller": "localqueue", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "LocalQueue", "LocalQueue": {"name":"lq","namespace":"pod-s7lrj"}, "namespace": "pod-s7lrj", "name": "lq", "reconcileID": "2e8dc2ae-cae3-456e-9c7a-f2156395e779", "localQueue": {"name":"lq","namespace":"pod-s7lrj"}}
  2025-01-30T18:22:17.063824332Z	LEVEL(-2)	jobframework/reconciler.go:355	Reconciling Job	{"controller": "v1_pod", "namespace": "group/pod-s7lrj", "name": "test-group", "reconcileID": "71db7283-e82f-44b7-8d37-0873f4683c7c", "job": "group/pod-s7lrj/test-group", "gvk": "/v1, Kind=Pod"}
  2025-01-30T18:22:17.063943514Z	LEVEL(-3)	jobframework/reconciler.go:423	The workload is nil, handle job with no workload	{"controller": "v1_pod", "namespace": "group/pod-s7lrj", "name": "test-group", "reconcileID": "71db7283-e82f-44b7-8d37-0873f4683c7c", "job": "group/pod-s7lrj/test-group", "gvk": "/v1, Kind=Pod"}
  2025-01-30T18:22:17.064016626Z	ERROR	jobframework/reconciler.go:433	Handling job with no workload	{"controller": "v1_pod", "namespace": "group/pod-s7lrj", "name": "test-group", "reconcileID": "71db7283-e82f-44b7-8d37-0873f4683c7c", "job": "group/pod-s7lrj/test-group", "gvk": "/v1, Kind=Pod", "error": "prebuild workload not found"}
  2025-01-30T18:22:17.064163009Z	ERROR	controller/controller.go:316	Reconciler error	{"controller": "v1_pod", "namespace": "group/pod-s7lrj", "name": "test-group", "reconcileID": "71db7283-e82f-44b7-8d37-0873f4683c7c", "error": "prebuild workload not found"}
  STEP: Admit workload @ 01/30/25 18:22:17.065
  2025-01-30T18:22:17.066684152Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:599	Workload create event	{"workload": {"name":"test-workload","namespace":"pod-s7lrj"}, "queue": "lq", "status": "pending"}
  2025-01-30T18:22:17.067269334Z	LEVEL(-2)	core/workload_controller.go:144	Reconciling Workload	{"controller": "workload", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Workload", "Workload": {"name":"test-workload","namespace":"pod-s7lrj"}, "namespace": "pod-s7lrj", "name": "test-workload", "reconcileID": "f1c9b50c-e82b-4bf1-bbdc-99d327bff147", "workload": {"name":"test-workload","namespace":"pod-s7lrj"}}
  2025-01-30T18:22:17.084961047Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:689	Workload update event	{"workload": {"name":"test-workload","namespace":"pod-s7lrj"}, "queue": "lq", "status": "quotaReserved", "prevStatus": "pending", "clusterQueue": "cluster-queue"}
  2025-01-30T18:22:17.084970747Z	LEVEL(-2)	jobframework/reconciler.go:355	Reconciling Job	{"controller": "v1_pod", "namespace": "group/pod-s7lrj", "name": "test-group", "reconcileID": "2bce43b5-34ee-46c0-bd1e-db604741f29c", "job": "group/pod-s7lrj/test-group", "gvk": "/v1, Kind=Pod"}
  2025-01-30T18:22:17.085704083Z	LEVEL(-2)	core/workload_controller.go:144	Reconciling Workload	{"controller": "workload", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Workload", "Workload": {"name":"test-workload","namespace":"pod-s7lrj"}, "namespace": "pod-s7lrj", "name": "test-workload", "reconcileID": "f6cc3ded-1b44-442b-bf0b-65d4b3591417", "workload": {"name":"test-workload","namespace":"pod-s7lrj"}}
  2025-01-30T18:22:17.107255487Z	LEVEL(-3)	jobframework/reconciler.go:441	update reclaimable counts if implemented by the job	{"controller": "v1_pod", "namespace": "group/pod-s7lrj", "name": "test-group", "reconcileID": "2bce43b5-34ee-46c0-bd1e-db604741f29c", "job": "group/pod-s7lrj/test-group", "gvk": "/v1, Kind=Pod"}
  2025-01-30T18:22:17.1073829Z	LEVEL(-3)	jobframework/reconciler.go:530	Job is suspended and workload not yet admitted by a clusterQueue, nothing to do	{"controller": "v1_pod", "namespace": "group/pod-s7lrj", "name": "test-group", "reconcileID": "2bce43b5-34ee-46c0-bd1e-db604741f29c", "job": "group/pod-s7lrj/test-group", "gvk": "/v1, Kind=Pod"}
  2025-01-30T18:22:17.107367269Z	DEBUG	events	recorder/recorder.go:104	Added 1 owner reference(s)	{"type": "Normal", "object": {"kind":"Workload","namespace":"pod-s7lrj","name":"test-workload","uid":"6f24fbb1-7902-49cb-bdf4-e79c52364af7","apiVersion":"kueue.x-k8s.io/v1beta1","resourceVersion":"941"}, "reason": "OwnerReferencesAdded"}
  2025-01-30T18:22:17.109510554Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:689	Workload update event	{"workload": {"name":"test-workload","namespace":"pod-s7lrj"}, "queue": "lq", "status": "quotaReserved", "clusterQueue": "cluster-queue"}
  2025-01-30T18:22:17.109654607Z	ERROR	controller/controller.go:316	Reconciler error	{"controller": "workload", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Workload", "Workload": {"name":"test-workload","namespace":"pod-s7lrj"}, "namespace": "pod-s7lrj", "name": "test-workload", "reconcileID": "f6cc3ded-1b44-442b-bf0b-65d4b3591417", "error": "Operation cannot be fulfilled on workloads.kueue.x-k8s.io \"test-workload\": the object has been modified; please apply your changes to the latest version and try again"}
  2025-01-30T18:22:17.110095967Z	LEVEL(-2)	core/workload_controller.go:144	Reconciling Workload	{"controller": "workload", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Workload", "Workload": {"name":"test-workload","namespace":"pod-s7lrj"}, "namespace": "pod-s7lrj", "name": "test-workload", "reconcileID": "b21c2250-9824-442b-84fc-a5c45e1a8f25", "workload": {"name":"test-workload","namespace":"pod-s7lrj"}}
  STEP: Workload should not be finished @ 01/30/25 18:22:17.129
  2025-01-30T18:22:17.131547779Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:689	Workload update event	{"workload": {"name":"test-workload","namespace":"pod-s7lrj"}, "queue": "lq", "status": "admitted", "prevStatus": "quotaReserved", "clusterQueue": "cluster-queue"}
  2025-01-30T18:22:17.135124084Z	ERROR	controller/controller.go:316	Reconciler error	{"controller": "workload", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Workload", "Workload": {"name":"test-workload","namespace":"pod-s7lrj"}, "namespace": "pod-s7lrj", "name": "test-workload", "reconcileID": "b21c2250-9824-442b-84fc-a5c45e1a8f25", "error": "Operation cannot be fulfilled on workloads.kueue.x-k8s.io \"test-workload\": the object has been modified; please apply your changes to the latest version and try again"}
  2025-01-30T18:22:17.135505112Z	LEVEL(-2)	core/workload_controller.go:144	Reconciling Workload	{"controller": "workload", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Workload", "Workload": {"name":"test-workload","namespace":"pod-s7lrj"}, "namespace": "pod-s7lrj", "name": "test-workload", "reconcileID": "6b86f226-eaa8-4f46-9e1e-5ae44a0cc6df", "workload": {"name":"test-workload","namespace":"pod-s7lrj"}}
  2025-01-30T18:22:17.145886161Z	LEVEL(-2)	core/workload_controller.go:144	Reconciling Workload	{"controller": "workload", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Workload", "Workload": {"name":"test-workload","namespace":"pod-s7lrj"}, "namespace": "pod-s7lrj", "name": "test-workload", "reconcileID": "a5434005-0c3a-4d04-9f15-8c88fcc9ebc0", "workload": {"name":"test-workload","namespace":"pod-s7lrj"}}
  2025-01-30T18:22:18.067920732Z	LEVEL(-2)	core/localqueue_controller.go:109	Reconciling LocalQueue	{"controller": "localqueue", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "LocalQueue", "LocalQueue": {"name":"lq","namespace":"pod-s7lrj"}, "namespace": "pod-s7lrj", "name": "lq", "reconcileID": "3cb33328-bcc2-4a55-9240-d244c5cd7578", "localQueue": {"name":"lq","namespace":"pod-s7lrj"}}
  STEP: Checking the pod is unsuspended @ 01/30/25 18:22:18.13
  [FAILED] in [It] - /home/prow/go/src/kubernetes-sigs/kueue/test/integration/singlecluster/controller/jobs/pod/pod_controller_test.go:1655 @ 01/30/25 18:22:28.131
  2025-01-30T18:22:28.147685414Z	LEVEL(-2)	localqueue-reconciler	core/localqueue_controller.go:170	LocalQueue delete event	{"localQueue": {"name":"lq","namespace":"pod-s7lrj"}}
  2025-01-30T18:22:28.148319297Z	LEVEL(-2)	core/workload_controller.go:144	Reconciling Workload	{"controller": "workload", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Workload", "Workload": {"name":"test-workload","namespace":"pod-s7lrj"}, "namespace": "pod-s7lrj", "name": "test-workload", "reconcileID": "7fbec627-604e-4ba4-9bb0-bbb0750b9af7", "workload": {"name":"test-workload","namespace":"pod-s7lrj"}}
  2025-01-30T18:22:28.150451002Z	LEVEL(-2)	jobframework/reconciler.go:355	Reconciling Job	{"controller": "v1_pod", "namespace": "group/pod-s7lrj", "name": "test-group", "reconcileID": "2f1d2fb2-9a10-4793-8163-4914fb0cda3c", "job": "group/pod-s7lrj/test-group", "gvk": "/v1, Kind=Pod"}
  2025-01-30T18:22:28.150669787Z	LEVEL(-3)	jobframework/reconciler.go:441	update reclaimable counts if implemented by the job	{"controller": "v1_pod", "namespace": "group/pod-s7lrj", "name": "test-group", "reconcileID": "2f1d2fb2-9a10-4793-8163-4914fb0cda3c", "job": "group/pod-s7lrj/test-group", "gvk": "/v1, Kind=Pod"}
  2025-01-30T18:22:28.150747018Z	LEVEL(-2)	jobframework/reconciler.go:500	Job admitted, unsuspending	{"controller": "v1_pod", "namespace": "group/pod-s7lrj", "name": "test-group", "reconcileID": "2f1d2fb2-9a10-4793-8163-4914fb0cda3c", "job": "group/pod-s7lrj/test-group", "gvk": "/v1, Kind=Pod"}
  2025-01-30T18:22:28.150993993Z	LEVEL(-3)	pod/pod_controller.go:279	Starting pod in group	{"controller": "v1_pod", "namespace": "group/pod-s7lrj", "name": "test-group", "reconcileID": "2f1d2fb2-9a10-4793-8163-4914fb0cda3c", "job": "group/pod-s7lrj/test-group", "gvk": "/v1, Kind=Pod", "podInGroup": {"name":"test-pod-1","namespace":"pod-s7lrj"}}
  2025-01-30T18:22:28.164352185Z	LEVEL(-3)	expectations/store.go:59	Observed UID	{"pod": {"name":"test-pod-1","namespace":"pod-s7lrj"}, "store": "finalizedPods", "key": {"name":"test-group","namespace":"pod-s7lrj"}, "uid": "28511d54-995a-4b20-af11-239eca5d8ece"}
  2025-01-30T18:22:28.16460956Z	ERROR	jobframework/reconciler.go:503	Unsuspending job	{"controller": "v1_pod", "namespace": "group/pod-s7lrj", "name": "test-group", "reconcileID": "2f1d2fb2-9a10-4793-8163-4914fb0cda3c", "job": "group/pod-s7lrj/test-group", "gvk": "/v1, Kind=Pod", "error": "pods \"test-pod-1\" not found"}
  2025-01-30T18:22:28.164809525Z	ERROR	controller/controller.go:316	Reconciler error	{"controller": "v1_pod", "namespace": "group/pod-s7lrj", "name": "test-group", "reconcileID": "2f1d2fb2-9a10-4793-8163-4914fb0cda3c", "error": "pods \"test-pod-1\" not found"}
  2025-01-30T18:22:28.175692064Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:634	Workload delete event	{"workload": {"name":"test-workload","namespace":"pod-s7lrj"}, "queue": "lq", "status": "admitted"}
  STEP: stopping the manager @ 01/30/25 18:22:29.224

```
Some observations:
- the workload was created very fast in ` 2025-01-30T18:22:17.066` and observed, so I don't believe that the waiting for workload as proposed in the PR https://github.com/kubernetes-sigs/kueue/pull/4208 by 1s fixes the problem. I think it just swipes the problem under the carpet by changing timing so that it works "in practice in the test". Returning error triggers the reconcile just immediately after, but reconciling after 1s gives more time.
- the last reconcile log is `2025-01-30T18:22:17.1073829Z	LEVEL(-3)	jobframework/reconciler.go:530	Job is suspended and workload not yet admitted by a clusterQueue, nothing to do` which returned without error

I'm not yet sure what exactly the problem is, but I suspect this is some race condition when using prebuilt-workload with Pod Groups which needs to be understood better.
