# Issue #9020: New  pull-kueue-test-tas-scheduling-perf-release-0-15 is failing

**Summary**: New  pull-kueue-test-tas-scheduling-perf-release-0-15 is failing

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9020

**Last updated**: 2026-02-09T11:07:33Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-02-06T08:05:53Z
- **Updated**: 2026-02-09T11:07:33Z
- **Closed**: 2026-02-09T11:07:32Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 8

## Description

**Which test is flaking?**:


pull-kueue-test-tas-scheduling-perf-release-0-15


**Link to failed CI job or steps to reproduce locally**:

https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/9014/pull-kueue-test-tas-scheduling-perf-release-0-15/2019497720158359552

**Failure message or logs**:
```
2026-02-05T20:08:40.630594077Z	ERROR	controller/controller.go:474	Reconciler error	{"controller": "workload", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Workload", "Workload": {"name":"medium-balanced-rack-5-5-0","namespace":"cq-0-1-cohort-1"}, "namespace": "cq-0-1-cohort-1", "name": "medium-balanced-rack-5-5-0", "reconcileID": "99630867-2cdf-47ef-8e9a-2abf02567266", "error": "Workload.kueue.x-k8s.io \"medium-balanced-rack-5-5-0\" is invalid: status.admission.podSetAssignments[0].topologyAssignment: Invalid value: \"object\": no such key: slices evaluating rule: valuesPerLevel must have the same length as the number of levels in this TopologyAssignment"}
sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).reconcileHandler
	/home/prow/go/src/sigs.k8s.io/kueue/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:474
sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).processNextWorkItem
	/home/prow/go/src/sigs.k8s.io/kueue/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:421
sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).Start.func1.1
	/home/prow/go/src/sigs.k8s.io/kueue/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:296
2026-02-05T20:08:40.730825024Z	ERROR	controller/controller.go:474	Reconciler error	{"controller": "workload", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Workload", "Workload": {"name":"medium-balanced-rack-5-5-0","namespace":"cq-0-2-cohort-0"}, "namespace": "cq-0-2-cohort-0", "name": "medium-balanced-rack-5-5-0", "reconcileID": "b4f88f95-18fb-4958-8ec9-a1ab75b72a5e", "error": "Workload.kueue.x-k8s.io \"medium-balanced-rack-5-5-0\" is invalid: status.admission.podSetAssignments[0].topologyAssignment: Invalid value: \"object\": no such key: slices evaluating rule: valuesPerLevel must have the same length as the number of levels in this TopologyAssignment"}
sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).reconcileHandler
	/home/prow/go/src/sigs.k8s.io/kueue/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:474
sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).processNextWorkItem
	/home/prow/go/src/sigs.k8s.io/kueue/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:421
sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).Start.func1.1
	/home/prow/go/src/sigs.k8s.io/kueue/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:296
2026-02-05T20:08:40.830090332Z	ERROR	controller/controller.go:474	Reconciler error	{"controller": "workload", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Workload", "Workload": {"name":"small-required-rack-0-12-0","namespace":"cq-0-0-cohort-0"}, "namespace": "cq-0-0-cohort-0", "name": "small-required-rack-0-12-0", "reconcileID": "c6e93abe-a2c7-4696-9cec-06a6263bffb3", "error": "Workload.kueue.x-k8s.io \"small-required-rack-0-12-0\" is invalid: status.admission.podSetAssignments[0].topologyAssignment: Invalid value: \"object\": no such key: slices evaluating rule: valuesPerLevel must have the same length as the number of levels in this TopologyAssignment"}
sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).reconcileHandler
	/home/prow/go/src/sigs.k8s.io/kueue/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:474
sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).processNextWorkItem
	/home/prow/go/src/sigs.k8s.io/kueue/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:421
sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).Start.func1.1
	/home/prow/go/src/sigs.k8s.io/kueue/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:296
2026-02-05T20:08:40.833138092Z	ERROR	Start recorder	runner/main.go:392	Recorder run	{"error": "context deadline exceeded"}
main.startRecorder.func1
	/home/prow/go/src/sigs.k8s.io/kueue/test/performance/scheduler/runner/main.go:392
sync.(*WaitGroup).Go.func1
	/usr/local/go/src/sync/waitgroup.go:239
2026-02-05T20:08:40.833213283Z	ERROR	runner/main.go:228	Error	{"error": "context deadline exceeded"}
main.main
	/home/prow/go/src/sigs.k8s.io/kueue/test/performance/scheduler/runner/main.go:228
runtime.main
	/usr/local/go/src/runtime/proc.go:285
2026-02-05T20:08:40.833327374Z	INFO	Run command	runner/main.go:270	Stop the command
```

**Anything else we need to know?**:

Follow up to https://github.com/kubernetes-sigs/kueue/issues/9007

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-06T08:11:38Z

cc @ikchifo @ASverdlov @mbobrovskyi @sohankunkerkar 


Look at that `"namespace": "cq-0-0-cohort-0", "name": "small-required-rack-0-12-0", "reconcileID": "c6e93abe-a2c7-4696-9cec-06a6263bffb3", "error": "Workload.kueue.x-k8s.io \"small-required-rack-0-12-0\" is invalid: status.admission.podSetAssignments[0].topologyAssignment: Invalid value: \"object\": no such key: slices evaluating rule: valuesPerLevel must have the same length as the number of levels in this TopologyAssignment"}`

Aha! I think this is because there is no `valuesPerLevel` in v1beta1, and from 0.16 we introduced a different structure for TopologyAssignment.

So I think we need to disable the perf tests on 0.15 or send a PR to adjust the testing to use v1beta1 structures. I think it is ok to just disable the tests in `test-infra` unless someone is willing to take the work.

Btw: `2026-02-05T20:08:40.833138092Z	ERROR	Start recorder	runner/main.go:392	Recorder run	{"error": "context deadline exceeded"} main.startRecorder.func1` could probably be silenced as we did in the scraper.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-06T09:13:46Z

Yeah, I think the cherrypicked test code assumes Workload v1beta2 is available, but the performance runner does not install conversion webhooks. So, the server Workload is in v1beta1. 

It is not a regression. Let me open a PR to disable the testing for 0.15.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-06T09:17:41Z

Opened: https://github.com/kubernetes/test-infra/pull/36394

### Comment by [@ASverdlov](https://github.com/ASverdlov) — 2026-02-06T12:22:26Z

Shoot, sorry, let me fix that!

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-06T12:52:07Z

FYI: if you want then sure, but from my perspective fixing 0.15 wrt to the test is just nice to have. This is a historical branch which will go out of support in 2 months. However if this is useful for you, then feel free

### Comment by [@ASverdlov](https://github.com/ASverdlov) — 2026-02-06T13:04:39Z

Yeah, I checked it briefly, and it looks like it's a lot of work for something that won't be supported in 2 months anymore. I will focus on something more productive.

/unassign

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-09T11:07:26Z

/close
Thank you 👍

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-02-09T11:07:33Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/9020#issuecomment-3871068315):

>/close
>Thank you 👍 


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
