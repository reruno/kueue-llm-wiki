# Issue #911: Flaky E2E test: when Creating a Job With Queueing Should unsuspend a job and set nodeSelectors

**Summary**: Flaky E2E test: when Creating a Job With Queueing Should unsuspend a job and set nodeSelectors

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/911

**Last updated**: 2023-06-27T21:26:19Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2023-06-27T20:05:18Z
- **Updated**: 2023-06-27T21:26:19Z
- **Closed**: 2023-06-27T21:26:19Z
- **Labels**: `kind/bug`
- **Assignees**: [@tenzen-y](https://github.com/tenzen-y)
- **Comments**: 11

## Description

**What happened**:

Flaky test https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/903/pull-kueue-test-e2e-main-1-24/1673404497516302336

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`): 1.24
- Kueue version (use `git describe --tags --dirty --always`): main
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-06-27T20:06:06Z

/assign @trasc

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-06-27T20:21:57Z

cc @tenzen-y

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-06-27T20:31:42Z

We need to check which verification failed. `workload.IsAdmitted(createdWorkload)` vs `apimeta.IsStatusConditionTrue(createdWorkload.Status.Conditions, kueue.WorkloadFinished)`.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-06-27T20:36:09Z

kueue logs:
```
{"level":"Level(-2)","ts":"2023-06-26T19:00:31.304074482Z","logger":"scheduler","caller":"scheduler/scheduler.go:400","msg":"Workload successfully admitted and assigned flavors","workload":{"name":"job-test-job-11501","namespace":"e2e-rh7w4"},"clusterQueue":{"name":"cluster-queue"},"assignments":[{"name":"main","flavors":{"cpu":"on-demand","memory":"on-demand"},"resourceUsage":{"cpu":"1","memory":"20Mi"},"count":1}]}
```

k8s job controller logs:

```
I0626 19:01:13.242968       1 event.go:294] "Event occurred" object="e2e-rh7w4/test-job" fieldPath="" kind="Job" apiVersion="batch/v1" type="Normal" reason="Completed" message="Job completed"
```

That's more than 30s later. I think the test just timed out.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-06-27T20:39:28Z

> kueue logs:
> 
> ```
> {"level":"Level(-2)","ts":"2023-06-26T19:00:31.304074482Z","logger":"scheduler","caller":"scheduler/scheduler.go:400","msg":"Workload successfully admitted and assigned flavors","workload":{"name":"job-test-job-11501","namespace":"e2e-rh7w4"},"clusterQueue":{"name":"cluster-queue"},"assignments":[{"name":"main","flavors":{"cpu":"on-demand","memory":"on-demand"},"resourceUsage":{"cpu":"1","memory":"20Mi"},"count":1}]}
> ```
> 
> k8s job controller logs:
> 
> ```
> I0626 19:01:13.242968       1 event.go:294] "Event occurred" object="e2e-rh7w4/test-job" fieldPath="" kind="Job" apiVersion="batch/v1" type="Normal" reason="Completed" message="Job completed"
> ```
> 
> That's more than 30s later. I think the test just timed out.

I see. Maybe the kube-apiserver's load is heavy.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-06-27T20:42:39Z

Ah, we didn't increase resource requests in https://github.com/kubernetes/test-infra/blob/1c382cce4cc1d6970d19294d13d9294cb999c9d6/config/jobs/kubernetes-sigs/kueue/kueue-presubmits-main.yaml#L162-L168 although we increase kind nodes from 1 to 3.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-06-27T20:43:40Z

Previously, we had only a control-plan. But currently we have 3 nodes, a control-plan, and two workers.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-06-27T20:43:41Z

Yes, I was going to say the same thing :)
Let's increase that
/assign @tenzen-y 
/unassign @trasc

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-06-27T20:57:50Z

I created: https://github.com/kubernetes/test-infra/pull/29948

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-06-27T21:26:15Z

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-06-27T21:26:19Z

@alculquicondor: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/911#issuecomment-1610242062):

>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
