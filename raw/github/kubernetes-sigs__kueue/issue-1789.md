# Issue #1789: Workloads corresponding to Jobs deleted with --cascede=orphan still consume resources

**Summary**: Workloads corresponding to Jobs deleted with --cascede=orphan still consume resources

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1789

**Last updated**: 2026-04-16T07:30:02Z

---

## Metadata

- **State**: open (reopened)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-03-04T10:49:37Z
- **Updated**: 2026-04-16T07:30:02Z
- **Closed**: —
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 23

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->
**What happened**:

Job deleted with --cascade=orphan continues to reserve ClusterQueue resources.

Note this is a "known" issue, which is a follow up to https://github.com/kubernetes-sigs/kueue/issues/1726

**What you expected to happen**:

Jobs deleted with --cascade=orphan should free the cluster resources.

**How to reproduce it (as minimally and precisely as possible)**:

1. Create a job with
```yaml
apiVersion: batch/v1

kind: Job
metadata:
  name: sample-job
  namespace: default
  labels:
    kueue.x-k8s.io/queue-name: user-queue
spec:
  parallelism: 3
  completions: 3
  suspend: true
  template:
    spec:
      containers:
      - name: dummy-job
        image: gcr.io/k8s-staging-perf-tests/sleep:v0.0.3
        args: ["1800s"]
        resources:
          requests:
            cpu: "1"
            memory: "200Mi"
      restartPolicy: Never
```
2. Delete the job with `kubectl delete job/sample-job --cascade=orphan`

Issue: The deleted job continues to reserve cluster queue resources:

`kubectl get clusterqueue -oyaml` returns:

```yaml
...
  status:
    admittedWorkloads: 1
    conditions:
    - lastTransitionTime: "2024-03-04T10:41:42Z"
      message: Can admit new workloads
      reason: Ready
      status: "True"
      type: Active
    flavorsReservation:
    - name: default-flavor
      resources:
      - borrowed: "0"
        name: cpu
        total: "3"
      - borrowed: "0"
        name: memory
        total: 600Mi
    flavorsUsage:
    - name: default-flavor
      resources:
      - borrowed: "0"
        name: cpu
        total: "3"
      - borrowed: "0"
        name: memory
        total: 600Mi
    pendingWorkloads: 0
    reservingWorkloads: 1
```

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-06-02T11:21:42Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-06-03T15:39:40Z

/remove-lifecycle stale

I think that this is still a valid, known issue.
I think that mentioning this in the documentation would be worth it.

### Comment by [@mwysokin](https://github.com/mwysokin) — 2024-08-08T11:27:05Z

I have some draft code that deals with orphaned Workloads that didn't make it to another issue (https://github.com/kubernetes-sigs/kueue/issues/1618) in order not to pollute it. I'll prepare a PR soon.

### Comment by [@mwysokin](https://github.com/mwysokin) — 2024-08-08T11:27:18Z

/assign

### Comment by [@mwysokin](https://github.com/mwysokin) — 2024-08-08T11:31:45Z

@mimowo @tenzen-y I don't think it makes sense to create time-based retention policies for orphaned Workloads like in (https://github.com/kubernetes-sigs/kueue/issues/1618). I think orphaned Workloads should be removed right away after their Job was deleted. The question is whether it should be something happening always or whether there should be a switch possibly in the new `ObjectRetentionPolicies` section. It could be something like: `OrphanedWorkloadsDeletion` or `OrpanedWorkloadsRetention` that would be a boolean switch deciding whether to keep or delete oraphen workloads. WDYT?

### Comment by [@mwysokin](https://github.com/mwysokin) — 2024-08-08T13:11:10Z

Unless I get other feedback I'm going to use @mimowo's comment in the other thread as feedback so that he doesn't need to repeat himself.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-08-09T06:01:12Z

> @mimowo @tenzen-y I don't think it makes sense to create time-based retention policies for orphaned Workloads like in (#1618). I think orphaned Workloads should be removed right away after their Job was deleted.

On the second thought I think it might be better to honor user's choice of using "orphan" mode. We should just transition the workloads to the "Finished" state, so that they don't occupy quota any longer. With the new mechanism they will be collected then.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-11-07T06:01:59Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-07T07:49:26Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-02-05T08:08:02Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-05T08:12:00Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-05-06T08:19:17Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-06T08:23:13Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-08-04T09:02:35Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-07T08:24:12Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-11-05T08:30:05Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-05T08:37:07Z

/remove-lifecycle stale
/unassign mwysokin
I think we completed https://github.com/kubernetes-sigs/kueue/pull/2742 which allows to cleanup workloads after a while.
However, I'm not clear what is the status of handling `kubectl delete job/<job-name> --cascade=orphan`.
It would be helpful if someone can double-check the current status, possibly the issue still exists (workloads still book capacity), but low priority. I guess to handle that we may need to check if the Workload is orphaned, and if so release the quota.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-02-03T09:16:43Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-03T09:22:49Z

/remove-lifecycle stale

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-06T18:48:22Z

/priority important-longerm

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-02-06T18:48:25Z

@mimowo: The label(s) `priority/important-longerm` cannot be applied, because the repository doesn't have them.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1789#issuecomment-3862046272):

>/priority important-longerm


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mimowo](https://github.com/mimowo) — 2026-04-16T07:29:55Z

/reopen
This is not yet addressed by https://github.com/kubernetes-sigs/kueue/pull/10274

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-04-16T07:30:02Z

@mimowo: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1789#issuecomment-4258174800):

>/reopen
>This is not yet addressed by https://github.com/kubernetes-sigs/kueue/pull/10274


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
