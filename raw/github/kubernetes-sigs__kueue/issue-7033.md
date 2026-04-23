# Issue #7033: [flaky test] MultiKueue Should run an ElasticJob on worker if admitted

**Summary**: [flaky test] MultiKueue Should run an ElasticJob on worker if admitted

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7033

**Last updated**: 2025-09-30T09:02:20Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-09-29T07:07:53Z
- **Updated**: 2025-09-30T09:02:20Z
- **Closed**: 2025-09-30T09:02:20Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 13

## Description

/kind flake 
**What happened**:

test flaked on unrelated branch: https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/7030/pull-kueue-test-integration-multikueue-main/1972555011267235840

**What you expected to happen**:
no failures
**How to reproduce it (as minimally and precisely as possible)**:
ci
**Anything else we need to know?**:
```
  2025-09-29T06:58:31.569654255Z	LEVEL(-3)	controller-runtime.cache	cache/reflector.go:364	Stopping reflector	{"type": "*v1beta2.AppWrapper", "resyncPeriod": "9h14m23.302262527s", "reflector": "sigs.k8s.io/controller-runtime/pkg/cache/internal/informers.go:114"}
  2025-09-29T06:58:31.569900499Z	INFO	manager/internal.go:554	Stopping and waiting for webhooks
  2025-09-29T06:58:31.570019701Z	INFO	controller-runtime.webhook	webhook/server.go:249	Shutting down webhook server with timeout of 1 minute
  2025-09-29T06:58:32.632451602Z	INFO	manager/internal.go:557	Stopping and waiting for HTTP servers
  2025-09-29T06:58:32.632688255Z	INFO	manager/internal.go:561	Wait completed, proceeding to shutdown the manager
  "level"=0 "msg"="manager stopped"
  << Timeline
  [FAILED] Expected success, but got an error:
      <*errors.StatusError | 0xc00bb7a780>: 
      jobs.batch "job" not found
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
              Message: "jobs.batch \"job\" not found",
              Reason: "NotFound",
              Details: {Name: "job", Group: "batch", Kind: "jobs", UID: "", Causes: nil, RetryAfterSeconds: 0},
              Code: 404,
          },
      }
  In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/integration/multikueue/jobs_test.go:1794 @ 09/29/25 06:58:30.336
------------------------------
[AfterSuite] PASSED [3.692 seconds]
[AfterSuite] 
/home/prow/go/src/sigs.k8s.io/kueue/test/integration/multikueue/suite_test.go:358
  Timeline >>
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-29T07:08:01Z

cc @ichekrygin ptal

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-29T11:05:37Z

cc @mszadkow @mbobrovskyi ptal too

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-29T12:06:59Z

https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/7048/pull-kueue-test-integration-multikueue-main/1972632311891496960

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-09-29T12:19:18Z

cc @ichekrygin

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-09-29T12:20:23Z

What I found interesting is that during the test the Job was stopped:
```
  2025-09-29T06:58:29.516585997Z ERROR jobframework/reconciler.go:471 Handling job with no workload {"controller": "job", "controllerGroup": "batch", "controllerKind": "Job", "Job": {"name":"job","namespace":"multikueue-fqkg4"}, "namespace": "multikueue-fqkg4", "name": "job", "reconcileID": "5bab5e59-182d-4333-bd12-7f252a2311fc", "job": "multikueue-fqkg4/job", "gvk": "batch/v1, Kind=Job", "error": "prebuilt workload not found"}
  sigs.k8s.io/kueue/pkg/controller/jobframework.(*JobReconciler).ReconcileGenericJob
   /home/prow/go/src/sigs.k8s.io/kueue/pkg/controller/jobframework/reconciler.go:471
  sigs.k8s.io/kueue/pkg/controller/jobframework.(*genericReconciler).Reconcile
   /home/prow/go/src/sigs.k8s.io/kueue/pkg/controller/jobframework/reconciler.go:1475
  sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).Reconcile
   /home/prow/go/src/sigs.k8s.io/kueue/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:119
  sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).reconcileHandler
   /home/prow/go/src/sigs.k8s.io/kueue/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:340
  sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).processNextWorkItem
   /home/prow/go/src/sigs.k8s.io/kueue/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:300
  sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).Start.func2.1
   /home/prow/go/src/sigs.k8s.io/kueue/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:202
  2025-09-29T06:58:29.516657229Z DEBUG events recorder/recorder.go:104 missing workload {"type": "Normal", "object": {"kind":"Job","namespace":"multikueue-fqkg4","name":"job","uid":"1f2ab246-b85c-406a-9e6d-a40424b07079","apiVersion":"batch/v1","resourceVersion":"618"}, "reason": "Stopped"}
```

I am not sure this should happen with ElasticJob

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-09-29T12:23:22Z

I was able to reproduce the flakiness locally quite easily, couple of repeats and it happens.
It matches above observation bc, this is not "job not found" rather one line further:
```
  [FAILED] Expected
      <*bool | 0xc006ef8c8f>: true
  to be equivalent to
      <*bool | 0xc006ef8caf>: false
  In [It] at: /Users/michal_szadkowski/workspace/kueue/test/integration/multikueue/jobs_test.go:1795 @ 09/29/25 13:54:28.524
------------------------------

Summarizing 1 Failure:
  [FAIL] MultiKueue [It] Should run an ElasticJob on worker if admitted
  /Users/michal_szadkowski/workspace/kueue/test/integration/multikueue/jobs_test.go:1795
```

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-29T12:31:28Z

Ok, it would be good to understand if this:
1. represents just a test flake
2. represents a prod code issue which can be fixed within the current design
3. represents a prod code issue which requires a design change

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-09-29T15:02:43Z

I am having hard time to reproduce this issue.

> I was able to reproduce the flakiness locally quite easily, couple of repeats and it happens.

I ran multiple times (in IDE) back-to-back (individual test-case "It", as well as, parent "Describe") - so far no repro.

Is there a specific test command that triggers this?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-29T15:20:16Z

I repro locally just by wrapping with the for loop:

```golang
	for i := range 20 {
		ginkgo.FIt(fmt.Sprintf("Should run an ElasticJob on worker if admitted %d", i), func() {
```
Then running from console with 
```sh
INTEGRATION_TARGET=./test/integration/multikueue make test-integration | tee out.txt
```
plus I disable the ContinueOnFailure

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-29T15:22:55Z

I have a hypothesis that in this part:

https://github.com/kubernetes-sigs/kueue/blob/c0ec343567d534021660b2ac7a4dfac255ded7f6/test/integration/multikueue/jobs_test.go#L1758-L1771

the call `g.Expect(workloadslicing.Finish(manager.ctx, manager.client, oldWorkload, kueue.WorkloadSliceReplaced, "Replaced to accommodate a new slice")).To(gomega.Succeed()) `

may cascade to the worker1 cluster, before the replacement workload on the worker1 cluster is admitted.

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-09-29T15:27:34Z

For me it works like this:
export `KUBEBUILDER_ASSETS`
go to `test/integration/multikueue`
run: `ginkgo --race -r --procs=4 --focus "Should run an ElasticJob on worker if admitted" --repeat=10`

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-09-29T15:34:20Z

> I have a hypothesis that in this part:

I think you could be right:

```
ginkgo.By("admit the new workload and finish the old workload in the manager cluster", func() {
	util.SetQuotaReservation(manager.ctx, manager.client, newWorkloadKey, utiltesting.MakeAdmission(managerCq.Name).Obj())
	gomega.Eventually(func(g gomega.Gomega) {
		oldWorkload := getWorkload(g, manager.ctx, manager.client, workloadKey)
		g.Expect(workloadslicing.Finish(manager.ctx, manager.client, oldWorkload, kueue.WorkloadSliceReplaced, "Replaced to accommodate a new slice")).To(gomega.Succeed())
	}, util.Timeout, util.Interval).Should(gomega.Succeed())
})
```

I think I got those 2 steps out of order. In "production" code scheduler:
* First, marks the old workload [slice] as "Finished" (replaced)
* Then, admits the new workload [slice]

Since we are not using (enabled) scheduler in this test case - those steps are "emulated".
Still digging into this.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-29T15:34:21Z

If the fix is involving I would like to consider temporarily disabling the test so that it does not interfere with the release process tomorrow, and re-enable along with the fix.

EDIT: to disable temporarily we could either use `ginkgo.XIt` of `ginkgo.Skip`
