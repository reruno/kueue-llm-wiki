# Issue #2691: JobSet fails to suspend if nodeSelectors are added on admission

**Summary**: JobSet fails to suspend if nodeSelectors are added on admission

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2691

**Last updated**: 2024-10-24T06:52:03Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-07-25T08:14:03Z
- **Updated**: 2024-10-24T06:52:03Z
- **Closed**: 2024-10-24T06:52:01Z
- **Labels**: `kind/bug`
- **Assignees**: [@mimowo](https://github.com/mimowo)
- **Comments**: 12

## Description

**What happened**:

JobSet fails to suspend if there are nodeSelectors added on admission. It fails because JobSet webhook rejects the update.

**What you expected to happen**:

JobSet can be suspended and the PodTemplate is restored.

**How to reproduce it (as minimally and precisely as possible)**:

0. Create a kind cluster and install Kueue 0.8.0 and JobSet 0.5.2
1. Configure Kueue using the following (node the nodeLabels for the flavor)

```
apiVersion: kueue.x-k8s.io/v1beta1
kind: ResourceFlavor
metadata:
  name: "worker-flavor"
spec:
  nodeLabels:
    "kubernetes.io/hostname": "kind-worker"
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: "cluster-queue"
spec:
  namespaceSelector: {} # match all.
  resourceGroups:
  - coveredResources: ["cpu", "memory"]
    flavors:
    - name: "worker-flavor"
      resources:
      - name: "cpu"
        nominalQuota: 9
      - name: "memory"
        nominalQuota: 36Gi
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: LocalQueue
metadata:
  namespace: "default"
  name: "user-queue"
spec:
  clusterQueue: "cluster-queue"
```
2. Create a JobSet that will get admitted to the queue:
```
apiVersion: jobset.x-k8s.io/v1alpha2
kind: JobSet
metadata:
  name: sleep
  labels:
    kueue.x-k8s.io/queue-name: user-queue
spec:
  suspend: true
  replicatedJobs:
  - name: workers
    template:
      spec:
        parallelism: 4
        completions: 4
        backoffLimit: 0
        template:
          spec:
            containers:
            - name: sleep
              image: busybox
              command:
                - sleep
              args:
                - 600s
              resources:
                requests:
                  memory: 100Mi
                  cpu: 100m
  - name: driver
    template:
      spec:
        parallelism: 1
        completions: 1
        backoffLimit: 0
        template:
          spec:
            containers:
            - name: sleep
              image: busybox
              command:
                - sleep
              args:
                - 600s
              resources:
                requests:
                  memory: 100Mi
                  cpu: 100m
```
3. Stop the Cluster queue `k edit clusterqueue/cluster-queue` and set the `stopPolicy: HoldAndDrain`

Issue: This should result in stopping the JobSet. However, it continues to run and be admitted. The logs for Kueue show that the mutation request is rejected by JobSet webhook.

The issue is reproduced by the e2e test in the WIP PR: https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/2700/pull-kueue-test-e2e-main-1-29/1816503837968568320

**Anything else we need to know?**:

I fill open a dedicated issue in JobSet and see if we can fix it there. We may need a work-around in Kueue to do 2-step stop:
suspend first, then restore the PodTemplate, but I prefer to avoid it. This is something we aim to avoid for Job in the long run too: https://github.com/kubernetes/kubernetes/issues/113221

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-07-25T08:14:14Z

/assign
/cc @tenzen-y

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-07-25T11:05:25Z

I think that this is a little big deal for the GPU workload since some users inject the tolerations for the GPU Node via resourceFlavor.

By this limitation, we can not preempt or deactivate the Jobs with tolerations inserted by the ResourceFlavor, right?
If so, https://github.com/kubernetes/kubernetes/issues/113221 is a higher priority for the Kueue.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-07-25T11:20:48Z

> By this limitation, we can not preempt or deactivate the Jobs with tolerations inserted by the ResourceFlavor, right?
If so, https://github.com/kubernetes/kubernetes/issues/113221 is a higher priority for the Kueue.

To workaround this problem we have implemented a custom stop in Kueue, which takes 3 requests to stop:
1. suspend
2. set startTime to nil
3. restore PodTemplate

So, while it is not very performant it works. So it is a high priority, but I would not call it urgent. We could follow a similar pattern for JobSet (one request to suspend, and one to restore PodTemplate), but I hope we can fix it in JobSet itself.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-07-25T11:22:48Z

I think it didn't surface until now because JobSet is mostly used with DWS ProvisioningRequests, where the quota is set very high, so evictions are rare.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-07-25T11:31:13Z

> > By this limitation, we can not preempt or deactivate the Jobs with tolerations inserted by the ResourceFlavor, right?
> > If so, [kubernetes/kubernetes#113221](https://github.com/kubernetes/kubernetes/issues/113221) is a higher priority for the Kueue.
> 
> To workaround this problem we have implemented a custom stop in Kueue, which takes 3 requests to stop:
> 
> 1. suspend
> 2. set startTime to nil
> 3. restore PodTemplate
> 
> So, while it is not very performant it works. So it is a high priority, but I would not call it urgent. We could follow a similar pattern for JobSet (one request to suspend, and one to restore PodTemplate), but I hope we can fix it in JobSet itself.

Yeah, that is the reason why we introduced the `JobWithCustomStop` interface...

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-07-25T11:35:38Z

> So, while it is not very performant it works. So it is a high priority, but I would not call it urgent. We could follow a similar pattern for JobSet (one request to suspend, and one to restore PodTemplate), but I hope we can fix it in JobSet itself.

One thing is preemption or deactivation throughput, this 3 step stop mechanism obviously would bring us lower throughput preemption.
I guess that this may be a little bit of a deal in the big cluster. But, I'm not sure if this could be one of the use cases of https://github.com/kubernetes/kubernetes/issues/113221.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-07-25T11:41:27Z

IIUC https://github.com/kubernetes/kubernetes/issues/113221 is about it - to give us an "official" API to do what we do in Kueue. The fact that Kueue sets `status.startTime=nil` is hacky - external controllers should not mutate Status of objects managed by another controller, in principle. 

I think the idea "We could implement mutable scheduling directives after suspension if we set .status.startTime to nil when when we are confident that there all the running pods are at least terminating. " is that `.status.startTime` is set to nil by the k8s Job controller, not an external controller.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-07-25T11:50:31Z

> IIUC [kubernetes/kubernetes#113221](https://github.com/kubernetes/kubernetes/issues/113221) is about it - to give us an "official" API to do what we do in Kueue. The fact that Kueue sets `status.startTime=nil` is hacky - external controllers should not mutate Status of objects managed by another controller, in principle.
> 
> I think the idea "We could implement mutable scheduling directives after suspension if we set .status.startTime to nil when when we are confident that there all the running pods are at least terminating. " is that `.status.startTime` is set to nil by the k8s Job controller, not an external controller.

I agree with you. Additionally, nice to have verifications if the `.status.active` and `.status.terminating` are 0.
Anyway, if we can discuss this in the sig-apps or wg-batch meeting for the next kubernetes release iteration, it sounds attractive.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-10-23T16:55:47Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-10-23T20:24:23Z

/remove-lifecycle stale

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-24T06:51:57Z

I think this is already addressed by the fix in JobSet: https://github.com/kubernetes-sigs/jobset/pull/644, followed up by the merge of e2e test in Kueue: https://github.com/kubernetes-sigs/kueue/pull/2700 (the e2e test covers to the scenario in the issue). 
/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-10-24T06:52:02Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/2691#issuecomment-2434443801):

>I think this is already addressed by the fix in JobSet: https://github.com/kubernetes-sigs/jobset/pull/644, followed up by the merge of e2e test in Kueue: https://github.com/kubernetes-sigs/kueue/pull/2700 (the e2e test covers to the scenario in the issue). 
>/close 


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
