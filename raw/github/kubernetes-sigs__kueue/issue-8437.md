# Issue #8437: [Flaky Perf Test] Client rate limiter Wait returned an error: context canceled"

**Summary**: [Flaky Perf Test] Client rate limiter Wait returned an error: context canceled"

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8437

**Last updated**: 2026-02-12T11:58:04Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2026-01-05T11:45:00Z
- **Updated**: 2026-02-12T11:58:04Z
- **Closed**: 2026-02-12T11:58:04Z
- **Labels**: `kind/bug`, `priority/important-soon`, `kind/flake`
- **Assignees**: [@sohankunkerkar](https://github.com/sohankunkerkar)
- **Comments**: 11

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->

/kind flake


**What happened**:

```
2026-01-05T09:16:43.908919858Z	INFO	Run generator	runner/main.go:355	Generator done	{"duration": "1m6.177059136s"}
push_pin
2026-01-05T09:25:37.732719758Z	ERROR	Start recorder	runner/main.go:368	Recorder run	{"error": "context deadline exceeded"}
main.startRecorder.func1
	/home/prow/go/src/sigs.k8s.io/kueue/test/performance/scheduler/runner/main.go:368
sync.(*WaitGroup).Go.func1
	/usr/local/go/src/sync/waitgroup.go:239
2026-01-05T09:25:37.73283916Z	ERROR	runner/main.go:210	Error	{"error": "context deadline exceeded"}
main.main
	/home/prow/go/src/sigs.k8s.io/kueue/test/performance/scheduler/runner/main.go:210
runtime.main
	/usr/local/go/src/runtime/proc.go:285
```

```
2026-01-05T09:37:52.408133361Z	INFO	manager/internal.go:578	Wait completed, proceeding to shutdown the manager
2026-01-05T09:38:03.147201793Z	ERROR	controller/controller.go:474	Reconciler error	{"controller": "workload", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Workload", "Workload": {"name":"small-0-18-0","namespace":"cq-0-3-cohort-0"}, "namespace": "cq-0-3-cohort-0", "name": "small-0-18-0", "reconcileID": "ba829d26-4b2e-4c3d-9697-a4be8f8b7453", "error": "client rate limiter Wait returned an error: context canceled"}
sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).reconcileHandler
	/home/prow/go/src/sigs.k8s.io/kueue/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:474
sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).processNextWorkItem
	/home/prow/go/src/sigs.k8s.io/kueue/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:421
sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).Start.func1.1
	/home/prow/go/src/sigs.k8s.io/kueue/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:296
```

**What you expected to happen**:

No issue

**How to reproduce it (as minimally and precisely as possible)**:

https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/8436/pull-kueue-test-scheduling-perf-main/2008104395681566720

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

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-01-05T14:39:57Z

/assign

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-01-05T15:20:05Z

The flake happens because the test shuts down while the controller is still busy processing workloads. During the performance test, the controller handles a high volume of workloads which creates a backlog of pending API requests. When the test ends and triggers shutdown, some reconcilers are still waiting to make API calls. These waiting operations receive a "context canceled" signal, and this gets logged as an error. 

I'm guessing this happens in perf tests because of the combination of high load and immediate shutdown. I think the test runner should recognize that "context canceled" errors occurring after shutdown begins are expected and shouldn't be treated as failures.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-01-07T07:03:39Z

Actually, we have context deadline exceeded:

```
2026-01-05T09:25:37.732719758Z	ERROR	Start recorder	runner/main.go:368	Recorder run	{"error": "context deadline exceeded"}
```

https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/8436/pull-kueue-test-scheduling-perf-main/2008104395681566720#1:build-log.txt%3A365

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-01-07T08:07:50Z

OK. From the logs, I can see that the first test attempt failed due to DeadlineExceeded. This is expected – sometimes the test-infra doesn’t have enough capacity due to overloading.

What I don’t understand, however, is why we’re seeing this error on the second test attempt.

```
2026-01-05T09:30:31.087499588Z	INFO	controller-runtime.cache	cache/reflector.go:568	Warning: watch ended with error	{"reflector": "sigs.k8s.io/controller-runtime/pkg/cache/internal/informers.go:114", "type": "*v1beta2.ClusterQueue", "err": "an error on the server (\"unable to decode an event from the watch stream: http2: client connection lost\") has prevented the request from succeeding"}
2026-01-05T09:30:31.048382782Z	INFO	controller-runtime.cache	cache/reflector.go:568	Warning: watch ended with error	{"reflector": "sigs.k8s.io/controller-runtime/pkg/cache/internal/informers.go:114", "type": "*v1beta2.Workload", "err": "an error on the server (\"unable to decode an event from the watch stream: http2: client connection lost\") has prevented the request from succeeding"}
2026-01-05T09:30:31.883005807Z	ERROR	controller/controller.go:474	Reconciler error	{"controller": "workload", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Workload", "Workload": {"name":"small-0-20-0","namespace":"cq-0-5-cohort-1"}, "namespace": "cq-0-5-cohort-1", "name": "small-0-20-0", "reconcileID": "ff5261ed-344f-4f08-a21e-14c8e424a889", "error": "Patch \"https://127.0.0.1:41781/apis/kueue.x-k8s.io/v1beta2/namespaces/cq-0-5-cohort-1/workloads/small-0-20-0/status?fieldManager=kueue-job-controller-Finished&force=true\": http2: client connection lost"}
sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).reconcileHandler
	/home/prow/go/src/sigs.k8s.io/kueue/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:474
sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).processNextWorkItem
	/home/prow/go/src/sigs.k8s.io/kueue/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:421
sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).Start.func1.1
	/home/prow/go/src/sigs.k8s.io/kueue/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:296
2026-01-05T09:30:31.916069211Z	ERROR	controller/controller.go:474	Reconciler error	{"controller": "workload", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Workload", "Workload": {"name":"small-0-20-0","namespace":"cq-0-0-cohort-2"}, "namespace": "cq-0-0-cohort-2", "name": "small-0-20-0", "reconcileID": "289b6574-007d-4a31-9a58-4bea905fb747", "error": "Patch \"https://127.0.0.1:41781/apis/kueue.x-k8s.io/v1beta2/namespaces/cq-0-0-cohort-2/workloads/small-0-20-0/status?fieldManager=kueue-job-controller-Finished&force=true\": http2: client connection lost"}
sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).reconcileHandler
	/home/prow/go/src/sigs.k8s.io/kueue/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:474
sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).processNextWorkItem
	/home/prow/go/src/sigs.k8s.io/kueue/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:421
sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).Start.func1.1
	/home/prow/go/src/sigs.k8s.io/kueue/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:296
2026-01-05T09:30:31.883004857Z	ERROR	controller/controller.go:474	Reconciler error	{"controller": "workload", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Workload", "Workload": {"name":"small-0-19-0","namespace":"cq-0-5-cohort-0"}, "namespace": "cq-0-5-cohort-0", "name": "small-0-19-0", "reconcileID": "077bda7a-62fa-4625-b61f-b597ceb716ad", "error": "Patch \"https://127.0.0.1:41781/apis/kueue.x-k8s.io/v1beta2/namespaces/cq-0-5-cohort-0/workloads/small-0-19-0/status?fieldManager=kueue-job-controller-Finished&force=true\": http2: client connection lost"}
```

But this is probably just a network issue, so we can close this issue.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-07T08:15:34Z

> But this is probably just a network issue, so we can close this issue.

It does not seem to involve external traffic. "client connection lost" shouldn't really happen for internal cluster traffic. All cases of connection lost for internal traffic I've seen so far were if Kueue was down for some reason.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-07T10:27:14Z

/priority important-soon

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-14T06:25:01Z

/reopen

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-01-14T06:25:06Z

@tenzen-y: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/8437#issuecomment-3747990410):

>/reopen
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-14T06:26:02Z

We observed this again
https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-scheduling-perf-main/2011287564287217664

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-14T07:39:36Z

What is characteristic for these failures is that the re-try was invoked, see https://gcsweb.k8s.io/gcs/kubernetes-ci-logs/logs/periodic-kueue-test-scheduling-perf-main/2011287564287217664/artifacts/

See the PR: https://github.com/kubernetes-sigs/kueue/pull/3020

This retry mechanism was added intentionally to handle flakes, but maybe for some reason the mechanism stopped working.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-19T07:30:45Z

https://storage.googleapis.com/kubernetes-ci-logs/logs/periodic-kueue-test-scheduling-perf-main/2012374868804243456/build-log.txt
