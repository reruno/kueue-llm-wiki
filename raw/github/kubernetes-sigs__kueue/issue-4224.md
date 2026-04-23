# Issue #4224: Stuck workload is not cleaned up/correctly handled

**Summary**: Stuck workload is not cleaned up/correctly handled

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4224

**Last updated**: 2025-06-11T11:23:50Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@woehrl01](https://github.com/woehrl01)
- **Created**: 2025-02-11T11:59:48Z
- **Updated**: 2025-06-11T11:23:50Z
- **Closed**: 2025-06-11T11:22:36Z
- **Labels**: `kind/bug`, `lifecycle/stale`
- **Assignees**: _none_
- **Comments**: 8

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

In our cluster we irregularly find stuck workloads which are multiple days old.

**What you expected to happen**:

That the workload is scheduled or garbage collected

**How to reproduce it (as minimally and precisely as possible)**:

**Anything else we need to know?**:

This is the workload which is "stuck":

```yaml
apiVersion: kueue.x-k8s.io/v1beta1
kind: Workload
metadata:
  creationTimestamp: "2024-11-29T00:39:00Z"
  finalizers:
  - kueue.x-k8s.io/resource-in-use
  generation: 1
  labels:
    kueue.x-k8s.io/job-uid: 2eae97f8-63f4-4ba6-9930-4c526f0ec781
  name: job-action
  namespace: default
  ownerReferences:
  - apiVersion: batch/v1
    blockOwnerDeletion: true
    controller: true
    kind: Job
    name: action
    uid: 2eae97f8-63f4-4ba6-9930-4c526f0ec781
  resourceVersion: "6456552770"
  uid: c69d69e1-7869-4bff-9282-9cae630cfdd7
spec:
  active: true
  podSets:
  - count: 1
    name: main
    template:
      metadata:
        labels:
          kueue.x-k8s.io/queue-name: queue
      spec:
        containers:
        - args:
          - -c
          - echo "hello world"
          command:
          - sh
          image: busybox
          imagePullPolicy: Always
          name: php-cli
          resources:
            limits:
              memory: 4Gi
            requests:
              cpu: 150m
              memory: "205785634"
          terminationMessagePath: /dev/termination-log
          terminationMessagePolicy: File
        dnsPolicy: ClusterFirst
        restartPolicy: Never
        securityContext:
          runAsGroup: 0
          runAsUser: 0
        terminationGracePeriodSeconds: 30
  queueName: queue
status:
  admission:
    clusterQueue: queue
    podSetAssignments:
    - count: 1
      flavors:
        cpu: on-demand
        memory: on-demand
      name: main
      resourceUsage:
        cpu: 150m
        memory: "205785634"
  conditions:
  - lastTransitionTime: "2024-11-29T03:03:26Z"
    message: Quota reserved in ClusterQueue queue
    observedGeneration: 1
    reason: QuotaReserved
    status: "True"
    type: QuotaReserved
  - lastTransitionTime: "2024-11-29T03:03:26Z"
    message: The workload is admitted
    observedGeneration: 1
    reason: Admitted
    status: "True"
    type: Admitted


```

**Environment**:
- Kubernetes version (use `kubectl version`): 1.31
- Kueue version (use `git describe --tags --dirty --always`): v0.10.1
- Cloud provider or hardware configuration: aws
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-11T12:35:00Z

What does it mean that the workload is stuck? Do you mean the pods get created by cannot get scheduled? 

If so then one option is to use waitForPodsReady. You can configure it to deactivate the workload after a couple of attempts. Then, you could have a small script to GC Deactivated workloads.

### Comment by [@woehrl01](https://github.com/woehrl01) — 2025-02-11T12:37:10Z

Stuck means that the job is not unsuspended. The workload is marked as submitted, but the job is not scheduled.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-11T12:54:26Z

weird, can you check events for the workload and the corresponding job?

### Comment by [@woehrl01](https://github.com/woehrl01) — 2025-02-11T12:56:14Z

Unfortunately not, in our case it is only detected if the workload is not executed for a day. Then all events are already gone. My assumption is that maybe the workload is updated, but the unsuspending of the job fails because of an api server error. Is this possible?

### Comment by [@woehrl01](https://github.com/woehrl01) — 2025-03-13T10:30:57Z

Hi,

we observed the same thing again on 0.10.1. It seems that the job is still "suspended: true" but the workload is already "active". This state is not getting resolved during a controller restart.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-06-11T11:09:15Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-11T11:22:31Z

The recommended way of dealing with such workloads in 0.12 is:
1. configure waitForPodsReady to trigger deactivation of the workload
2. configure object retention policy for deactived workloads to delete them after this issue is done: https://github.com/kubernetes-sigs/kueue/issues/4471, see more details with example in [Setup garbage-collection of workload](https://kueue.sigs.k8s.io/docs/tasks/manage/setup_object_retention_policy/#example)

Posting the example config here (which you may need to tune for your needs as 1min might be too short):
```yaml
  objectRetentionPolicies:
    workloads:
      afterFinished: "1m"
      afterDeactivatedByKueue: "1m"
  waitForPodsReady:
    enable: true
    timeout: 2m
    recoveryTimeout: 1m
    blockAdmission: true
    requeuingStrategy:
      backoffLimitCount: 0
```

/close
As I believe the issue is solved. Feel free to re-open, or open follow up issue if there are still some gaps.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-06-11T11:22:36Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4224#issuecomment-2962302284):

>The recommended way of dealing with such workloads in 0.12 is:
>1. configure waitForPodsReady to trigger deactivation of the workload
>2. configure object retention policy for deactived workloads to delete them after this issue is done: https://github.com/kubernetes-sigs/kueue/issues/4471, see more details with example in [Setup garbage-collection of workload](https://kueue.sigs.k8s.io/docs/tasks/manage/setup_object_retention_policy/#example)
>
>Posting the example config here:
>```yaml
>  objectRetentionPolicies:
>    workloads:
>      afterFinished: "1m"
>      afterDeactivatedByKueue: "1m"
>  waitForPodsReady:
>    enable: true
>    timeout: 2m
>    recoveryTimeout: 1m
>    blockAdmission: true
>    requeuingStrategy:
>      backoffLimitCount: 0
>```
>
>/close
>As I believe the issue is solved. Feel free to re-open, or open follow up issue if there are still some gaps.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
