# Issue #8713: RoleTracker: reports as "follower" replicas which are actually "leaders"

**Summary**: RoleTracker: reports as "follower" replicas which are actually "leaders"

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8713

**Last updated**: 2026-01-23T16:55:28Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-01-21T08:47:38Z
- **Updated**: 2026-01-23T16:55:28Z
- **Closed**: 2026-01-23T16:55:28Z
- **Labels**: `kind/bug`, `priority/important-soon`
- **Assignees**: [@IrvingMg](https://github.com/IrvingMg)
- **Comments**: 3

## Description

**What happened**:

The RoleTracker does not report correctly roles for controllers which don't use controller-runtime leader election. 

This is because many of our controllers implement our leader election to keep caches warm while "following". 

This makes investigation of user issues harder, because it is misleading.

**What you expected to happen**:

For example we can see that controllers from the leading replica of Kueue report as follower in our e2e tests:

https://storage.googleapis.com/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-main-1-35/2013832293147217920/artifacts/run-test-e2e-singlecluster-1.35.0/kind-worker/pods/kueue-system_kueue-controller-manager-9f487f597-zw8nc_ade98a03-13ac-4058-8d92-cfcf7513f1d1/manager/0.log

we can see:

```
2026-01-21T04:55:05.048339045Z stderr F 2026-01-21T04:55:05.048126373Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:808	Workload create event	{"replica-role": "follower", "workload": {"name":"job-test-job-1-d5d24","namespace":"e2e-gfd7h"}, "queue": "a", "status": "pending"}
```
and the other replica of Kueue also reported as "follower", see: https://storage.googleapis.com/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-main-1-35/2013832293147217920/artifacts/run-test-e2e-singlecluster-1.35.0/kind-worker2/pods/kueue-system_kueue-controller-manager-9f487f597-gf6j2_62791bf4-0f79-40f9-977b-c3b2dea763e4/manager/0.log

```
2026-01-21T04:55:05.048396186Z stderr F 2026-01-21T04:55:05.048161693Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:808	Workload create event	{"replica-role": "follower", "workload": {"name":"job-test-job-1-d5d24","namespace":"e2e-gfd7h"}, "queue": "a", "status": "pending"}
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-21T08:47:50Z

cc @IrvingMg @mbobrovskyi ptal

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-21T08:57:07Z

/priority important-soon
I think this is fairly important bug, because it provides misleading information

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2026-01-21T09:19:32Z

/assign
