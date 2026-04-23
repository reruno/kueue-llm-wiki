# Issue #5979: Fair Share Preemption with MultiKueue + Plain Pods - Preempted Pod not Terminated in the Manager Cluster

**Summary**: Fair Share Preemption with MultiKueue + Plain Pods - Preempted Pod not Terminated in the Manager Cluster

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5979

**Last updated**: 2026-02-19T11:54:08Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@gu-san](https://github.com/gu-san)
- **Created**: 2025-07-14T23:09:15Z
- **Updated**: 2026-02-19T11:54:08Z
- **Closed**: 2026-02-19T11:54:07Z
- **Labels**: `kind/bug`, `priority/important-soon`, `area/multikueue`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi), [@polinasand](https://github.com/polinasand)
- **Comments**: 8

## Description

Hi,

We have experienced some unexpected behaviour with the combination of Multikueue, Plain Pods and Fair Share preemption.  We believe we have followed the relevant documentation to set this up.  We can't find a reference in the documentation that this combination shouldn't work. Our apologies if we have missed something.

**What happened**:

When Plain Pods are Preempted to a Fair Share in MultiKueue, the preempted pod in the Worker cluster is terminated as expected, but the corresponding pod in the Manger Cluster remains in a `Running` state and is later rescheduled on a Worker Cluster.

**What you expected to happen**:

* We expected similar behaviour to single cluster Kueue behaviour with Plain Pods, which when a Pod is preempted it is terminated and deleted https://kueue.sigs.k8s.io/docs/tasks/run/plain_pods/#d-limitations
* We expected the preempted pod be terminated and deleted in *both* the workload and manager cluster and not rescheduled

**How to reproduce it (as minimally and precisely as possible)**:

1. enable integrations.frameworks - "pods" in manager config
2. enable fairSharing in manager config

```
fairSharing:
  enable: true
  preemptionStrategies: [LessThanOrEqualToFinalShare, LessThanInitialShare]
```

3. Setup Multi-Kueue - AdmissionCheck and MutiKueueConfig in the Manager Cluster referencing a Worker Cluster

4. Setup queues and cohorts as follows

	local-queue-1 -> cluster-queue-1 -> cohort-1
	local-queue-2-> cluster-queue-2 -> cohort-2
	cluster-queue-1 nominal cpu quota = 1
	cluster-queue-2 nominal cpu quota = 1

	enable preemption on both cluster queues
```
preemption:
  withinClusterQueue: LowerOrNewerEqualPriority
  borrowWithinCohort:
    policy: Never
  reclaimWithinCohort: Any
```

	cohort-1 (with parent root-cohort): weight 0.50
	cohort-2 (with parent root-cohort): weight 0.50

3. schedule 2 x pods in queue-1 each requiring 1 cpu, 1 cpu will be borrowed from cohort-2/cluster-queue-2
```
  labels:
    kueue.x-k8s.io/queue-name: local-queue-1
```
Resulting state - 
	  manager cluster:
		sleep-job-queue1-2wcd8  - Running
		sleep-job-queue1-65ft5 - Running
	  workload cluster:
		sleep-job-queue1-2wcd8  -Running
		sleep-job-queue1-65ft5 - Running
4. schedule 2 x pods in queue-2 each requiring 1 cpu
```
  labels:
    kueue.x-k8s.io/queue-name: local-queue-2
```

	1 x pod from cluster-queue-1 will be preempted and terminated which is what happens in the workload cluster, but this termination is not reflected in the manager cluster

Resulting state - 
	  manager cluster:
		sleep-job-queue1-2wcd8 - Running  (**this should have also been terminated**)
		sleep-job-queue1-65ft5 - Running
		sleep-job-queue2-5pvlp - Running
		sleep-job-queue2-qvbhz - Pending
	  workload cluster:
		sleep-job-queue1-65ft5 - Running
		sleep-job-queue2-5pvlp - Running

Please let us know if you require further information.

**Anything else we need to know?**:

By expanding the `stopReason` condition on this line to also include `WorkloadEvictedDueToPreempted` we were able to achieve the expected behaviour but we are unsure if this would be a valid fix -  https://github.com/kubernetes-sigs/kueue/blob/v0.12.3/pkg/controller/jobs/pod/pod_controller.go#L451

We are happy to submit this fix or help by working on a suggested change for this.

**Environment**:
- Kubernetes version (use `kubectl version`):
	Client Version: v1.33.0
	Kustomize Version: v5.6.0
	Server Version: v1.31.9-eks-5d4a308
- Kueue version (use `git describe --tags --dirty --always`):
    image: registry.k8s.io/kueue/kueue:v0.12.3
- Cloud provider or hardware configuration:
	EKS
- OS (e.g: `cat /etc/os-release`):
	- Amazon Linux 2023.7.20250527
- Kernel (e.g. `uname -a`):
	- Linux ip-10-233-144-137.redacted 6.1.134-152.225.amzn2023.x86_64 #1 SMP PREEMPT_DYNAMIC Wed May  7 09:10:59 UTC 2025 x86_64 x86_64 x86_64 GNU/Linux
- Install tools:
- Others:

## Discussion

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-10-12T23:38:44Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-11-11T23:46:08Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-10T08:42:30Z

/remove-lifecycle rotten

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-10T08:44:00Z

I think this is an example of https://github.com/kubernetes-sigs/kueue/issues/7350
/assign @mbobrovskyi 
tentatively to check if this scenario is fixed, and maybe also adding a test for that as part of the fix

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T08:26:53Z

/area multikueue
/priority important-soon

### Comment by [@polinasand](https://github.com/polinasand) — 2026-02-19T11:38:01Z

/assign
The issue is not reproducible for kueue:v0.15 and can be closed

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-19T11:54:01Z

/close
Thank you for the feedback 👍

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-02-19T11:54:07Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/5979#issuecomment-3926781196):

>/close
>Thank you for the feedback 👍 


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
