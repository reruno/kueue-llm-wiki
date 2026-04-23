# Issue #158: Flaky integration test for the scheduler?

**Summary**: Flaky integration test for the scheduler?

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/158

**Last updated**: 2022-03-30T16:54:26Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2022-03-28T20:32:57Z
- **Updated**: 2022-03-30T16:54:26Z
- **Closed**: 2022-03-30T16:54:26Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 3

## Description

**What happened**:

The integration tests failed with a extraneous message in the logs:

```
ERROR	scheduler	Updating QueuedWorkload status	{"error": "resource name may not be empty"}
    sigs.k8s.io/kueue/pkg/scheduler.(*Scheduler).schedule
    	/home/prow/go/src/sigs.k8s.io/kueue/pkg/scheduler/scheduler.go:128
    k8s.io/apimachinery/pkg/util/wait.JitterUntilWithContext.func1
    	/home/prow/go/pkg/mod/k8s.io/apimachinery@v0.23.4/pkg/util/wait/wait.go:188
    k8s.io/apimachinery/pkg/util/wait.BackoffUntil.func1
    	/home/prow/go/pkg/mod/k8s.io/apimachinery@v0.23.4/pkg/util/wait/wait.go:155
    k8s.io/apimachinery/pkg/util/wait.BackoffUntil
    	/home/prow/go/pkg/mod/k8s.io/apimachinery@v0.23.4/pkg/util/wait/wait.go:156
    k8s.io/apimachinery/pkg/util/wait.JitterUntil
    	/home/prow/go/pkg/mod/k8s.io/apimachinery@v0.23.4/pkg/util/wait/wait.go:133
    k8s.io/apimachinery/pkg/util/wait.JitterUntilWithContext
    	/home/prow/go/pkg/mod/k8s.io/apimachinery@v0.23.4/pkg/util/wait/wait.go:188
    k8s.io/apimachinery/pkg/util/wait.UntilWithContext
    	/home/prow/go/pkg/mod/k8s.io/apimachinery@v0.23.4/pkg/util/wait/wait.go:99
    sigs.k8s.io/kueue/pkg/scheduler.(*Scheduler).Start
    	/home/prow/go/src/sigs.k8s.io/kueue/pkg/scheduler/scheduler.go:66
    sigs.k8s.io/kueue/test/integration/scheduler.managerAndSchedulerSetup.func1
    	/home/prow/go/src/sigs.k8s.io/kueue/test/integration/scheduler/suite_test.go:87
```

Full error log: https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/157/pull-kueue-test-integration-main/1508537482113716224

So somehow we got a QW without a name? The only way I could see this possibly happen is that we used a QW object without cloning it from the informer cache.

**What you expected to happen**:

No error

**How to reproduce it (as minimally and precisely as possible)**:

No idea. I will try to run the test multiple times.

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`): main
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-03-29T13:51:12Z

/reopen

It looks like there is still another bug https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/157/pull-kueue-test-integration-main/1508802194659348480

There is only one error in the log:

```
ERROR	scheduler	Admitting workload and assigning flavors	{"queuedWorkload": {"name":"job","namespace":"core-qsjsr"}, "clusterQueue": {"name":"cluster-queue-with-selector"}, "error": "Operation cannot be fulfilled on queuedworkloads.kueue.x-k8s.io \"job\": the object has been modified; please apply your changes to the latest version and try again"}
```

which is somewhat expected (there was probably a status update in-between). However, we should have retried, and I see no indication that it happened. So maybe there is a bug when re-queueing.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2022-03-29T13:51:24Z

@alculquicondor: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/158#issuecomment-1081899027):

>/reopen
>
>It looks like there is still another bug https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/157/pull-kueue-test-integration-main/1508802194659348480
>
>There is only one error in the log:
>
>```
>ERROR	scheduler	Admitting workload and assigning flavors	{"queuedWorkload": {"name":"job","namespace":"core-qsjsr"}, "clusterQueue": {"name":"cluster-queue-with-selector"}, "error": "Operation cannot be fulfilled on queuedworkloads.kueue.x-k8s.io \"job\": the object has been modified; please apply your changes to the latest version and try again"}
>```
>
>which is somewhat expected (there was probably a status update in-between). However, we should have retried, and I see no indication that it happened. So maybe there is a bug when re-queueing.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-03-29T21:05:06Z

This last failure has more informative logs

https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/163/pull-kueue-test-integration-main/1508910799555399680

There is QW update event after the workload is assumed. The scheduler never retries.
