# Issue #1450: High churn cluster with pod only causing stuck queue and overcommitment

**Summary**: High churn cluster with pod only causing stuck queue and overcommitment

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1450

**Last updated**: 2024-01-11T21:04:08Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@woehrl01](https://github.com/woehrl01)
- **Created**: 2023-12-13T19:06:02Z
- **Updated**: 2024-01-11T21:04:08Z
- **Closed**: 2024-01-11T21:04:08Z
- **Labels**: `kind/bug`
- **Assignees**: [@achernevskii](https://github.com/achernevskii)
- **Comments**: 15

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

Workloads are not deleted even though the pods are deleted, keeping a dangling finalizer and thus the queue gets stuck

**What you expected to happen**:

Work is processed correctly

**How to reproduce it (as minimally and precisely as possible)**:

**Anything else we need to know?**:

The queue shows > 1000 admitted workloads, even though only about 110 are allowed:

![Bildschirmfoto 2023-12-13 um 19 44 45](https://github.com/kubernetes-sigs/kueue/assets/2535856/556d0e56-37f7-43af-951b-575f9668cd04)

The following shows that there are stucked workloads on the ClusterQueue "background" stuck since a few hours.
![Bildschirmfoto 2023-12-13 um 19 59 04](https://github.com/kubernetes-sigs/kueue/assets/2535856/70ead118-0536-407a-b276-ee5f4a4b1dfa)

workloads have a deletion timestamp and finalizer, which is hours old (pod does not exist anymore)
![Bildschirmfoto 2023-12-13 um 20 18 36](https://github.com/kubernetes-sigs/kueue/assets/2535856/8e09fa81-4c23-46b5-b6e5-c9e91e1fd3d7)

looks like that is not finialized, even though the "JobFinished" condition is true on the workflow (example from a different stuck workload): 

![Bildschirmfoto 2023-12-14 um 08 08 31](https://github.com/kubernetes-sigs/kueue/assets/2535856/ecc56e6a-066b-40ae-996f-aaed31ecdb95)




Deleting the finalizer, causes the admitted "workload" resources to get cleaned up. Restarting the controller didn't resolve the error.


**Environment**:
- Kubernetes version (use `kubectl version`): 1.28.3-eks
- Kueue version (use `git describe --tags --dirty --always`): v0.5.1
- Cloud provider or hardware configuration: AWS EKS
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@woehrl01](https://github.com/woehrl01) — 2023-12-14T07:33:31Z

I think one of the issue is here:

https://github.com/kubernetes-sigs/kueue/blob/615dc8e42d160174962f379dd8767e95298a1457/pkg/controller/jobframework/reconciler.go#L254-L265

We have to remove the finalizer as well if the call to `stopJob` returns an error. (line 261)

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-12-14T16:20:31Z

> We have to remove the finalizer as well if the call to stopJob returns an error. (line 261)

I agree. The solution should be to return the error, so that the reconciler as a whole is retried. Right now, there are no retries.

### Comment by [@trasc](https://github.com/trasc) — 2023-12-19T06:10:06Z

> > We have to remove the finalizer as well if the call to stopJob returns an error. (line 261)
> 
> I agree. The solution should be to return the error, so that the reconciler as a whole is retried. Right now, there are no retries.

The error is returned at L264, and the reconcile called again.
 
Sure it could be rewritten as : 
```go
if wl != nil && !wl.DeletionTimestamp.IsZero() { 
 	log.V(2).Info("The workload is marked for deletion") 
 	err := r.stopJob(ctx, job, wl, StopReasonWorkloadDeleted, "Workload is deleted") 
 	if err != nil { 
 		log.Error(err, "Suspending job with deleted workload") 
 		return ctrl.Result{}, err 
 	} 
  
 	if wl != nil { 
 		return ctrl.Result{}, r.removeFinalizer(ctx, wl) 
 	} 
 	return ctrl.Result{}, nil 
 } 
```

But the behavior is the same.

### Comment by [@achernevskii](https://github.com/achernevskii) — 2023-12-22T02:06:49Z

/assign

### Comment by [@achernevskii](https://github.com/achernevskii) — 2023-12-22T19:04:40Z

If wl has a FinishedCondition set, both job and workload should be finalized here:
https://github.com/kubernetes-sigs/kueue/blob/bb69906b810c13c4c49d1386d4c2341f713738e3/pkg/controller/jobframework/reconciler.go#L242-L251

I'm assuming that something else finalized and deleted the pods while they were finished but before the workload was finalized. If that's the case, workload is indeed not finalized.

Exact steps to reproduce and the integration used might be useful.

### Comment by [@woehrl01](https://github.com/woehrl01) — 2023-12-22T19:11:35Z

@achernevskii The integration facing this issue is the pure Pod integration. I use Argo Workflow which spins up the pod with the kueue label. The Argo Workflow is configured to remove the pod as soon the the pod is finished. https://github.com/argoproj/argo-workflows/blob/main/examples%2Fpod-gc-strategy.yaml

### Comment by [@achernevskii](https://github.com/achernevskii) — 2023-12-22T21:27:18Z

To summarize, there are two parts of code which should've finalized the workload in this case:

1. If workload is has a `Finished` condition, it should be finalized right here:
   https://github.com/kubernetes-sigs/kueue/blob/bb69906b810c13c4c49d1386d4c2341f713738e3/pkg/controller/jobframework/reconciler.go#L242-L251
  As I understand, it never happened because the pods were deleted before the reconciler reached that part of the code.

2. If pods are absent from the cluster, this part should drop the workload finalizer:
    https://github.com/kubernetes-sigs/kueue/blob/bb69906b810c13c4c49d1386d4c2341f713738e3/pkg/controller/jobframework/reconciler.go#L161-L184
   But this part could never be reached because of the bug in the `Skip` method, that was skipping reconcile for any not found pod.

Raised a PR with a fix: #1512. @woehrl01, @alculquicondor, please take a look if you'll have the time.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-12-27T14:08:41Z

> The Argo Workflow is configured to remove the pod as soon the the pod is finished.

Does this mean that Argo is removing any finalizers that it didn't set?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-12-27T14:20:59Z

Another question:
What was the metadata of the Workload object once the Pods were deleted? In particular, were the ownerReferences empty?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-01-04T09:11:20Z

/reopen

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-01-04T09:11:25Z

@tenzen-y: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1450#issuecomment-1876749609):

>/reopen


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@kchopra456](https://github.com/kchopra456) — 2024-01-11T14:29:52Z

We have a similar problem for Jobs, where a completed job's correspoding workload when deleted, requeues the workload at times and leads to overcommitment of resources, this happens intermittent.

When kueue-controller-manager restarts, all workloads get submitted to LQ and and it leads to overcommitment beyond the resourceflavor limits.

Attaching kueue-controller-manager logs
```json
{"level":"Level(-2)","ts":"2024-01-11T14:21:03.769950593Z","logger":"workload-reconciler","caller":"core/workload_controller.go:339","msg":"Workload delete event","workload":{"name":"job-trial-job-232c3","namespace":"dev-env"},"queue":"level-0","status":"finished"}
{"level":"Level(-2)","ts":"2024-01-11T14:21:03.77005488Z","logger":"cluster-queue-reconciler","caller":"core/clusterqueue_controller.go:317","msg":"Got generic event","obj":{"name":"job-trial-job-232c3","namespace":"dev-env"},"kind":"/, Kind="}
{"level":"Level(-2)","ts":"2024-01-11T14:21:03.770229932Z","caller":"jobframework/reconciler.go:212","msg":"Reconciling Job","controller":"job","controllerGroup":"batch","controllerKind":"Job","Job":{"name":"trial-job","namespace":"dev-env"},"namespace":"dev-env","name":"trial-job","reconcileID":"1b3c242d-d62e-41c9-bf74-5c405918affd","job":"dev-env/trial-job","gvk":"batch/v1, Kind=Job"}
{"level":"Level(-2)","ts":"2024-01-11T14:21:03.770360388Z","caller":"jobframework/reconciler.go:418","msg":"job with no matching workload, suspending","controller":"job","controllerGroup":"batch","controllerKind":"Job","Job":{"name":"trial-job","namespace":"dev-env"},"namespace":"dev-env","name":"trial-job","reconcileID":"1b3c242d-d62e-41c9-bf74-5c405918affd","job":"dev-env/trial-job","gvk":"batch/v1, Kind=Job"}
{"level":"Level(-2)","ts":"2024-01-11T14:21:03.789380939Z","logger":"workload-reconciler","caller":"core/workload_controller.go:304","msg":"Workload create event","workload":{"name":"job-trial-job-232c3","namespace":"dev-env"},"queue":"level-0","status":"pending"}
{"level":"Level(-2)","ts":"2024-01-11T14:21:03.7894713Z","logger":"cluster-queue-reconciler","caller":"core/clusterqueue_controller.go:317","msg":"Got generic event","obj":{"name":"job-trial-job-232c3","namespace":"dev-env"},"kind":"/, Kind="}
{"level":"Level(-2)","ts":"2024-01-11T14:21:03.789503311Z","caller":"core/workload_controller.go:131","msg":"Reconciling Workload","controller":"workload","controllerGroup":"kueue.x-k8s.io","controllerKind":"Workload","Workload":{"name":"job-trial-job-232c3","namespace":"dev-env"},"namespace":"dev-env","name":"job-trial-job-232c3","reconcileID":"ef38ff35-569f-4af5-9d75-b870139f85f1","workload":{"name":"job-trial-job-232c3","namespace":"dev-env"}}
{"level":"debug","ts":"2024-01-11T14:21:03.789690946Z","logger":"events","caller":"recorder/recorder.go:104","msg":"Created Workload: dev-env/job-trial-job-232c3","type":"Normal","object":{"kind":"Job","namespace":"dev-env","name":"trial-job","uid":"e64d242e-b2f7-46b2-845f-60421be2cc3b","apiVersion":"batch/v1","resourceVersion":"398505458"},"reason":"CreatedWorkload"}
{"level":"Level(-2)","ts":"2024-01-11T14:21:03.789705403Z","logger":"scheduler","caller":"scheduler/scheduler.go:446","msg":"Workload assumed in the cache","workload":{"name":"job-trial-job-232c3","namespace":"dev-env"},"clusterQueue":{"name":"level-0-v2"}}
{"level":"Level(-2)","ts":"2024-01-11T14:21:03.789749677Z","caller":"jobframework/reconciler.go:212","msg":"Reconciling Job","controller":"job","controllerGroup":"batch","controllerKind":"Job","Job":{"name":"trial-job","namespace":"dev-env"},"namespace":"dev-env","name":"trial-job","reconcileID":"4d9e1514-d952-43d0-99f2-73a1ca3c92de","job":"dev-env/trial-job","gvk":"batch/v1, Kind=Job"}
{"level":"Level(-2)","ts":"2024-01-11T14:21:03.797115959Z","logger":"workload-reconciler","caller":"core/workload_controller.go:394","msg":"Workload update event","workload":{"name":"job-trial-job-232c3","namespace":"dev-env"},"queue":"level-0","status":"finished","prevStatus":"pending"}
{"level":"Level(-2)","ts":"2024-01-11T14:21:03.79741215Z","caller":"core/workload_controller.go:131","msg":"Reconciling Workload","controller":"workload","controllerGroup":"kueue.x-k8s.io","controllerKind":"Workload","Workload":{"name":"job-trial-job-232c3","namespace":"dev-env"},"namespace":"dev-env","name":"job-trial-job-232c3","reconcileID":"d8aca21e-d668-4fd8-b215-723059bb8d37","workload":{"name":"job-trial-job-232c3","namespace":"dev-env"}}
{"level":"Level(-2)","ts":"2024-01-11T14:21:03.797403884Z","logger":"cluster-queue-reconciler","caller":"core/clusterqueue_controller.go:317","msg":"Got generic event","obj":{"name":"job-trial-job-232c3","namespace":"dev-env"},"kind":"/, Kind="}
{"level":"Level(-2)","ts":"2024-01-11T14:21:03.797461463Z","caller":"jobframework/reconciler.go:212","msg":"Reconciling Job","controller":"job","controllerGroup":"batch","controllerKind":"Job","Job":{"name":"trial-job","namespace":"dev-env"},"namespace":"dev-env","name":"trial-job","reconcileID":"1c63f021-b2db-45a6-8fab-7c748ecf7587","job":"dev-env/trial-job","gvk":"batch/v1, Kind=Job"}
{"level":"Level(-2)","ts":"2024-01-11T14:21:03.806182991Z","logger":"scheduler","caller":"scheduler/scheduler.go:454","msg":"Workload successfully admitted and assigned flavors","workload":{"name":"job-trial-job-232c3","namespace":"dev-env"},"clusterQueue":{"name":"level-0-v2"},"assignments":[{"name":"main","flavors":{"cpu":"node-set-2","nvidia.com/gpu":"node-set-2"},"resourceUsage":{"cpu":"2","nvidia.com/gpu":"1"},"count":1}]}
{"level":"debug","ts":"2024-01-11T14:21:03.806234609Z","logger":"events","caller":"recorder/recorder.go:104","msg":"Admitted by ClusterQueue level-0-v2, wait time was 1s","type":"Normal","object":{"kind":"Workload","namespace":"dev-env","name":"job-trial-job-232c3","uid":"8c047d52-d6ad-4da1-9d0a-640775a6d381","apiVersion":"kueue.x-k8s.io/v1beta1","resourceVersion":"399376517"},"reason":"Admitted"}
{"level":"Level(-2)","ts":"2024-01-11T14:21:03.806594229Z","logger":"workload-reconciler","caller":"core/workload_controller.go:394","msg":"Workload update event","workload":{"name":"job-trial-job-232c3","namespace":"dev-env"},"queue":"level-0","status":"finished","clusterQueue":"level-0-v2"}
{"level":"Level(-2)","ts":"2024-01-11T14:21:03.806720268Z","logger":"cluster-queue-reconciler","caller":"core/clusterqueue_controller.go:317","msg":"Got generic event","obj":{"name":"job-trial-job-232c3","namespace":"dev-env"},"kind":"/, Kind="}
{"level":"Level(-2)","ts":"2024-01-11T14:21:03.806759252Z","caller":"core/workload_controller.go:131","msg":"Reconciling Workload","controller":"workload","controllerGroup":"kueue.x-k8s.io","controllerKind":"Workload","Workload":{"name":"job-trial-job-232c3","namespace":"dev-env"},"namespace":"dev-env","name":"job-trial-job-232c3","reconcileID":"0a85a2ea-73ef-45cb-8f68-ae88d627a7d4","workload":{"name":"job-trial-job-232c3","namespace":"dev-env"}}
{"level":"error","ts":"2024-01-11T14:21:03.810342314Z","caller":"controller/controller.go:329","msg":"Reconciler error","controller":"job","controllerGroup":"batch","controllerKind":"Job","Job":{"name":"trial-job","namespace":"dev-env"},"namespace":"dev-env","name":"trial-job","reconcileID":"1c63f021-b2db-45a6-8fab-7c748ecf7587","error":"Operation cannot be fulfilled on workloads.kueue.x-k8s.io \"job-trial-job-232c3\": the object has been modified; please apply your changes to the latest version and try again","stacktrace":"sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).reconcileHandler\n\t/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.16.2/pkg/internal/controller/controller.go:329\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).processNextWorkItem\n\t/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.16.2/pkg/internal/controller/controller.go:266\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).Start.func2.2\n\t/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.16.2/pkg/internal/controller/controller.go:227"}
{"level":"Level(-2)","ts":"2024-01-11T14:21:03.810425591Z","caller":"jobframework/reconciler.go:212","msg":"Reconciling Job","controller":"job","controllerGroup":"batch","controllerKind":"Job","Job":{"name":"trial-job","namespace":"dev-env"},"namespace":"dev-env","name":"trial-job","reconcileID":"c8ca77b7-4973-4fde-8ecf-1677a998f381","job":"dev-env/trial-job","gvk":"batch/v1, Kind=Job"}
{"level":"Level(-2)","ts":"2024-01-11T14:21:03.822113223Z","caller":"jobframework/reconciler.go:212","msg":"Reconciling Job","controller":"job","controllerGroup":"batch","controllerKind":"Job","Job":{"name":"trial-job","namespace":"dev-env"},"namespace":"dev-env","name":"trial-job","reconcileID":"88f3bccb-20b8-4fee-ad3a-2c64644c4145","job":"dev-env/trial-job","gvk":"batch/v1, Kind=Job"}
{"level":"Level(-2)","ts":"2024-01-11T14:21:03.822813488Z","logger":"workload-reconciler","caller":"core/workload_controller.go:394","msg":"Workload update event","workload":{"name":"job-trial-job-232c3","namespace":"dev-env"},"queue":"level-0","status":"finished","clusterQueue":"level-0-v2"}
{"level":"Level(-2)","ts":"2024-01-11T14:21:03.822906935Z","logger":"cluster-queue-reconciler","caller":"core/clusterqueue_controller.go:317","msg":"Got generic event","obj":{"name":"job-trial-job-232c3","namespace":"dev-env"},"kind":"/, Kind="}
{"level":"Level(-2)","ts":"2024-01-11T14:21:03.822992527Z","caller":"core/workload_controller.go:131","msg":"Reconciling Workload","controller":"workload","controllerGroup":"kueue.x-k8s.io","controllerKind":"Workload","Workload":{"name":"job-trial-job-232c3","namespace":"dev-env"},"namespace":"dev-env","name":"job-trial-job-232c3","reconcileID":"e9327b36-44a7-4622-abe6-b76aba31226c","workload":{"name":"job-trial-job-232c3","namespace":"dev-env"}}
{"level":"error","ts":"2024-01-11T14:21:03.82881663Z","caller":"controller/controller.go:329","msg":"Reconciler error","controller":"job","controllerGroup":"batch","controllerKind":"Job","Job":{"name":"trial-job","namespace":"dev-env"},"namespace":"dev-env","name":"trial-job","reconcileID":"88f3bccb-20b8-4fee-ad3a-2c64644c4145","error":"Operation cannot be fulfilled on workloads.kueue.x-k8s.io \"job-trial-job-232c3\": the object has been modified; please apply your changes to the latest version and try again","stacktrace":"sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).reconcileHandler\n\t/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.16.2/pkg/internal/controller/controller.go:329\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).processNextWorkItem\n\t/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.16.2/pkg/internal/controller/controller.go:266\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).Start.func2.2\n\t/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.16.2/pkg/internal/controller/controller.go:227"}
{"level":"Level(-2)","ts":"2024-01-11T14:21:03.828929655Z","caller":"jobframework/reconciler.go:212","msg":"Reconciling Job","controller":"job","controllerGroup":"batch","controllerKind":"Job","Job":{"name":"trial-job","namespace":"dev-env"},"namespace":"dev-env","name":"trial-job","reconcileID":"5f309284-1a14-436f-a18d-740796afdc92","job":"dev-env/trial-job","gvk":"batch/v1, Kind=Job"}
{"level":"Level(-2)","ts":"2024-01-11T14:21:03.834097205Z","caller":"jobframework/reconciler.go:212","msg":"Reconciling Job","controller":"job","controllerGroup":"batch","controllerKind":"Job","Job":{"name":"trial-job","namespace":"dev-env"},"namespace":"dev-env","name":"trial-job","reconcileID":"91c22bf2-5fc5-4c68-9c02-b52bec91c175","job":"dev-env/trial-job","gvk":"batch/v1, Kind=Job"}
```

Steps to reproduce
1. Create a job, let the job complete.
2. Delete the workload a few times, I deleted 2 times
3. Rollout restart for the controller
4. Check localqueue, it will admit finished workload
Note: to reset the behavior, delete the affected workload and that clears out localqueue admitted state, but it would reappear once the controller is restarted.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-01-11T15:49:07Z

Can you confirm the kueue version?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-01-11T16:11:14Z

It looks like this won't be a problem in 0.6 https://github.com/kubernetes-sigs/kueue/pull/1383

Although it is possible that it was a bug in 0.5. I'll continue investigating.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-01-11T17:07:52Z

I created a cherry-pick #1572
