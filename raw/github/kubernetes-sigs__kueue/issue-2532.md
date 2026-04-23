# Issue #2532: Flaky integration:  JobSet controller when basic setup Should allow to create jobset with one replicated job replica count 0

**Summary**: Flaky integration:  JobSet controller when basic setup Should allow to create jobset with one replicated job replica count 0

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2532

**Last updated**: 2024-07-09T20:45:41Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2024-07-03T19:14:22Z
- **Updated**: 2024-07-09T20:45:41Z
- **Closed**: 2024-07-09T06:16:15Z
- **Labels**: `kind/bug`
- **Assignees**: [@IrvingMg](https://github.com/IrvingMg), [@trasc](https://github.com/trasc)
- **Comments**: 13

## Description


**What happened**:

```
{Timed out after 5.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/integration/controller/jobs/jobset/jobset_controller_test.go:347 with:
Expected
    <bool>: false
to be true failed [FAILED] Timed out after 5.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/integration/controller/jobs/jobset/jobset_controller_test.go:347 with:
Expected
    <bool>: false
to be true
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/integration/controller/jobs/jobset/jobset_controller_test.go:348 @ 07/03/24 18:35:53.861
}
```

**What you expected to happen**:

No failure

**How to reproduce it (as minimally and precisely as possible)**:

https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/2531/pull-kueue-test-integration-release-0-7/1808569390875021312

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

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-07-03T19:14:42Z

It happened in 0.7, but I suppose it also could happen in the main branch.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-07-03T19:16:16Z

/assign @IrvingMg

### Comment by [@trasc](https://github.com/trasc) — 2024-07-04T13:59:04Z

/assign

### Comment by [@trasc](https://github.com/trasc) — 2024-07-05T14:24:16Z

@alculquicondor 

In my opinion this is just a timing issue due to overloaded test infra., since we hit all the kueue points that should unsuspend the jobset:

```
2024-07-03T18:35:48.860228453Z	LEVEL(-2)	jobframework/reconciler.go:308	Reconciling Job	{"controller": "jobset", "controllerGroup": "jobset.x-k8s.io", "controllerKind": "JobSet", "JobSet": {"name":"mix-jobset","namespace":"jobset-5tpgw"}, "namespace": "jobset-5tpgw", "name": "mix-jobset", "reconcileID": "c5ac7287-d35d-4718-a074-b8d243b46c0e", "job": "jobset-5tpgw/mix-jobset", "gvk": "jobset.x-k8s.io/v1alpha2, Kind=JobSet"}
2024-07-03T18:35:48.860420986Z	LEVEL(-3)	jobframework/reconciler.go:390	update reclaimable counts if implemented by the job	{"controller": "jobset", "controllerGroup": "jobset.x-k8s.io", "controllerKind": "JobSet", "JobSet": {"name":"mix-jobset","namespace":"jobset-5tpgw"}, "namespace": "jobset-5tpgw", "name": "mix-jobset", "reconcileID": "c5ac7287-d35d-4718-a074-b8d243b46c0e", "job": "jobset-5tpgw/mix-jobset", "gvk": "jobset.x-k8s.io/v1alpha2, Kind=JobSet"}
2024-07-03T18:35:48.860453157Z	LEVEL(-2)	jobframework/reconciler.go:453	Job admitted, unsuspending	{"controller": "jobset", "controllerGroup": "jobset.x-k8s.io", "controllerKind": "JobSet", "JobSet": {"name":"mix-jobset","namespace":"jobset-5tpgw"}, "namespace": "jobset-5tpgw", "name": "mix-jobset", "reconcileID": "c5ac7287-d35d-4718-a074-b8d243b46c0e", "job": "jobset-5tpgw/mix-jobset", "gvk": "jobset.x-k8s.io/v1alpha2, Kind=JobSet"}
```

and get a second reconcile that confirms the jobset is unsuspended:

```
2024-07-03T18:35:48.87462375Z	LEVEL(-2)	jobframework/reconciler.go:308	Reconciling Job	{"controller": "jobset", "controllerGroup": "jobset.x-k8s.io", "controllerKind": "JobSet", "JobSet": {"name":"mix-jobset","namespace":"jobset-5tpgw"}, "namespace": "jobset-5tpgw", "name": "mix-jobset", "reconcileID": "3202f822-e25e-4f1c-a463-e2b38339af1c", "job": "jobset-5tpgw/mix-jobset", "gvk": "jobset.x-k8s.io/v1alpha2, Kind=JobSet"}
2024-07-03T18:35:48.874784503Z	LEVEL(-3)	jobframework/reconciler.go:390	update reclaimable counts if implemented by the job	{"controller": "jobset", "controllerGroup": "jobset.x-k8s.io", "controllerKind": "JobSet", "JobSet": {"name":"mix-jobset","namespace":"jobset-5tpgw"}, "namespace": "jobset-5tpgw", "name": "mix-jobset", "reconcileID": "3202f822-e25e-4f1c-a463-e2b38339af1c", "job": "jobset-5tpgw/mix-jobset", "gvk": "jobset.x-k8s.io/v1alpha2, Kind=JobSet"}
2024-07-03T18:35:48.874810343Z	LEVEL(-3)	jobframework/reconciler.go:499	Job running with admitted workload, nothing to do	{"controller": "jobset", "controllerGroup": "jobset.x-k8s.io", "controllerKind": "JobSet", "JobSet": {"name":"mix-jobset","namespace":"jobset-5tpgw"}, "namespace": "jobset-5tpgw", "name": "mix-jobset", "reconcileID": "3202f822-e25e-4f1c-a463-e2b38339af1c", "job": "jobset-5tpgw/mix-jobset", "gvk": "jobset.x-k8s.io/v1alpha2, Kind=JobSet"}
```

For now, I wold just keep this issue open for a couple more days to see if this issue is observed again and not just increase the timeout.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-07-05T18:10:36Z

```
2024-07-03T18:35:48.874810343Z	LEVEL(-3)	jobframework/reconciler.go:499	Job running with admitted workload, nothing to do
{"controller": "jobset", "controllerGroup": "jobset.x-k8s.io", "controllerKind": "JobSet", "JobSet": {"name":"mix-jobset","namespace":"jobset-5tpgw"}, "namespace": "jobset-5tpgw", "name": "mix-jobset", "reconcileID": "3202f822-e25e-4f1c-a463-e2b38339af1c", "job": "jobset-5tpgw/mix-jobset", "gvk": "jobset.x-k8s.io/v1alpha2, Kind=JobSet"}
```

That's actually 5s earlier than the error reports:

```
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/integration/controller/jobs/jobset/jobset_controller_test.go:348 @ 07/03/24 18:35:53.861
```

Are you sure it didn't get unsuspended later on?

The controller and the test share the same client, so I wouldn't expect them to see different objects.

### Comment by [@trasc](https://github.com/trasc) — 2024-07-08T13:39:52Z

There are no other events processes by any of the integration test code, and there are no other components running. 

To get more info on scenarios like this, we can add something as #2549 to get the logs from the api sever, the test time is similar but the logs size get 9x bigger with a `v=3` log level.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-07-08T16:38:38Z

I'm suspecting that CPU steals sometimes happen since recent integration tests often cusumed around 6 cores based on these metrics: https://monitoring-eks.prow.k8s.io/d/96Q8oOOZk/builds?orgId=1&from=now-7d&to=now&var-org=kubernetes-sigs&var-repo=kueue&var-job=pull-kueue-test-integration-main&var-build=All&refresh=30s

But, we restrict the availability of cores here: https://github.com/kubernetes/test-infra/blob/7daf0254e022e4f48a4027a0853adb56539c6e70/config/jobs/kubernetes-sigs/kueue/kueue-presubmits-main.yaml#L52-L60

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-07-08T19:40:49Z

If we don't have any evidence of a bug, then let's close this for now.

We know that the test infra is running out of resources overall, since sometimes we can't even get our jobs scheduled :(

### Comment by [@trasc](https://github.com/trasc) — 2024-07-09T06:16:11Z

/close

We can still keep #2549 , with logging disabled by default as it can be useful at a later time.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-07-09T06:16:15Z

@trasc: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/2532#issuecomment-2216673220):

>/close
>
>We can still keep #2549 , with logging disabled by default as it can be useful at a later time.
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@trasc](https://github.com/trasc) — 2024-07-09T06:57:43Z

> I'm suspecting that CPU steals sometimes happen since recent integration tests often cusumed around 6 cores based on these metrics: https://monitoring-eks.prow.k8s.io/d/96Q8oOOZk/builds?orgId=1&from=now-7d&to=now&var-org=kubernetes-sigs&var-repo=kueue&var-job=pull-kueue-test-integration-main&var-build=All&refresh=30s
> 
> But, we restrict the availability of cores here: https://github.com/kubernetes/test-infra/blob/7daf0254e022e4f48a4027a0853adb56539c6e70/config/jobs/kubernetes-sigs/kueue/kueue-presubmits-main.yaml#L52-L60

Overall I guess we can think of tuning cpu values we have  `GOMAXPROCS` == `limits.cpu` but we run at least 3 go apps during the integration tests (the_test, apiserver, etcd) and in theory we can get 18 cpu usage.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-07-09T15:15:44Z

maybe we can do `GOMAXPROCS = 2/3 * limits.cpu`? I wouldn't do just 1/3, because most of the time a single binary is not using all the cpus available to it.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-07-09T20:45:40Z

> maybe we can do `GOMAXPROCS = 2/3 * limits.cpu`? I wouldn't do just 1/3, because most of the time a single binary is not using all the cpus available to it.

SGTM
