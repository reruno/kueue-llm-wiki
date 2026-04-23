# Issue #5303: [flaky test] Job when Creating a Job should admit a Job to TAS Block if Rack preferred

**Summary**: [flaky test] Job when Creating a Job should admit a Job to TAS Block if Rack preferred

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5303

**Last updated**: 2025-10-03T15:40:55Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-05-20T15:45:39Z
- **Updated**: 2025-10-03T15:40:55Z
- **Closed**: 2025-10-03T15:40:54Z
- **Labels**: `kind/bug`, `kind/flake`, `lifecycle/rotten`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 6

## Description

/kind flake

**What happened**:

failure on periodic build https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-tas-release-0-10/1924774246098145280

**What you expected to happen**:

no failure

**How to reproduce it (as minimally and precisely as possible)**:

ci

**Anything else we need to know?**:

```
{Timed out after 45.004s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/tas/job_test.go:170 with:
Expected
    <[]v1.Condition | len:2, cap:4>: [
        {
            Type: "QuotaReserved",
            Status: "True",
            ObservedGeneration: 1,
            LastTransitionTime: {
                Time: 2025-05-20T10:43:38Z,
            },
            Reason: "QuotaReserved",
            Message: "Quota reserved in ClusterQueue cluster-queue",
        },
        {
            Type: "Admitted",
            Status: "True",
            ObservedGeneration: 1,
            LastTransitionTime: {
                Time: 2025-05-20T10:43:38Z,
            },
            Reason: "Admitted",
            Message: "The workload is admitted",
        },
    ]
to have condition Finished and status True failed [FAILED] Timed out after 45.004s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/tas/job_test.go:170 with:
Expected
    <[]v1.Condition | len:2, cap:4>: [
        {
            Type: "QuotaReserved",
            Status: "True",
            ObservedGeneration: 1,
            LastTransitionTime: {
                Time: 2025-05-20T10:43:38Z,
            },
            Reason: "QuotaReserved",
            Message: "Quota reserved in ClusterQueue cluster-queue",
        },
        {
            Type: "Admitted",
            Status: "True",
            ObservedGeneration: 1,
            LastTransitionTime: {
                Time: 2025-05-20T10:43:38Z,
            },
            Reason: "Admitted",
            Message: "The workload is admitted",
        },
    ]
to have condition Finished and status True
In [It] at: /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/tas/job_test.go:171 @ 05/20/25 10:44:23.398
}
```

## Discussion

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-05-29T13:33:42Z

/assign

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-06-05T14:34:56Z

Seems that pods were admitted, 

```
2025-05-20T10:43:38.178734131Z stderr F 2025-05-20T10:43:38.178449777Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:689	Workload update event	{"workload": {"name":"job-test-job-df7af","namespace":"e2e-tas-job-5774d"}, "queue": "main", "status": "admitted", "prevStatus": "pending", "clusterQueue": "cluster-queue"}
```

but never ungated as this was logged several times for the failed test.

```
2025-05-20T10:44:23.478382532Z stderr F 2025-05-20T10:44:23.47821949Z	ERROR	tas/topology_ungater.go:385	failed to read rank information from Pods	{"controller": "tas_topology_ungater", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Workload", "Workload": {"name":"job-test-job-df7af","namespace":"e2e-tas-job-5774d"}, "namespace": "e2e-tas-job-5774d", "name": "job-test-job-df7af", "reconcileID": "a2e470b3-a0ca-40a8-973d-c6c510a6c5ca", "workload": "e2e-tas-job-5774d/job-test-job-df7af", "error": "label not found: no label \"batch.kubernetes.io/job-completion-index\" for Pod \"e2e-tas-job-5774d/test-job-wjc9b\""}
2025-05-20T10:44:23.478393062Z stderr F sigs.k8s.io/kueue/pkg/controller/tas.readRanksIfAvailable
2025-05-20T10:44:23.478398152Z stderr F 	/workspace/pkg/controller/tas/topology_ungater.go:385
2025-05-20T10:44:23.478403492Z stderr F sigs.k8s.io/kueue/pkg/controller/tas.assignGatedPodsToDomains
2025-05-20T10:44:23.478408172Z stderr F 	/workspace/pkg/controller/tas/topology_ungater.go:302
2025-05-20T10:44:23.478452392Z stderr F sigs.k8s.io/kueue/pkg/controller/tas.(*topologyUngater).Reconcile
2025-05-20T10:44:23.478458763Z stderr F 	/workspace/pkg/controller/tas/topology_ungater.go:182
2025-05-20T10:44:23.478463533Z stderr F sigs.k8s.io/kueue/pkg/controller/core.(*leaderAwareReconciler).Reconcile
2025-05-20T10:44:23.478467883Z stderr F 	/workspace/pkg/controller/core/leader_aware_reconciler.go:77
2025-05-20T10:44:23.478473053Z stderr F sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).Reconcile
2025-05-20T10:44:23.478477593Z stderr F 	/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:116
2025-05-20T10:44:23.478482223Z stderr F sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).reconcileHandler
2025-05-20T10:44:23.478486713Z stderr F 	/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:303
2025-05-20T10:44:23.478491473Z stderr F sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).processNextWorkItem
2025-05-20T10:44:23.478496023Z stderr F 	/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:263
2025-05-20T10:44:23.478500663Z stderr F sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).Start.func2.2
2025-05-20T10:44:23.478505613Z stderr F 	/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:224
```

It happened first time in the job history and it's really hard to accompany this with any change that should occur before May 20th.

It doesn't make sense because, that would require feature to be turned off...
```go
func (j *Job) PodSets() []kueue.PodSet {
[...]
	if features.Enabled(features.TopologyAwareScheduling) {
		podSet.TopologyRequest = jobframework.PodSetTopologyRequest(
			&j.Spec.Template.ObjectMeta,
			ptr.To(batchv1.JobCompletionIndexAnnotation),
			nil, nil,
		)
	}
```

Checking further, no success in reproduction so far.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-09-03T14:57:35Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle stale`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-10-03T15:29:20Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle rotten

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-03T15:40:49Z

/close
We don't have any logs to investigate at this point, and we don't have more reports of the issue repeating itself.

Since then there have been a couple of improvements to the stability of e2e tests for TAS, for example making sure Pods from previous Jobs are deleted before starting a new one. So, I suspect it is already fixed.

Let's re-open if this reoccurs.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-10-03T15:40:55Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/5303#issuecomment-3366224928):

>/close
>We don't have any logs to investigate at this point, and we don't have more reports of the issue repeating itself.
>
>Since then there have been a couple of improvements to the stability of e2e tests for TAS, for example making sure Pods from previous Jobs are deleted before starting a new one. So, I suspect it is already fixed.
>
>Let's re-open if this reoccurs.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
