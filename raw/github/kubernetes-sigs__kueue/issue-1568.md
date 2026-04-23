# Issue #1568: Admitted RayJobs remain in pending state when `manageJobsWithoutQueueName` is true

**Summary**: Admitted RayJobs remain in pending state when `manageJobsWithoutQueueName` is true

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1568

**Last updated**: 2024-12-17T08:57:57Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@astefanutti](https://github.com/astefanutti)
- **Created**: 2024-01-11T11:21:46Z
- **Updated**: 2024-12-17T08:57:57Z
- **Closed**: 2024-12-17T08:57:37Z
- **Labels**: `kind/bug`
- **Assignees**: [@kaisoz](https://github.com/kaisoz)
- **Comments**: 15

## Description

**What happened**:

When a RayJob managed by Kueue configured with `manageJobsWithoutQueueName` is admitted, it remains in pending state.

The Job that KubeRay creates to submit the actual job to the Ray cluster stays in suspended state.

**What you expected to happen**:

The RayJob should run successfully.

**How to reproduce it (as minimally and precisely as possible)**:

1. Set `manageJobsWithoutQueueName: true` is Kueue configuration
2. Create a RayJob

**Anything else we need to know?**:

Relates to #1434.

**Environment**:
- Kubernetes version (use `kubectl version`): v1.25.3
- Kueue version (use `git describe --tags --dirty --always`): v0.6.0-devel-146-ged81667f-dirty

## Discussion

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-04-10T11:30:05Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-04-10T12:48:24Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-07-09T13:40:46Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-08-08T14:03:46Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-08-14T16:22:54Z

/remove-lifecycle rotten

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-11-12T16:52:02Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-12T14:38:04Z

I'm wondering if this is more related to https://github.com/kubernetes-sigs/kueue/issues/1434 or to the child-owner management. I think there has been numerous changes in Kueue to the child-parent management so would be good to re-test e2e if this remains a problem.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-12T14:39:31Z

cc @dgrove-oss @andrewsykim who recently worked on related aspects of the problem.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-12T14:40:36Z

/remove-lifecycle stale 
The issue is looking for a contributor to re-test it e2e

### Comment by [@kaisoz](https://github.com/kaisoz) — 2024-12-12T14:52:23Z

/assign

I can take care of this, but if any other contributor also wants to have a look is more than fine for me 😊

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2024-12-12T21:50:57Z

Assuming kuberay links the RayJob and the RayCluster via a controller ref, then I agree this should work now.

### Comment by [@andrewsykim](https://github.com/andrewsykim) — 2024-12-12T23:38:56Z

The submitter Job, that runs "ray job submit" may not be accounted for. But a reasonable workaround is adding labels to map that submitter Job to a specific local queue

### Comment by [@kaisoz](https://github.com/kaisoz) — 2024-12-17T08:41:53Z

I've tested this on both `main` and `v0.9.1` and I can confirm that this works now. For each version I've:

1. Deployed a `kind` cluster, `kueue` and the `Ray` operator
1. Modified the `kueue` CM and set `manageJobsWithoutQueueName: true` . Then I restarted the kueue controller pods
1. Applied the [single clusterqueue setup](https://kueue.sigs.k8s.io/examples/admin/single-clusterqueue-setup.yaml) from the examples
1. Deploy the RayJob from the [example](https://kueue.sigs.k8s.io/docs/tasks/run/rayjobs/)

And I can see that after deploying the rayjob

```
$> kubectl get rayjobs
NAME            JOB STATUS   DEPLOYMENT STATUS   RAY CLUSTER NAME                 START TIME             END TIME   AGE
rayjob-sample                Initializing        rayjob-sample-raycluster-jmmwb   2024-12-17T08:38:28Z              8s
```

The job is created and run
```
$> kubectl get jobs
NAME            STATUS    COMPLETIONS   DURATION   AGE
rayjob-sample   Running   0/1           3s         3s
```

```
$> kubectl describe job rayjob-sample   
Name:             rayjob-sample
Namespace:        default
Selector:         batch.kubernetes.io/controller-uid=cc396c82-06b5-48a5-8de7-ea093d003eeb
Labels:           app.kubernetes.io/created-by=kuberay-operator
                  ray.io/originated-from-cr-name=rayjob-sample
                  ray.io/originated-from-crd=RayJob
Annotations:      <none>
Controlled By:    RayJob/rayjob-sample
Parallelism:      1
Completions:      1
Completion Mode:  NonIndexed
Suspend:          false
Backoff Limit:    2
Start Time:       Tue, 17 Dec 2024 09:38:58 +0100
Pods Statuses:    0 Active (0 Ready) / 0 Succeeded / 2 Failed
Pod Template:
  Labels:  batch.kubernetes.io/controller-uid=cc396c82-06b5-48a5-8de7-ea093d003eeb
           batch.kubernetes.io/job-name=rayjob-sample
           controller-uid=cc396c82-06b5-48a5-8de7-ea093d003eeb
           job-name=rayjob-sample
  Containers:
   ray-job-submitter:
    Image:      rayproject/ray:2.9.0
    Port:       <none>
    Host Port:  <none>
    Command:
      ray
      job
      submit
      --address
      http://rayjob-sample-raycluster-jmmwb-head-svc.default.svc.cluster.local:8265
      --runtime-env-json
      {"env_vars":{"counter_name":"test_counter"},"pip":["requests==2.26.0","pendulum==2.1.2"]}
      --submission-id
      rayjob-sample-q9jht
      --
      python
      /home/ray/samples/sample_code.py
    Limits:
      cpu:     1
      memory:  1Gi
    Requests:
      cpu:     500m
      memory:  200Mi
    Environment:
      PYTHONUNBUFFERED:       1
      RAY_DASHBOARD_ADDRESS:  rayjob-sample-raycluster-jmmwb-head-svc.default.svc.cluster.local:8265
      RAY_JOB_SUBMISSION_ID:  rayjob-sample-q9jht
    Mounts:                   <none>
  Volumes:                    <none>
  Node-Selectors:             <none>
  Tolerations:                <none>
Events:
  Type    Reason            Age   From            Message
  ----    ------            ----  ----            -------
  Normal  SuccessfulCreate  21s   job-controller  Created pod: rayjob-sample-th89s
  Normal  SuccessfulCreate  8s    job-controller  Created pod: rayjob-sample-fg7zv
```

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-17T08:57:32Z

sgtm, thank you for testing @kaisoz . Still the automated sanity tests for Ray will be useful: https://github.com/kubernetes-sigs/kueue/issues/3829
/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-12-17T08:57:37Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1568#issuecomment-2547854257):

>sgtm, thank you for testing @kaisoz .
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
