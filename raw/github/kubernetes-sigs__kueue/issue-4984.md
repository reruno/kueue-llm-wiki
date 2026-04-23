# Issue #4984: [0.11] Flaky Test: Job controller interacting with Workload controller when waitForPodsReady is enabled

**Summary**: [0.11] Flaky Test: Job controller interacting with Workload controller when waitForPodsReady is enabled

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4984

**Last updated**: 2025-04-16T08:39:07Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-04-15T14:03:00Z
- **Updated**: 2025-04-16T08:39:07Z
- **Closed**: 2025-04-16T08:39:07Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@PBundyra](https://github.com/PBundyra)
- **Comments**: 6

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

Failed `Job Controller Suite: [It] Job controller interacting with Workload controller when waitForPodsReady is enabled when A tiny recoveryTimeout is configured and a pod fails should evict workload due waitForPodsReady.recoveryTimeout` on periodic CI.

https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-integration-release-0-11/1912124887439249408

```shell
{Expected success, but got an error:
    <*errors.StatusError | 0xc000b0f0e0>: 
    Operation cannot be fulfilled on jobs.batch "job": the object has been modified; please apply your changes to the latest version and try again
    {
        ErrStatus: {
            TypeMeta: {Kind: "", APIVersion: ""},
            ListMeta: {
                SelfLink: "",
                ResourceVersion: "",
                Continue: "",
                RemainingItemCount: nil,
            },
            Status: "Failure",
            Message: "Operation cannot be fulfilled on jobs.batch \"job\": the object has been modified; please apply your changes to the latest version and try again",
            Reason: "Conflict",
            Details: {Name: "job", Group: "batch", Kind: "jobs", UID: "", Causes: nil, RetryAfterSeconds: 0},
            Code: 409,
        },
    } failed [FAILED] Expected success, but got an error:
    <*errors.StatusError | 0xc000b0f0e0>: 
    Operation cannot be fulfilled on jobs.batch "job": the object has been modified; please apply your changes to the latest version and try again
    {
        ErrStatus: {
            TypeMeta: {Kind: "", APIVersion: ""},
            ListMeta: {
                SelfLink: "",
                ResourceVersion: "",
                Continue: "",
                RemainingItemCount: nil,
            },
            Status: "Failure",
            Message: "Operation cannot be fulfilled on jobs.batch \"job\": the object has been modified; please apply your changes to the latest version and try again",
            Reason: "Conflict",
            Details: {Name: "job", Group: "batch", Kind: "jobs", UID: "", Causes: nil, RetryAfterSeconds: 0},
            Code: 409,
        },
    }
In [It] at: /home/prow/go/src/kubernetes-sigs/kueue/test/integration/singlecluster/controller/jobs/job/job_controller_test.go:2249 @ 04/15/25 12:52:53.812
}
```

**What you expected to happen**:

No errors.

**How to reproduce it (as minimally and precisely as possible)**:

https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-integration-release-0-11/1912124887439249408

**Anything else we need to know?**:

<img width="1019" alt="Image" src="https://github.com/user-attachments/assets/b881dbcf-b542-4a86-b471-c0577722db82" />

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-04-15T14:03:47Z

/kind flake

### Comment by [@mimowo](https://github.com/mimowo) — 2025-04-15T15:12:08Z

cc @PBundyra @mbobrovskyi in case you have some ideas about the root cause.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-04-16T07:21:34Z

Oh ,  I grepped the logs by the namespace

```
> cat build-log | grep core-jvmpf                                                                                                                           
  "level"=0 "msg"="Created namespace: core-jvmpf"
  2025-04-15T12:52:53.29838274Z	LEVEL(-2)	localqueue-reconciler	core/localqueue_controller.go:140	LocalQueue create event	{"localQueue": {"name":"lq","namespace":"core-jvmpf"}}
  2025-04-15T12:52:53.398847183Z	LEVEL(-2)	core/localqueue_controller.go:115	Reconcile LocalQueue	{"controller": "localqueue_controller", "namespace": "core-jvmpf", "name": "lq", "reconcileID": "95dedd86-268e-4349-bf9e-7ac091818f75"}
  2025-04-15T12:52:53.399297258Z	LEVEL(-2)	jobframework/reconciler.go:366	Reconciling Job	{"controller": "job", "controllerGroup": "batch", "controllerKind": "Job", "Job": {"name":"job","namespace":"core-jvmpf"}, "namespace": "core-jvmpf", "name": "job", "reconcileID": "e09561fd-f9b9-4bea-8118-9eb4f3dc2d87", "job": "core-jvmpf/job", "gvk": "batch/v1, Kind=Job"}
  2025-04-15T12:52:53.399477859Z	LEVEL(-3)	jobframework/reconciler.go:434	The workload is nil, handle job with no workload	{"controller": "job", "controllerGroup": "batch", "controllerKind": "Job", "Job": {"name":"job","namespace":"core-jvmpf"}, "namespace": "core-jvmpf", "name": "job", "reconcileID": "e09561fd-f9b9-4bea-8118-9eb4f3dc2d87", "job": "core-jvmpf/job", "gvk": "batch/v1, Kind=Job"}
  2025-04-15T12:52:53.408844607Z	LEVEL(-2)	core/localqueue_controller.go:115	Reconcile LocalQueue	{"controller": "localqueue_controller", "namespace": "core-jvmpf", "name": "lq", "reconcileID": "9e40d61d-e670-4900-97c8-cfcf99775636"}
  2025-04-15T12:52:53.40907619Z	LEVEL(-2)	localqueue-reconciler	core/localqueue_controller.go:173	Queue update event	{"localQueue": {"name":"lq","namespace":"core-jvmpf"}}
  2025-04-15T12:52:53.419053724Z	LEVEL(-2)	core/localqueue_controller.go:115	Reconcile LocalQueue	{"controller": "localqueue_controller", "namespace": "core-jvmpf", "name": "lq", "reconcileID": "c3d3be1a-8f7a-48fd-941e-dc712927410d"}
  2025-04-15T12:52:53.419710081Z	LEVEL(-2)	localqueue-reconciler	core/localqueue_controller.go:173	Queue update event	{"localQueue": {"name":"lq","namespace":"core-jvmpf"}}
  2025-04-15T12:52:53.42626793Z	ERROR	controller/controller.go:316	Reconciler error	{"controller": "localqueue_controller", "namespace": "core-jvmpf", "name": "lq", "reconcileID": "c3d3be1a-8f7a-48fd-941e-dc712927410d", "error": "Operation cannot be fulfilled on localqueues.kueue.x-k8s.io \"lq\": the object has been modified; please apply your changes to the latest version and try again"}
  2025-04-15T12:52:53.426636263Z	LEVEL(-2)	core/localqueue_controller.go:115	Reconcile LocalQueue	{"controller": "localqueue_controller", "namespace": "core-jvmpf", "name": "lq", "reconcileID": "8ba5d42a-a837-4ba0-b934-fb9c5407b2ba"}
  2025-04-15T12:52:53.437219945Z	LEVEL(-2)	core/localqueue_controller.go:115	Reconcile LocalQueue	{"controller": "localqueue_controller", "namespace": "core-jvmpf", "name": "lq", "reconcileID": "80b26259-b828-4be4-9fbe-1f64db2c5572"}
  2025-04-15T12:52:53.518620518Z	DEBUG	events	recorder/recorder.go:104	Created Workload: core-jvmpf/job-job-90988	{"type": "Normal", "object": {"kind":"Job","namespace":"core-jvmpf","name":"job","uid":"e2903a87-a6d6-4fe1-9005-5419217b1f6b","apiVersion":"batch/v1","resourceVersion":"299"}, "reason": "CreatedWorkload"}
  2025-04-15T12:52:53.520926082Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:601	Workload create event	{"workload": {"name":"job-job-90988","namespace":"core-jvmpf"}, "queue": "lq", "status": "pending"}
  2025-04-15T12:52:53.52171526Z	LEVEL(-2)	core/workload_controller.go:151	Reconcile Workload	{"controller": "workload_controller", "namespace": "core-jvmpf", "name": "job-job-90988", "reconcileID": "69e0db5d-c384-47ad-b196-55a6776a0a53"}
  2025-04-15T12:52:53.522945843Z	LEVEL(-2)	jobframework/reconciler.go:366	Reconciling Job	{"controller": "job", "controllerGroup": "batch", "controllerKind": "Job", "Job": {"name":"job","namespace":"core-jvmpf"}, "namespace": "core-jvmpf", "name": "job", "reconcileID": "a5ce76bb-beba-4890-92d7-28a9f0d7086f", "job": "core-jvmpf/job", "gvk": "batch/v1, Kind=Job"}
  2025-04-15T12:52:53.523358177Z	LEVEL(-3)	jobframework/reconciler.go:452	update reclaimable counts if implemented by the job	{"controller": "job", "controllerGroup": "batch", "controllerKind": "Job", "Job": {"name":"job","namespace":"core-jvmpf"}, "namespace": "core-jvmpf", "name": "job", "reconcileID": "a5ce76bb-beba-4890-92d7-28a9f0d7086f", "job": "core-jvmpf/job", "gvk": "batch/v1, Kind=Job"}
  2025-04-15T12:52:53.523455888Z	LEVEL(-3)	jobframework/reconciler.go:472	Handling a job when waitForPodsReady is enabled	{"controller": "job", "controllerGroup": "batch", "controllerKind": "Job", "Job": {"name":"job","namespace":"core-jvmpf"}, "namespace": "core-jvmpf", "name": "job", "reconcileID": "a5ce76bb-beba-4890-92d7-28a9f0d7086f", "job": "core-jvmpf/job", "gvk": "batch/v1, Kind=Job"}
  2025-04-15T12:52:53.523532329Z	LEVEL(-3)	jobframework/reconciler.go:475	Updating the PodsReady condition	{"controller": "job", "controllerGroup": "batch", "controllerKind": "Job", "Job": {"name":"job","namespace":"core-jvmpf"}, "namespace": "core-jvmpf", "name": "job", "reconcileID": "a5ce76bb-beba-4890-92d7-28a9f0d7086f", "job": "core-jvmpf/job", "gvk": "batch/v1, Kind=Job", "reason": "WaitForStart", "status": "False"}
  2025-04-15T12:52:53.541017382Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:680	Workload update event	{"workload": {"name":"job-job-90988","namespace":"core-jvmpf"}, "queue": "lq", "status": "pending"}
  2025-04-15T12:52:53.541708569Z	LEVEL(-2)	core/workload_controller.go:151	Reconcile Workload	{"controller": "workload_controller", "namespace": "core-jvmpf", "name": "job-job-90988", "reconcileID": "dd4646c0-070b-4f51-a891-536680a4f892"}
  2025-04-15T12:52:53.542385996Z	LEVEL(-2)	core/localqueue_controller.go:115	Reconcile LocalQueue	{"controller": "localqueue_controller", "namespace": "core-jvmpf", "name": "lq", "reconcileID": "3750f91d-3ba1-4744-af0b-2faf1fc08dde"}
  2025-04-15T12:52:53.546160066Z	LEVEL(-2)	jobframework/reconciler.go:366	Reconciling Job	{"controller": "job", "controllerGroup": "batch", "controllerKind": "Job", "Job": {"name":"job","namespace":"core-jvmpf"}, "namespace": "core-jvmpf", "name": "job", "reconcileID": "9b435cf2-e234-4eee-93e0-5bdd73364b44", "job": "core-jvmpf/job", "gvk": "batch/v1, Kind=Job"}
  2025-04-15T12:52:53.546596821Z	LEVEL(-3)	jobframework/reconciler.go:452	update reclaimable counts if implemented by the job	{"controller": "job", "controllerGroup": "batch", "controllerKind": "Job", "Job": {"name":"job","namespace":"core-jvmpf"}, "namespace": "core-jvmpf", "name": "job", "reconcileID": "9b435cf2-e234-4eee-93e0-5bdd73364b44", "job": "core-jvmpf/job", "gvk": "batch/v1, Kind=Job"}
  2025-04-15T12:52:53.546689682Z	LEVEL(-3)	jobframework/reconciler.go:472	Handling a job when waitForPodsReady is enabled	{"controller": "job", "controllerGroup": "batch", "controllerKind": "Job", "Job": {"name":"job","namespace":"core-jvmpf"}, "namespace": "core-jvmpf", "name": "job", "reconcileID": "9b435cf2-e234-4eee-93e0-5bdd73364b44", "job": "core-jvmpf/job", "gvk": "batch/v1, Kind=Job"}
  2025-04-15T12:52:53.546774963Z	LEVEL(-3)	jobframework/reconciler.go:483	No update for PodsReady condition	{"controller": "job", "controllerGroup": "batch", "controllerKind": "Job", "Job": {"name":"job","namespace":"core-jvmpf"}, "namespace": "core-jvmpf", "name": "job", "reconcileID": "9b435cf2-e234-4eee-93e0-5bdd73364b44", "job": "core-jvmpf/job", "gvk": "batch/v1, Kind=Job"}
  2025-04-15T12:52:53.546861323Z	LEVEL(-3)	jobframework/reconciler.go:543	Job is suspended and workload not yet admitted by a clusterQueue, nothing to do	{"controller": "job", "controllerGroup": "batch", "controllerKind": "Job", "Job": {"name":"job","namespace":"core-jvmpf"}, "namespace": "core-jvmpf", "name": "job", "reconcileID": "9b435cf2-e234-4eee-93e0-5bdd73364b44", "job": "core-jvmpf/job", "gvk": "batch/v1, Kind=Job"}
  2025-04-15T12:52:53.553792707Z	LEVEL(-2)	localqueue-reconciler	core/localqueue_controller.go:173	Queue update event	{"localQueue": {"name":"lq","namespace":"core-jvmpf"}}
  2025-04-15T12:52:53.554251421Z	LEVEL(-2)	core/localqueue_controller.go:115	Reconcile LocalQueue	{"controller": "localqueue_controller", "namespace": "core-jvmpf", "name": "lq", "reconcileID": "74c9bc58-aea7-437f-9952-9a83cacc47b6"}
  2025-04-15T12:52:53.760483081Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:680	Workload update event	{"workload": {"name":"job-job-90988","namespace":"core-jvmpf"}, "queue": "lq", "status": "quotaReserved", "prevStatus": "pending", "clusterQueue": "cq"}
  2025-04-15T12:52:53.760919246Z	LEVEL(-2)	jobframework/reconciler.go:366	Reconciling Job	{"controller": "job", "controllerGroup": "batch", "controllerKind": "Job", "Job": {"name":"job","namespace":"core-jvmpf"}, "namespace": "core-jvmpf", "name": "job", "reconcileID": "44620b08-efbf-4ca4-a405-eeca1375e0df", "job": "core-jvmpf/job", "gvk": "batch/v1, Kind=Job"}
  2025-04-15T12:52:53.76128692Z	LEVEL(-2)	core/workload_controller.go:151	Reconcile Workload	{"controller": "workload_controller", "namespace": "core-jvmpf", "name": "job-job-90988", "reconcileID": "92d35855-9b6c-4e00-918b-7449a949a14c"}
  2025-04-15T12:52:53.761366091Z	LEVEL(-3)	jobframework/reconciler.go:452	update reclaimable counts if implemented by the job	{"controller": "job", "controllerGroup": "batch", "controllerKind": "Job", "Job": {"name":"job","namespace":"core-jvmpf"}, "namespace": "core-jvmpf", "name": "job", "reconcileID": "44620b08-efbf-4ca4-a405-eeca1375e0df", "job": "core-jvmpf/job", "gvk": "batch/v1, Kind=Job"}
  2025-04-15T12:52:53.761459872Z	LEVEL(-3)	jobframework/reconciler.go:472	Handling a job when waitForPodsReady is enabled	{"controller": "job", "controllerGroup": "batch", "controllerKind": "Job", "Job": {"name":"job","namespace":"core-jvmpf"}, "namespace": "core-jvmpf", "name": "job", "reconcileID": "44620b08-efbf-4ca4-a405-eeca1375e0df", "job": "core-jvmpf/job", "gvk": "batch/v1, Kind=Job"}
  2025-04-15T12:52:53.761533042Z	LEVEL(-3)	jobframework/reconciler.go:483	No update for PodsReady condition	{"controller": "job", "controllerGroup": "batch", "controllerKind": "Job", "Job": {"name":"job","namespace":"core-jvmpf"}, "namespace": "core-jvmpf", "name": "job", "reconcileID": "44620b08-efbf-4ca4-a405-eeca1375e0df", "job": "core-jvmpf/job", "gvk": "batch/v1, Kind=Job"}
  2025-04-15T12:52:53.761611993Z	LEVEL(-3)	jobframework/reconciler.go:543	Job is suspended and workload not yet admitted by a clusterQueue, nothing to do	{"controller": "job", "controllerGroup": "batch", "controllerKind": "Job", "Job": {"name":"job","namespace":"core-jvmpf"}, "namespace": "core-jvmpf", "name": "job", "reconcileID": "44620b08-efbf-4ca4-a405-eeca1375e0df", "job": "core-jvmpf/job", "gvk": "batch/v1, Kind=Job"}
  2025-04-15T12:52:53.781526603Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:680	Workload update event	{"workload": {"name":"job-job-90988","namespace":"core-jvmpf"}, "queue": "lq", "status": "admitted", "prevStatus": "quotaReserved", "clusterQueue": "cq"}
  2025-04-15T12:52:53.788489996Z	LEVEL(-2)	jobframework/reconciler.go:366	Reconciling Job	{"controller": "job", "controllerGroup": "batch", "controllerKind": "Job", "Job": {"name":"job","namespace":"core-jvmpf"}, "namespace": "core-jvmpf", "name": "job", "reconcileID": "ae67cbec-ab36-4587-9541-dcd0b9e984ce", "job": "core-jvmpf/job", "gvk": "batch/v1, Kind=Job"}
  2025-04-15T12:52:53.789636068Z	LEVEL(-3)	jobframework/reconciler.go:452	update reclaimable counts if implemented by the job	{"controller": "job", "controllerGroup": "batch", "controllerKind": "Job", "Job": {"name":"job","namespace":"core-jvmpf"}, "namespace": "core-jvmpf", "name": "job", "reconcileID": "ae67cbec-ab36-4587-9541-dcd0b9e984ce", "job": "core-jvmpf/job", "gvk": "batch/v1, Kind=Job"}
  2025-04-15T12:52:53.789804479Z	LEVEL(-3)	jobframework/reconciler.go:472	Handling a job when waitForPodsReady is enabled	{"controller": "job", "controllerGroup": "batch", "controllerKind": "Job", "Job": {"name":"job","namespace":"core-jvmpf"}, "namespace": "core-jvmpf", "name": "job", "reconcileID": "ae67cbec-ab36-4587-9541-dcd0b9e984ce", "job": "core-jvmpf/job", "gvk": "batch/v1, Kind=Job"}
  2025-04-15T12:52:53.78989429Z	LEVEL(-3)	jobframework/reconciler.go:1202	Generating PodsReady condition	{"controller": "job", "controllerGroup": "batch", "controllerKind": "Job", "Job": {"name":"job","namespace":"core-jvmpf"}, "namespace": "core-jvmpf", "name": "job", "reconcileID": "ae67cbec-ab36-4587-9541-dcd0b9e984ce", "job": "core-jvmpf/job", "gvk": "batch/v1, Kind=Job", "Current PodsReady condition": "&Condition{Type:PodsReady,Status:False,ObservedGeneration:1,LastTransitionTime:2025-04-15 12:52:53 +0000 UTC,Reason:WaitForStart,Message:Not all pods are ready or succeeded,}", "Pods are ready": false}
  2025-04-15T12:52:53.790041412Z	LEVEL(-3)	jobframework/reconciler.go:483	No update for PodsReady condition	{"controller": "job", "controllerGroup": "batch", "controllerKind": "Job", "Job": {"name":"job","namespace":"core-jvmpf"}, "namespace": "core-jvmpf", "name": "job", "reconcileID": "ae67cbec-ab36-4587-9541-dcd0b9e984ce", "job": "core-jvmpf/job", "gvk": "batch/v1, Kind=Job"}
  2025-04-15T12:52:53.790142813Z	LEVEL(-2)	jobframework/reconciler.go:513	Job admitted, unsuspending	{"controller": "job", "controllerGroup": "batch", "controllerKind": "Job", "Job": {"name":"job","namespace":"core-jvmpf"}, "namespace": "core-jvmpf", "name": "job", "reconcileID": "ae67cbec-ab36-4587-9541-dcd0b9e984ce", "job": "core-jvmpf/job", "gvk": "batch/v1, Kind=Job"}
  2025-04-15T12:52:53.799617062Z	LEVEL(-2)	core/workload_controller.go:151	Reconcile Workload	{"controller": "workload_controller", "namespace": "core-jvmpf", "name": "job-job-90988", "reconcileID": "2fd37b23-c82e-4eaa-83df-49b7dad0ccdd"}
  2025-04-15T12:52:53.800114557Z	DEBUG	events	recorder/recorder.go:104	Admitted by ClusterQueue cq, wait time since reservation was 1s	{"type": "Normal", "object": {"kind":"Workload","namespace":"core-jvmpf","name":"job-job-90988","uid":"ddcf8e50-b3fe-41ba-adec-efbfccb6cc66","apiVersion":"kueue.x-k8s.io/v1beta1","resourceVersion":"309"}, "reason": "Admitted"}
  2025-04-15T12:52:53.802964137Z	DEBUG	events	recorder/recorder.go:104	Admitted by clusterQueue cq	{"type": "Normal", "object": {"kind":"Job","namespace":"core-jvmpf","name":"job","uid":"e2903a87-a6d6-4fe1-9005-5419217b1f6b","apiVersion":"batch/v1","resourceVersion":"311"}, "reason": "Started"}
  2025-04-15T12:52:53.80322118Z	LEVEL(-2)	jobframework/reconciler.go:366	Reconciling Job	{"controller": "job", "controllerGroup": "batch", "controllerKind": "Job", "Job": {"name":"job","namespace":"core-jvmpf"}, "namespace": "core-jvmpf", "name": "job", "reconcileID": "649320ec-7480-4cce-9a8b-0f9b1315d565", "job": "core-jvmpf/job", "gvk": "batch/v1, Kind=Job"}
  2025-04-15T12:52:53.803698595Z	LEVEL(-3)	jobframework/reconciler.go:452	update reclaimable counts if implemented by the job	{"controller": "job", "controllerGroup": "batch", "controllerKind": "Job", "Job": {"name":"job","namespace":"core-jvmpf"}, "namespace": "core-jvmpf", "name": "job", "reconcileID": "649320ec-7480-4cce-9a8b-0f9b1315d565", "job": "core-jvmpf/job", "gvk": "batch/v1, Kind=Job"}
  2025-04-15T12:52:53.803809496Z	LEVEL(-3)	jobframework/reconciler.go:472	Handling a job when waitForPodsReady is enabled	{"controller": "job", "controllerGroup": "batch", "controllerKind": "Job", "Job": {"name":"job","namespace":"core-jvmpf"}, "namespace": "core-jvmpf", "name": "job", "reconcileID": "649320ec-7480-4cce-9a8b-0f9b1315d565", "job": "core-jvmpf/job", "gvk": "batch/v1, Kind=Job"}
  2025-04-15T12:52:53.803891857Z	LEVEL(-3)	jobframework/reconciler.go:1202	Generating PodsReady condition	{"controller": "job", "controllerGroup": "batch", "controllerKind": "Job", "Job": {"name":"job","namespace":"core-jvmpf"}, "namespace": "core-jvmpf", "name": "job", "reconcileID": "649320ec-7480-4cce-9a8b-0f9b1315d565", "job": "core-jvmpf/job", "gvk": "batch/v1, Kind=Job", "Current PodsReady condition": "&Condition{Type:PodsReady,Status:False,ObservedGeneration:1,LastTransitionTime:2025-04-15 12:52:53 +0000 UTC,Reason:WaitForStart,Message:Not all pods are ready or succeeded,}", "Pods are ready": false}
  2025-04-15T12:52:53.804036628Z	LEVEL(-3)	jobframework/reconciler.go:483	No update for PodsReady condition	{"controller": "job", "controllerGroup": "batch", "controllerKind": "Job", "Job": {"name":"job","namespace":"core-jvmpf"}, "namespace": "core-jvmpf", "name": "job", "reconcileID": "649320ec-7480-4cce-9a8b-0f9b1315d565", "job": "core-jvmpf/job", "gvk": "batch/v1, Kind=Job"}
  2025-04-15T12:52:53.804133329Z	LEVEL(-3)	jobframework/reconciler.go:559	Job running with admitted workload, nothing to do	{"controller": "job", "controllerGroup": "batch", "controllerKind": "Job", "Job": {"name":"job","namespace":"core-jvmpf"}, "namespace": "core-jvmpf", "name": "job", "reconcileID": "649320ec-7480-4cce-9a8b-0f9b1315d565", "job": "core-jvmpf/job", "gvk": "batch/v1, Kind=Job"}
  2025-04-15T12:52:53.838680061Z	LEVEL(-2)	localqueue-reconciler	core/localqueue_controller.go:165	LocalQueue delete event	{"localQueue": {"name":"lq","namespace":"core-jvmpf"}}
  2025-04-15T12:52:53.839316708Z	LEVEL(-2)	core/workload_controller.go:151	Reconcile Workload	{"controller": "workload_controller", "namespace": "core-jvmpf", "name": "job-job-90988", "reconcileID": "27b41b48-747d-4f01-85d2-328a50c94e97"}
  2025-04-15T12:52:53.848783817Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:680	Workload update event	{"workload": {"name":"job-job-90988","namespace":"core-jvmpf"}, "queue": "lq", "status": "admitted", "clusterQueue": "cq"}
  2025-04-15T12:52:53.849519735Z	LEVEL(-2)	core/workload_controller.go:151	Reconcile Workload	{"controller": "workload_controller", "namespace": "core-jvmpf", "name": "job-job-90988", "reconcileID": "25f6c6b9-06ff-4488-ae7f-5c43fa8e6779"}
  2025-04-15T12:52:53.870263462Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:631	Workload delete event	{"workload": {"name":"job-job-90988","namespace":"core-jvmpf"}, "queue": "lq", "status": "admitted"}
```
And as you can see the entire test finished in less than 1s (since the creation of the namespace), so as if the timeout was not respected at all in this block:

```
			gomega.Eventually(func(g gomega.Gomega) {
				g.Expect(k8sClient.Get(ctx, jobKey, job)).Should(gomega.Succeed())
				job.Status.Active = 1
				job.Status.Ready = ptr.To[int32](1)
				gomega.Expect(k8sClient.Status().Update(ctx, job)).Should(gomega.Succeed())
			}, util.Timeout, util.Interval).Should(gomega.Succeed())
```

I think this is likely because we used `gomega` rather than the local `g` variable when calling the `gomega.Expect`.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-04-16T08:05:12Z

@PBundyra: GitHub didn't allow me to assign the following users: me.

Note that only [kubernetes-sigs members](https://github.com/orgs/kubernetes-sigs/people) with read permissions, repo collaborators and people who have commented on this issue/PR can be assigned. Additionally, issues/PRs can only have 10 assignees at the same time.
For more information please see [the contributor guide](https://git.k8s.io/community/contributors/guide/first-contribution.md#issue-assignment-in-github)

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4984#issuecomment-2808744347):

>/assign me


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-04-16T08:05:46Z

Let me fix that,
/assign pbundyra

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-04-16T08:11:13Z

https://github.com/kubernetes-sigs/kueue/pull/4994
