# Issue #1215: When a job resets reclaimable pods when evicted, it gets stuck due to Workload validation

**Summary**: When a job resets reclaimable pods when evicted, it gets stuck due to Workload validation

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1215

**Last updated**: 2023-10-28T07:59:38Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@GhangZh](https://github.com/GhangZh)
- **Created**: 2023-10-17T08:14:48Z
- **Updated**: 2023-10-28T07:59:38Z
- **Closed**: 2023-10-28T07:59:38Z
- **Labels**: `kind/feature`
- **Assignees**: [@yaroslava-serdiuk](https://github.com/yaroslava-serdiuk)
- **Comments**: 18

## Description

If the workload is preempted, will ReclaimablePod be set to nil?
![image](https://github.com/kubernetes-sigs/kueue/assets/92301646/56036425-2fc6-410d-844e-02b864c4c218)
```bash
{"level":"error","ts":"2023-10-16T12:47:55.770288657Z","caller":"controller/controller.go:324","msg":"Reconciler error","controller":"job","controllerGroup":"batch.volcano.sh","controllerKind":"Job","Job":{"name":"hobot-job-xxx","namespace":"cpu-preempt"},"namespace":"cpu-preempt","name":"hobot-job-xxx","reconcileID":"f4abf36a-f5f2-4ec0-bbae-31b49cfef394","error":"admission webhook \"[vworkload.kb.io](http://vworkload.kb.io/)\" denied the request: status.reclaimablePods[main]: Required value: cannot be removed","stacktrace":"[sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).reconcileHandler\n\t/gopath/pkg/mod/sigs.k8s.io/controller-runtime@v0.15.0/pkg/internal/controller/controller.go:324\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).processNextWorkItem\n\t/gopath/pkg/mod/sigs.k8s.io/controller-runtime@v0.15.0/pkg/internal/controller/controller.go:265\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).Start.func2.2\n\t/gopath/pkg/mod/sigs.k8s.io/controller-runtime@v0.15.0/pkg/internal/controller/controller.go:226](http://sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).reconcileHandler/n/t/gopath/pkg/mod/sigs.k8s.io/controller-runtime@v0.15.0/pkg/internal/controller/controller.go:324/nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).processNextWorkItem/n/t/gopath/pkg/mod/sigs.k8s.io/controller-runtime@v0.15.0/pkg/internal/controller/controller.go:265/nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).Start.func2.2/n/t/gopath/pkg/mod/sigs.k8s.io/controller-runtime@v0.15.0/pkg/internal/controller/controller.go:226)"}
```
Is this our normal logic, or am I using it incorrectly, which would cause the webhook checksum to fail for the departure workload.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-10-17T13:13:36Z

cc @trasc 

Yes, the reclaimable pods should stay, because those reclaimable pods shouldn't be recreated when the job is resumed.

Can you elaborate about the webhook failure?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-10-17T13:27:25Z

I opened a couple of follow ups based on your question

### Comment by [@GhangZh](https://github.com/GhangZh) — 2023-10-17T13:29:50Z

> cc @trasc
> 
> Yes, the reclaimable pods should stay, because those reclaimable pods shouldn't be recreated when the job is resumed.
> 
> Can you elaborate about the webhook failure?

1. Queue A resources to meet the minCount, task jobA normal operation, such as some of the pod has been completed, ReclaimPod will record the number of completed, but there are still part of the pod in the running
2. At this time, queue A is preempted by the task of queue B will happen this webhook failure

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-10-17T13:33:43Z

I see
/kind bug

### Comment by [@GhangZh](https://github.com/GhangZh) — 2023-10-17T13:33:49Z

> I opened a couple of follow ups based on your question

That's great. I really need this.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-10-17T13:34:23Z

/remove-kind support

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-10-17T13:35:28Z

/retitle When a job with reclaimable pods is evicted, a webhook failure prevents it from preemption.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-10-17T14:06:16Z

/assign @mimowo

### Comment by [@trasc](https://github.com/trasc) — 2023-10-18T05:25:08Z

skipping https://github.com/kubernetes-sigs/kueue/blob/525098b838eb28ee241cf1aaee5e53f161d30a0c/pkg/controller/jobframework/reconciler.go#L268-L278

while the workload has the evicted condition set, should do the trick.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-10-18T14:20:05Z

why? Are you suggesting that, during suspend, the calculation for number of reclaimable pods is somehow decreasing?

### Comment by [@yaroslava-serdiuk](https://github.com/yaroslava-serdiuk) — 2023-10-19T13:31:06Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2023-10-19T13:35:00Z

/unassign

### Comment by [@trasc](https://github.com/trasc) — 2023-10-20T08:00:43Z

> why? Are you suggesting that, during suspend, the calculation for number of reclaimable pods is somehow decreasing?

Yes it could be,  it's not the case for `batch/job` but for other kind of jobs, as long as workload is not attempting to increase it's usage while holding a quota-reservation it should be fine.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-10-20T14:01:10Z

@GhangZh in which job API were you observing this?

### Comment by [@GhangZh](https://github.com/GhangZh) — 2023-10-20T14:18:22Z

> @GhangZh in which job API were you observing this?

volcano job
Is kueue designed to complete a portion of the pod and then be suspended, and then when it is re-run it will only start the remaining pods?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-10-20T15:14:46Z

I see.
Yes, that's correct.
If vcjob can't support this, you can choose not to implement `ReclaimablePods` and it will be assumed zero.

Otherwise, have a look at Job's implementation https://github.com/kubernetes-sigs/kueue/blob/6c812be6d9bbe2214cae5cfcaa33953f7a14fdba/pkg/controller/jobs/job/job_controller.go#L190

We rely on the succeeded count

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-10-20T15:17:47Z

I guess we could do something along the lines of https://github.com/kubernetes-sigs/kueue/issues/1215#issuecomment-1767665772

Or change the webhook to allow reclaimable pods to go to zero when the job is suspended. This way, we don't make assumptions about whether the job needs to restart from scratch or not.

/remove-kind bug
/kind feature

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-10-20T15:19:07Z

/retitle When a job resets reclaimable pods when evicted, it gets stuck due to Workload validation
