# Issue #688: Flaky test: Workload controller with scheduler when When LimitRanges are defined Should use the range defined default requests, if provided

**Summary**: Flaky test: Workload controller with scheduler when When LimitRanges are defined Should use the range defined default requests, if provided

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/688

**Last updated**: 2023-04-25T12:40:58Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@mcariatm](https://github.com/mcariatm)
- **Created**: 2023-04-07T07:13:04Z
- **Updated**: 2023-04-25T12:40:58Z
- **Closed**: 2023-04-25T12:40:58Z
- **Labels**: `kind/bug`
- **Assignees**: [@mcariatm](https://github.com/mcariatm)
- **Comments**: 6

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
Flaky integration test: : Workload controller with scheduler when When LimitRanges are defined Should use the range defined default requests, if provided
**What you expected to happen**:

**How to reproduce it (as minimally and precisely as possible)**:
Randomly when run the integration tests on my local machine.

**Anything else we need to know?**:
`
> Enter [BeforeEach] Workload controller with scheduler - /mnt/c/projects/kueue/test/integration/scheduler/workload_controller_test.go:54 @ 04/06/23 22:24:56.247
< Exit [BeforeEach] Workload controller with scheduler - /mnt/c/projects/kueue/test/integration/scheduler/workload_controller_test.go:54 @ 04/06/23 22:24:56.249 (1ms)
> Enter [BeforeEach] when When LimitRanges are defined - /mnt/c/projects/kueue/test/integration/scheduler/workload_controller_test.go:185 @ 04/06/23 22:24:56.249
2023-04-06T22:24:56.266732943+03:00	DEBUG	controller-runtime.webhook.webhooks	admission/http.go:96	received request	{"webhook": "/mutate-kueue-x-k8s-io-v1beta1-resourceflavor", "UID": "88e574f1-bc5e-4812-be64-25961d5d01d2", "kind": "kueue.x-k8s.io/v1beta1, Kind=ResourceFlavor", "resource": {"group":"kueue.x-k8s.io","version":"v1beta1","resource":"resourceflavors"}}
2023-04-06T22:24:56.266860944+03:00	DEBUG	controller-runtime.webhook.webhooks	admission/http.go:143	wrote response	{"webhook": "/mutate-kueue-x-k8s-io-v1beta1-resourceflavor", "code": 200, "reason": "", "UID": "88e574f1-bc5e-4812-be64-25961d5d01d2", "allowed": true}
2023-04-06T22:24:56.267493055+03:00	DEBUG	controller-runtime.webhook.webhooks	admission/http.go:96	received request	{"webhook": "/validate-kueue-x-k8s-io-v1beta1-resourceflavor", "UID": "7e3bd766-987a-491a-b1bc-3988c912534a", "kind": "kueue.x-k8s.io/v1beta1, Kind=ResourceFlavor", "resource": {"group":"kueue.x-k8s.io","version":"v1beta1","resource":"resourceflavors"}}
2023-04-06T22:24:56.267570526+03:00	DEBUG	controller-runtime.webhook.webhooks	admission/http.go:143	wrote response	{"webhook": "/validate-kueue-x-k8s-io-v1beta1-resourceflavor", "code": 200, "reason": "", "UID": "7e3bd766-987a-491a-b1bc-3988c912534a", "allowed": true}
2023-04-06T22:24:56.268598548+03:00	LEVEL(-2)	resourceflavor-reconciler	core/resourceflavor_controller.go:127	ResourceFlavor create event	{"resourceFlavor": {"name":"on-demand"}}
2023-04-06T22:24:56.268663519+03:00	LEVEL(-2)	core/resourceflavor_controller.go:78	Reconciling ResourceFlavor	{"controller": "resourceflavor", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "ResourceFlavor", "ResourceFlavor": {"name":"on-demand"}, "namespace": "", "name": "on-demand", "reconcileID": "274f1e86-1529-4f87-b503-4df0877a3dd6", "resourceFlavor": {"name":"on-demand"}}
2023-04-06T22:24:56.268673618+03:00	LEVEL(-2)	cluster-queue-reconciler	core/clusterqueue_controller.go:231	Got generic event	{"obj": {"name":"on-demand"}, "kind": "/, Kind="}
2023-04-06T22:24:56.269544283+03:00	DEBUG	controller-runtime.webhook.webhooks	admission/http.go:96	received request	{"webhook": "/mutate-kueue-x-k8s-io-v1beta1-clusterqueue", "UID": "d7341d60-6820-456a-83db-d596964d821b", "kind": "kueue.x-k8s.io/v1beta1, Kind=ClusterQueue", "resource": {"group":"kueue.x-k8s.io","version":"v1beta1","resource":"clusterqueues"}}
2023-04-06T22:24:56.269691153+03:00	DEBUG	controller-runtime.webhook.webhooks	admission/http.go:143	wrote response	{"webhook": "/mutate-kueue-x-k8s-io-v1beta1-clusterqueue", "code": 200, "reason": "", "UID": "d7341d60-6820-456a-83db-d596964d821b", "allowed": true}
2023-04-06T22:24:56.270428392+03:00	DEBUG	controller-runtime.webhook.webhooks	admission/http.go:96	received request	{"webhook": "/validate-kueue-x-k8s-io-v1beta1-clusterqueue", "UID": "b7d04674-e81a-48e1-9925-760c63ea01e0", "kind": "kueue.x-k8s.io/v1beta1, Kind=ClusterQueue", "resource": {"group":"kueue.x-k8s.io","version":"v1beta1","resource":"clusterqueues"}}
2023-04-06T22:24:56.270512831+03:00	DEBUG	controller-runtime.webhook.webhooks	admission/http.go:143	wrote response	{"webhook": "/validate-kueue-x-k8s-io-v1beta1-clusterqueue", "code": 200, "reason": "", "UID": "b7d04674-e81a-48e1-9925-760c63ea01e0", "allowed": true}
2023-04-06T22:24:56.27185798+03:00	LEVEL(-2)	cluster-queue-reconciler	core/clusterqueue_controller.go:175	ClusterQueue create event	{"clusterQueue": {"name":"clusterqueue"}}
2023-04-06T22:24:56.271959802+03:00	LEVEL(-2)	core/clusterqueue_controller.go:90	Reconciling ClusterQueue	{"controller": "clusterqueue", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "ClusterQueue", "ClusterQueue": {"name":"clusterqueue"}, "namespace": "", "name": "clusterqueue", "reconcileID": "e48a1baa-1379-476b-96c1-13f126ac2bb7", "clusterQueue": {"name":"clusterqueue"}}
2023-04-06T22:24:56.272783293+03:00	DEBUG	controller-runtime.webhook.webhooks	admission/http.go:96	received request	{"webhook": "/validate-kueue-x-k8s-io-v1beta1-localqueue", "UID": "201e45c1-721c-478b-b18f-a2f00d75190f", "kind": "kueue.x-k8s.io/v1beta1, Kind=LocalQueue", "resource": {"group":"kueue.x-k8s.io","version":"v1beta1","resource":"localqueues"}}
2023-04-06T22:24:56.272857629+03:00	DEBUG	controller-runtime.webhook.webhooks	admission/http.go:143	wrote response	{"webhook": "/validate-kueue-x-k8s-io-v1beta1-localqueue", "code": 200, "reason": "", "UID": "201e45c1-721c-478b-b18f-a2f00d75190f", "allowed": true}
2023-04-06T22:24:56.273804839+03:00	LEVEL(-2)	localqueue-reconciler	core/localqueue_controller.go:117	LocalQueue create event	{"localQueue": {"name":"queue","namespace":"core-workload-nrb62"}}
< Exit [BeforeEach] when When LimitRanges are defined - /mnt/c/projects/kueue/test/integration/scheduler/workload_controller_test.go:185 @ 04/06/23 22:24:56.273 (25ms)
> Enter [It] Should use the range defined default requests, if provided - /mnt/c/projects/kueue/test/integration/scheduler/workload_controller_test.go:203 @ 04/06/23 22:24:56.273
2023-04-06T22:24:56.273879077+03:00	LEVEL(-2)	core/localqueue_controller.go:92	Reconciling LocalQueue	{"controller": "localqueue", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "LocalQueue", "LocalQueue": {"name":"queue","namespace":"core-workload-nrb62"}, "namespace": "core-workload-nrb62", "name": "queue", "reconcileID": "fa1e2168-9189-4876-afa0-cdbdd30703b8", "localQueue": {"name":"queue","namespace":"core-workload-nrb62"}}
STEP: Create and wait for workload admission - /mnt/c/projects/kueue/test/integration/scheduler/workload_controller_test.go:204 @ 04/06/23 22:24:56.273
2023-04-06T22:24:56.27435365+03:00	LEVEL(-2)	cluster-queue-reconciler	core/clusterqueue_controller.go:214	ClusterQueue update event	{"clusterQueue": {"name":"clusterqueue"}}
2023-04-06T22:24:56.274422436+03:00	LEVEL(-2)	core/clusterqueue_controller.go:90	Reconciling ClusterQueue	{"controller": "clusterqueue", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "ClusterQueue", "ClusterQueue": {"name":"clusterqueue"}, "namespace": "", "name": "clusterqueue", "reconcileID": "9ecf1fce-8053-487c-813d-02fef028771c", "clusterQueue": {"name":"clusterqueue"}}
2023-04-06T22:24:56.274858086+03:00	DEBUG	controller-runtime.webhook.webhooks	admission/http.go:96	received request	{"webhook": "/mutate-kueue-x-k8s-io-v1beta1-workload", "UID": "d900fd9e-e033-4e05-9d6b-2c25942bad7b", "kind": "kueue.x-k8s.io/v1beta1, Kind=Workload", "resource": {"group":"kueue.x-k8s.io","version":"v1beta1","resource":"workloads"}}
2023-04-06T22:24:56.274993578+03:00	DEBUG	controller-runtime.webhook.webhooks	admission/http.go:143	wrote response	{"webhook": "/mutate-kueue-x-k8s-io-v1beta1-workload", "code": 200, "reason": "", "UID": "d900fd9e-e033-4e05-9d6b-2c25942bad7b", "allowed": true}
2023-04-06T22:24:56.275627481+03:00	LEVEL(-2)	localqueue-reconciler	core/localqueue_controller.go:147	Queue update event	{"localQueue": {"name":"queue","namespace":"core-workload-nrb62"}}
2023-04-06T22:24:56.275683756+03:00	DEBUG	controller-runtime.webhook.webhooks	admission/http.go:96	received request	{"webhook": "/validate-kueue-x-k8s-io-v1beta1-workload", "UID": "b490e8a2-f5a1-4cba-b417-36d311db45d7", "kind": "kueue.x-k8s.io/v1beta1, Kind=Workload", "resource": {"group":"kueue.x-k8s.io","version":"v1beta1","resource":"workloads"}}
2023-04-06T22:24:56.275788521+03:00	DEBUG	controller-runtime.webhook.webhooks	admission/http.go:143	wrote response	{"webhook": "/validate-kueue-x-k8s-io-v1beta1-workload", "code": 200, "reason": "", "UID": "b490e8a2-f5a1-4cba-b417-36d311db45d7", "allowed": true}
2023-04-06T22:24:56.275813064+03:00	LEVEL(-2)	core/localqueue_controller.go:92	Reconciling LocalQueue	{"controller": "localqueue", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "LocalQueue", "LocalQueue": {"name":"queue","namespace":"core-workload-nrb62"}, "namespace": "core-workload-nrb62", "name": "queue", "reconcileID": "fbdad9ff-ca95-4509-a5e3-b29b38244fba", "localQueue": {"name":"queue","namespace":"core-workload-nrb62"}}
2023-04-06T22:24:56.277082324+03:00	LEVEL(-2)	workload-reconciler	core/workload_controller.go:186	Workload create event	{"workload": {"name":"one","namespace":"core-workload-nrb62"}, "queue": "queue", "status": "pending"}
2023-04-06T22:24:56.277157027+03:00	LEVEL(-2)	core/workload_controller.go:128	Reconciling Workload	{"controller": "workload", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Workload", "Workload": {"name":"one","namespace":"core-workload-nrb62"}, "namespace": "core-workload-nrb62", "name": "one", "reconcileID": "20b81e47-d2f7-4c59-8c2e-3c3bb9d56c86", "workload": {"name":"one","namespace":"core-workload-nrb62"}}
2023-04-06T22:24:56.277155093+03:00	LEVEL(-3)	localqueue-reconciler	core/localqueue_controller.go:159	Got Workload event	{"workload": {"name":"one","namespace":"core-workload-nrb62"}}
2023-04-06T22:24:56.277164863+03:00	LEVEL(-2)	cluster-queue-reconciler	core/clusterqueue_controller.go:231	Got generic event	{"obj": {"name":"one","namespace":"core-workload-nrb62"}, "kind": "/, Kind="}
2023-04-06T22:24:56.277179261+03:00	LEVEL(-3)	scheduler	queue/manager.go:443	Obtained ClusterQueue heads	{"count": 1}
2023-04-06T22:24:56.277207814+03:00	LEVEL(-2)	scheduler	scheduler/scheduler.go:279	Workload assumed in the cache	{"workload": {"name":"one","namespace":"core-workload-nrb62"}, "clusterQueue": {"name":"clusterqueue"}}
2023-04-06T22:24:56.277224854+03:00	LEVEL(-3)	scheduler	scheduler/scheduler.go:195	Workload evaluated for admission	{"workload": {"name":"one","namespace":"core-workload-nrb62"}, "clusterQueue": {"name":"clusterqueue"}, "status": "assumed", "reason": ""}
2023-04-06T22:24:56.277283213+03:00	LEVEL(-3)	scheduler	queue/manager.go:443	Obtained ClusterQueue heads	{"count": 0}
2023-04-06T22:24:56.277520604+03:00	LEVEL(-2)	localqueue-reconciler	core/localqueue_controller.go:147	Queue update event	{"localQueue": {"name":"queue","namespace":"core-workload-nrb62"}}
2023-04-06T22:24:56.277576067+03:00	LEVEL(-2)	core/localqueue_controller.go:92	Reconciling LocalQueue	{"controller": "localqueue", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "LocalQueue", "LocalQueue": {"name":"queue","namespace":"core-workload-nrb62"}, "namespace": "core-workload-nrb62", "name": "queue", "reconcileID": "3e59449e-8a97-41b8-8990-8052531aaba2", "localQueue": {"name":"queue","namespace":"core-workload-nrb62"}}
2023-04-06T22:24:56.278837849+03:00	DEBUG	controller-runtime.webhook.webhooks	admission/http.go:96	received request	{"webhook": "/validate-kueue-x-k8s-io-v1beta1-workload", "UID": "52ef9450-e78c-49f0-b9fb-1e0148781fdc", "kind": "kueue.x-k8s.io/v1beta1, Kind=Workload", "resource": {"group":"kueue.x-k8s.io","version":"v1beta1","resource":"workloads"}}
2023-04-06T22:24:56.278977411+03:00	DEBUG	controller-runtime.webhook.webhooks	admission/http.go:143	wrote response	{"webhook": "/validate-kueue-x-k8s-io-v1beta1-workload", "code": 200, "reason": "", "UID": "52ef9450-e78c-49f0-b9fb-1e0148781fdc", "allowed": true}
2023-04-06T22:24:56.27920411+03:00	LEVEL(-2)	localqueue-reconciler	core/localqueue_controller.go:147	Queue update event	{"localQueue": {"name":"queue","namespace":"core-workload-nrb62"}}
2023-04-06T22:24:56.279340681+03:00	LEVEL(-2)	core/localqueue_controller.go:92	Reconciling LocalQueue	{"controller": "localqueue", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "LocalQueue", "LocalQueue": {"name":"queue","namespace":"core-workload-nrb62"}, "namespace": "core-workload-nrb62", "name": "queue", "reconcileID": "b19fd076-0f7e-48ba-85d4-f5c61ddc7c8f", "localQueue": {"name":"queue","namespace":"core-workload-nrb62"}}
2023-04-06T22:24:56.279889206+03:00	LEVEL(-2)	workload-reconciler	core/workload_controller.go:275	Workload update event	{"workload": {"name":"one","namespace":"core-workload-nrb62"}, "queue": "queue", "status": "admitted", "prevStatus": "pending", "clusterQueue": "clusterqueue"}
2023-04-06T22:24:56.279955209+03:00	LEVEL(-2)	core/workload_controller.go:128	Reconciling Workload	{"controller": "workload", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Workload", "Workload": {"name":"one","namespace":"core-workload-nrb62"}, "namespace": "core-workload-nrb62", "name": "one", "reconcileID": "1047a987-72dd-4fb1-93e3-8e795ba3cd32", "workload": {"name":"one","namespace":"core-workload-nrb62"}}
2023-04-06T22:24:56.279980894+03:00	LEVEL(-2)	cluster-queue-reconciler	core/clusterqueue_controller.go:231	Got generic event	{"obj": {"name":"one","namespace":"core-workload-nrb62"}, "kind": "/, Kind="}
2023-04-06T22:24:56.280001788+03:00	LEVEL(-3)	localqueue-reconciler	core/localqueue_controller.go:159	Got Workload event	{"workload": {"name":"one","namespace":"core-workload-nrb62"}}
2023-04-06T22:24:56.280092231+03:00	LEVEL(-2)	scheduler	scheduler/scheduler.go:295	Workload successfully admitted and assigned flavors	{"workload": {"name":"one","namespace":"core-workload-nrb62"}, "clusterQueue": {"name":"clusterqueue"}}
2023-04-06T22:24:56.28011425+03:00	DEBUG	events	recorder/recorder.go:103	Admitted by ClusterQueue clusterqueue, wait time was 0.280s	{"type": "Normal", "object": {"kind":"Workload","namespace":"core-workload-nrb62","name":"one","uid":"25b07d74-77ba-4433-ad17-de0db034e2ce","apiVersion":"kueue.x-k8s.io/v1beta1","resourceVersion":"931"}, "reason": "Admitted"}
END STEP: Create and wait for workload admission - /mnt/c/projects/kueue/test/integration/scheduler/workload_controller_test.go:204 @ 04/06/23 22:24:56.531 (257ms)
STEP: Check queue resource consumption - /mnt/c/projects/kueue/test/integration/scheduler/workload_controller_test.go:219 @ 04/06/23 22:24:56.531
2023-04-06T22:24:57.278495333+03:00	LEVEL(-2)	core/localqueue_controller.go:92	Reconciling LocalQueue	{"controller": "localqueue", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "LocalQueue", "LocalQueue": {"name":"queue","namespace":"core-workload-nrb62"}, "namespace": "core-workload-nrb62", "name": "queue", "reconcileID": "0a3a3d0d-e87b-409d-a539-342c511616e0", "localQueue": {"name":"queue","namespace":"core-workload-nrb62"}}
2023-04-06T22:24:57.278498624+03:00	LEVEL(-2)	core/clusterqueue_controller.go:90	Reconciling ClusterQueue	{"controller": "clusterqueue", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "ClusterQueue", "ClusterQueue": {"name":"clusterqueue"}, "namespace": "", "name": "clusterqueue", "reconcileID": "4f622e04-a774-46f8-a9d8-cb8a1a0ba3a3", "clusterQueue": {"name":"clusterqueue"}}
2023-04-06T22:24:57.284179817+03:00	LEVEL(-2)	cluster-queue-reconciler	core/clusterqueue_controller.go:214	ClusterQueue update event	{"clusterQueue": {"name":"clusterqueue"}}
2023-04-06T22:24:57.284437941+03:00	LEVEL(-2)	core/clusterqueue_controller.go:90	Reconciling ClusterQueue	{"controller": "clusterqueue", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "ClusterQueue", "ClusterQueue": {"name":"clusterqueue"}, "namespace": "", "name": "clusterqueue", "reconcileID": "39ee8d3d-638a-4431-9538-9cfcf5da582c", "clusterQueue": {"name":"clusterqueue"}}
END STEP: Check queue resource consumption - /mnt/c/projects/kueue/test/integration/scheduler/workload_controller_test.go:219 @ 04/06/23 22:25:26.531 (30.001s)
[FAILED] Timed out after 30.000s.
  v1beta1.ClusterQueueStatus{
  	FlavorsUsage: []v1beta1.FlavorUsage{
  		{
  			Name: "on-demand",
  			Resources: []v1beta1.ResourceUsage{
  				{
  					Name:     s"cpu",
\- 					Total:    resource.Quantity{i: resource.int64Amount{value: 3}, s: "3", Format: "DecimalSI"},
\+ 					Total:    resource.Quantity{s: "0", Format: "DecimalSI"},
  					Borrowed: {},
  				},
  			},
  		},
  	},
  	PendingWorkloads:  0,
  	AdmittedWorkloads: 1,
  	... // 1 ignored field
  }
In [It] at: /mnt/c/projects/kueue/test/integration/scheduler/workload_controller_test.go:223 @ 04/06/23 22:25:26.531
< Exit [It] Should use the range defined default requests, if provided - /mnt/c/projects/kueue/test/integration/scheduler/workload_controller_test.go:203 @ 04/06/23 22:25:26.531 (30.258s)

> Enter [AfterEach] when When LimitRanges are defined - /mnt/c/projects/kueue/test/integration/scheduler/workload_controller_test.go:197 @ 04/06/23 22:25:26.531
2023-04-06T22:25:26.535694859+03:00	LEVEL(-2)	localqueue-reconciler	core/localqueue_controller.go:134	LocalQueue delete event	{"localQueue": {"name":"queue","namespace":"core-workload-nrb62"}}
2023-04-06T22:25:26.53803426+03:00	LEVEL(-2)	workload-reconciler	core/workload_controller.go:220	Workload delete event	{"workload": {"name":"one","namespace":"core-workload-nrb62"}, "queue": "queue", "status": "admitted"}
2023-04-06T22:25:26.538100878+03:00	LEVEL(-3)	localqueue-reconciler	core/localqueue_controller.go:159	Got Workload event	{"workload": {"name":"one","namespace":"core-workload-nrb62"}}
2023-04-06T22:25:26.538126255+03:00	LEVEL(-2)	cluster-queue-reconciler	core/clusterqueue_controller.go:231	Got generic event	{"obj": {"name":"one","namespace":"core-workload-nrb62"}, "kind": "/, Kind="}
2023-04-06T22:25:26.542069632+03:00	LEVEL(-2)	resourceflavor-reconciler	core/resourceflavor_controller.go:165	ResourceFlavor update event	{"resourceFlavor": {"name":"on-demand"}}
2023-04-06T22:25:26.54212408+03:00	LEVEL(-2)	core/resourceflavor_controller.go:78	Reconciling ResourceFlavor	{"controller": "resourceflavor", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "ResourceFlavor", "ResourceFlavor": {"name":"on-demand"}, "namespace": "", "name": "on-demand", "reconcileID": "b9256d55-4899-4b5d-83db-f0c16c2fbe59", "resourceFlavor": {"name":"on-demand"}}
2023-04-06T22:25:26.542117702+03:00	LEVEL(-2)	cluster-queue-reconciler	core/clusterqueue_controller.go:231	Got generic event	{"obj": {"name":"on-demand"}, "kind": "/, Kind="}
2023-04-06T22:25:26.54214003+03:00	LEVEL(-3)	core/resourceflavor_controller.go:92	resourceFlavor is still in use	{"controller": "resourceflavor", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "ResourceFlavor", "ResourceFlavor": {"name":"on-demand"}, "namespace": "", "name": "on-demand", "reconcileID": "b9256d55-4899-4b5d-83db-f0c16c2fbe59", "resourceFlavor": {"name":"on-demand"}, "ClusterQueues": ["clusterqueue"]}
2023-04-06T22:25:26.542180818+03:00	LEVEL(-2)	core/clusterqueue_controller.go:90	Reconciling ClusterQueue	{"controller": "clusterqueue", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "ClusterQueue", "ClusterQueue": {"name":"clusterqueue"}, "namespace": "", "name": "clusterqueue", "reconcileID": "01591fa8-76d7-4ebd-8be4-5dd06cba70f5", "clusterQueue": {"name":"clusterqueue"}}
2023-04-06T22:25:26.543883801+03:00	LEVEL(-2)	cluster-queue-reconciler	core/clusterqueue_controller.go:214	ClusterQueue update event	{"clusterQueue": {"name":"clusterqueue"}}
2023-04-06T22:25:26.544754697+03:00	ERROR	controller/controller.go:329	Reconciler error	{"controller": "clusterqueue", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "ClusterQueue", "ClusterQueue": {"name":"clusterqueue"}, "namespace": "", "name": "clusterqueue", "reconcileID": "01591fa8-76d7-4ebd-8be4-5dd06cba70f5", "error": "Operation cannot be fulfilled on clusterqueues.kueue.x-k8s.io \"clusterqueue\": the object has been modified; please apply your changes to the latest version and try again"}
sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).reconcileHandler
	/home/mcaria/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.14.5/pkg/internal/controller/controller.go:329
sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).processNextWorkItem
	/home/mcaria/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.14.5/pkg/internal/controller/controller.go:274
sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).Start.func2.2
	/home/mcaria/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.14.5/pkg/internal/controller/controller.go:235
2023-04-06T22:25:26.544805526+03:00	LEVEL(-2)	core/clusterqueue_controller.go:90	Reconciling ClusterQueue	{"controller": "clusterqueue", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "ClusterQueue", "ClusterQueue": {"name":"clusterqueue"}, "namespace": "", "name": "clusterqueue", "reconcileID": "35d404dd-717b-45c1-a976-cb1b205fbb49", "clusterQueue": {"name":"clusterqueue"}}
2023-04-06T22:25:26.546298751+03:00	DEBUG	controller-runtime.webhook.webhooks	admission/http.go:96	received request	{"webhook": "/validate-kueue-x-k8s-io-v1beta1-clusterqueue", "UID": "5503f1d5-f140-438a-948c-366f48169bcc", "kind": "kueue.x-k8s.io/v1beta1, Kind=ClusterQueue", "resource": {"group":"kueue.x-k8s.io","version":"v1beta1","resource":"clusterqueues"}}
2023-04-06T22:25:26.546468362+03:00	DEBUG	controller-runtime.webhook.webhooks	admission/http.go:143	wrote response	{"webhook": "/validate-kueue-x-k8s-io-v1beta1-clusterqueue", "code": 200, "reason": "", "UID": "5503f1d5-f140-438a-948c-366f48169bcc", "allowed": true}
2023-04-06T22:25:26.547995589+03:00	LEVEL(-2)	cluster-queue-reconciler	core/clusterqueue_controller.go:195	ClusterQueue delete event	{"clusterQueue": {"name":"clusterqueue"}}
2023-04-06T22:25:26.548124373+03:00	LEVEL(-2)	resourceflavor-reconciler	core/resourceflavor_controller.go:178	Got generic event	{"obj": {"name":"clusterqueue"}, "kind": "/, Kind="}
2023-04-06T22:25:26.54818366+03:00	LEVEL(-2)	core/resourceflavor_controller.go:78	Reconciling ResourceFlavor	{"controller": "resourceflavor", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "ResourceFlavor", "ResourceFlavor": {"name":"on-demand"}, "namespace": "", "name": "on-demand", "reconcileID": "a2175e03-5858-4f25-aaf6-cb1b62bbea50", "resourceFlavor": {"name":"on-demand"}}
2023-04-06T22:25:26.549148092+03:00	DEBUG	controller-runtime.webhook.webhooks	admission/http.go:96	received request	{"webhook": "/validate-kueue-x-k8s-io-v1beta1-resourceflavor", "UID": "cc7ea7e4-12cd-45f6-b494-4c20f59399ac", "kind": "kueue.x-k8s.io/v1beta1, Kind=ResourceFlavor", "resource": {"group":"kueue.x-k8s.io","version":"v1beta1","resource":"resourceflavors"}}
2023-04-06T22:25:26.549217866+03:00	DEBUG	controller-runtime.webhook.webhooks	admission/http.go:143	wrote response	{"webhook": "/validate-kueue-x-k8s-io-v1beta1-resourceflavor", "code": 200, "reason": "", "UID": "cc7ea7e4-12cd-45f6-b494-4c20f59399ac", "allowed": true}
2023-04-06T22:25:26.550269584+03:00	LEVEL(-2)	resourceflavor-reconciler	core/resourceflavor_controller.go:149	ResourceFlavor delete event	{"resourceFlavor": {"name":"on-demand"}}
2023-04-06T22:25:26.55029919+03:00	LEVEL(-2)	cluster-queue-reconciler	core/clusterqueue_controller.go:231	Got generic event	{"obj": {"name":"on-demand"}, "kind": "/, Kind="}
< Exit [AfterEach] when When LimitRanges are defined - /mnt/c/projects/kueue/test/integration/scheduler/workload_controller_test.go:197 @ 04/06/23 22:25:26.797 (267ms)
> Enter [AfterEach] Workload controller with scheduler - /mnt/c/projects/kueue/test/integration/scheduler/workload_controller_test.go:65 @ 04/06/23 22:25:26.798
< Exit [AfterEach] Workload controller with scheduler - /mnt/c/projects/kueue/test/integration/scheduler/workload_controller_test.go:65 @ 04/06/23 22:25:26.798 (0s)
`

**Environment**:
- Kubernetes version (use `kubectl version`): Client Version: v1.25.4, Kustomize Version: v4.5.7
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:  12th Gen Intel(R) Core(TM) i7-12700H   2.30 GHz, 16.0 GB, Windows 64-bit operating system, x64-based processor
- OS (e.g: `cat /etc/os-release`):
On WSL
PRETTY_NAME="Ubuntu 22.04 LTS"
NAME="Ubuntu"
VERSION_ID="22.04"
VERSION="22.04 LTS (Jammy Jellyfish)"
VERSION_CODENAME=jammy
ID=ubuntu
ID_LIKE=debian
HOME_URL="https://www.ubuntu.com/"
SUPPORT_URL="https://help.ubuntu.com/"
BUG_REPORT_URL="https://bugs.launchpad.net/ubuntu/"
PRIVACY_POLICY_URL="https://www.ubuntu.com/legal/terms-and-policies/privacy-policy"
UBUNTU_CODENAME=jammy
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@mcariatm](https://github.com/mcariatm) — 2023-04-07T07:55:38Z

/assign

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-04-11T12:17:56Z

@trasc any theories for this?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-04-11T13:56:03Z

One option suggested by @trasc is to implement #485.

Another option would be to manually preempt the workload in the test and let it be readmitted, until it satisfies all requirements.

### Comment by [@mcariatm](https://github.com/mcariatm) — 2023-04-13T08:11:40Z

I tried to wait for limitRange to be ready, but this didn't fix the issue.
BUT I found something interesting. I run the test in Linux using WSL and I use mounted project from my windows NTFS disk.
When I move the project from mounted to native path the issue disappear.
@alculquicondor do you have any ideas why it is happening? May I close this issue?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-04-13T12:26:57Z

The disk characteristics could only affect etcd performance. If etcd is slow, it's possible that the client is taking a while to receive the notification for the new LimitRange.
Still, I'm curious why waiting for the LimitRange to be available in the client wasn't enough.
But if we can't reproduce in the bots (which in general are already slow), then I'm ok closing this.

### Comment by [@mcariatm](https://github.com/mcariatm) — 2023-04-25T12:40:58Z

Happens only on mounted project in WSL from windows NTFS disk.
