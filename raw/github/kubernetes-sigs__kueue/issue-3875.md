# Issue #3875: Python example of how to delete/stop kueue jobs that are queues or in progress

**Summary**: Python example of how to delete/stop kueue jobs that are queues or in progress

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3875

**Last updated**: 2025-08-02T23:44:38Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@joshwhieb](https://github.com/joshwhieb)
- **Created**: 2024-12-17T22:52:06Z
- **Updated**: 2025-08-02T23:44:38Z
- **Closed**: 2025-08-02T23:44:37Z
- **Labels**: `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 5

## Description

In the kubernetes python examples there is submission of jobs but nothing on stopping/deleting jobs that are queued or in progress.  I can use the batchV1API instance in python and it works for jobs in progress but can't quite figure out how I stop jobs that are queued in kueue.  I believe the jobs are submitted to kueue as workloads but is there an API to delete workloads?

https://kueue.sigs.k8s.io/docs/tasks/run/python_jobs/

```
    namespace = 'default'
    group_id = 'f4336081-0079-4403-b9f4-55b4f4cda948'
    config = create_kubernetes_config(server, token, cert, key)
    batch_api_inst = kubernetes.client.BatchV1Api(kubernetes.client.ApiClient(configuration=config))
    ret = batch_api_inst.list_namespaced_job(
            namespace,
            label_selector=f"group_id={group_id}"
    )
    for j in ret.items:
         batch_api_inst.delete_namespaced_job(j.metadata.name, namespace)
```

EDIT:
Looking in the kueue workloads definitions I have to change the "active" field in the workloads so looks like I have to use a different API call to modify the workload fields.

https://kueue.sigs.k8s.io/docs/concepts/workload/

![image](https://github.com/user-attachments/assets/16ce1d9f-64db-4fa5-8a08-a8f4a519c389)

## Discussion

### Comment by [@joshwhieb](https://github.com/joshwhieb) — 2025-03-05T22:50:06Z

Found that including propagation_policy='Foreground' in the job delete also deletes the workload so that seems to work as a decent solution for the time being.

```
batch_api_inst.delete_namespaced_job(j.metadata.name, namespace, propagation_policy='Foreground', grace_period_seconds=0)
```

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-06-03T23:00:04Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-07-03T23:33:41Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-08-02T23:44:33Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues and PRs.

This bot triages issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Reopen this issue with `/reopen`
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/close not-planned

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-08-02T23:44:38Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3875#issuecomment-3146856796):

>The Kubernetes project currently lacks enough active contributors to adequately respond to all issues and PRs.
>
>This bot triages issues according to the following rules:
>- After 90d of inactivity, `lifecycle/stale` is applied
>- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
>- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed
>
>You can:
>- Reopen this issue with `/reopen`
>- Mark this issue as fresh with `/remove-lifecycle rotten`
>- Offer to help out with [Issue Triage][1]
>
>Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).
>
>/close not-planned
>
>[1]: https://www.kubernetes.dev/docs/guide/issue-triage/


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
