# Issue #1476: pytorchjobs scheduling unaware of node resource topology

**Summary**: pytorchjobs scheduling unaware of node resource topology

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1476

**Last updated**: 2024-06-30T14:19:01Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@kchopra456](https://github.com/kchopra456)
- **Created**: 2023-12-16T13:08:12Z
- **Updated**: 2024-06-30T14:19:01Z
- **Closed**: 2024-06-30T14:18:34Z
- **Labels**: `kind/support`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 13

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
- Kueue when handling distributed jobs, such as pytorchjob makes node-unaware admission decisions for dedicated resource such as GPUs.
- Even though the requested resource count may be available in aggregation, that does not translate to actual cluster physical resource availability, explained under.
  - 3 nodes with 8 GPU each, translates to 24 GPUs, all managed under kueue; initial cluster configuration is `8,8,8 GPUs`.
  - Admit 2 jobs, 1 GPU each, scheduled on 2 nodes; cluster configuration `7,7,8 GPUs`.
  - Submit a pytorchjob with 1 master and 1 worker, each requesting 8 GPU each, total requested GPUs 16.
  - Kueue allows this workload to be scheduled even though actual physical node topology would not schedule the job immediatedly and both the pods will sit in default k8s queue pending, waitiing for 1 more node to open (_partial admission not allowed_).

**What you expected to happen**:
- pytorchjob to remain suspended until 2 nodes i.e. 16 GPUs (8,8,X cluster configuration) is possible.
- A new job requesting a 8 GPU job should be able to schedule but with current implementation it waits suspended.

**How to reproduce it (as minimally and precisely as possible)**:
1. Create kueue resources
```yaml
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: ResourceFlavor
metadata:
  name: test-node
spec:
  nodeLabels:
    hpc/kueue-test: 'true' 

---
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: test-cq
spec:
  cohort: no-cohort
  namespaceSelector: {}
  resourceGroups:
    - coveredResources:
        - nvidia.com/gpu
      flavors:
        - name: test-node
          resources:
            - name: nvidia.com/gpu
              nominalQuota: '24'
              borrowingLimit: '0'

---
apiVersion: kueue.x-k8s.io/v1beta1
kind: LocalQueue
metadata:
  name: test-default
spec:
  clusterQueue: test-cq
```
2. Create jobs in the following sequence
   1. 1-GPU job (force it to node-001)
   2. 1-GPU job (force it to node-002)
   3. 16-GPU pytorchjob
   4. 8-GPU job
3. Use the template to create jobs and pytorchjob
`job.yaml`
```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: job-001
  labels:
    kueue.x-k8s.io/queue-name: test-default
spec:
  template:
     spec:
      nodeName: node-00X
      containers:
        - name: main
          image: nginx:latest
          command:
            - sleep
            - '600'
          resources:
            limits:
              nvidia.com/gpu: "1"
          imagePullPolicy: IfNotPresent
      restartPolicy: Never
  suspend: true
```
`pytorchjob.yaml`
```yaml
apiVersion: kubeflow.org/v1
kind: PyTorchJob
metadata:
  name: pytorch-cq-001
  labels:
    kueue.x-k8s.io/queue-name: test-default
spec:
  pytorchReplicaSpecs:
    Master:
      replicas: 1
      restartPolicy: Never
      template:
        spec:
          containers:
            - name: pytorch
              image: nginx:latest
              imagePullPolicy: IfNotPresent
              command:
                - sleep
                - '600'
              resources:
                limits:
                  nvidia.com/gpu: "8"
    Worker:
      replicas: 1
      restartPolicy: OnFailure
      template:
        spec:
          containers:
            - name: pytorch
              image: nginx:latest
              imagePullPolicy: IfNotPresent
              command:
                - sleep
                - '600'
              resources:
                limits:
                  nvidia.com/gpu: "8"
```

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`):
  - cluster: v1.23
  - kubectl : v1.25
- Kueue version (use `git describe --tags --dirty --always`):
  - v0.5.0
- Cloud provider or hardware configuration:
  - Nvidia GPU
- OS (e.g: `cat /etc/os-release`):
  - Ubuntu 20.04
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-12-26T11:49:22Z

@kchopra456 The kueue doesn't consider actual available node resources.
As an alternative, I think that you can use the `sequential_admission` feature.
In the `sequential_admission` feature, if the unsuspended workload like PyTorchJob isn't ready in spite of timeout exceeding, the workload will be evicted and re-queued.

https://kueue.sigs.k8s.io/docs/tasks/setup_sequential_admission/

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-12-26T11:49:34Z

/remove-kind bug
/kind support

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-03-25T12:01:54Z

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

### Comment by [@AllenXu93](https://github.com/AllenXu93) — 2024-04-24T07:05:38Z

> @kchopra456 The kueue doesn't consider actual available node resources. As an alternative, I think that you can use the `sequential_admission` feature. In the `sequential_admission` feature, if the unsuspended workload like PyTorchJob isn't ready in spite of timeout exceeding, the workload will be evicted and re-queued.
> 
> https://kueue.sigs.k8s.io/docs/tasks/setup_sequential_admission/

After job requeue, will it still pop by queue and still admit then hang in next schedule epoch?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-04-24T07:28:35Z

> > @kchopra456 The kueue doesn't consider actual available node resources. As an alternative, I think that you can use the `sequential_admission` feature. In the `sequential_admission` feature, if the unsuspended workload like PyTorchJob isn't ready in spite of timeout exceeding, the workload will be evicted and re-queued.
> > https://kueue.sigs.k8s.io/docs/tasks/setup_sequential_admission/
> 
> After job requeue, will it still pop by queue and still admit then hang in next schedule epoch?

Yes, it could happen again. But, we have a backoff and configurable limit re-queuing mechanism so that we could avoid the endless re-queueing.

### Comment by [@AllenXu93](https://github.com/AllenXu93) — 2024-04-24T08:16:14Z

> > > @kchopra456 The kueue doesn't consider actual available node resources. As an alternative, I think that you can use the `sequential_admission` feature. In the `sequential_admission` feature, if the unsuspended workload like PyTorchJob isn't ready in spite of timeout exceeding, the workload will be evicted and re-queued.
> > > https://kueue.sigs.k8s.io/docs/tasks/setup_sequential_admission/
> > 
> > 
> > After job requeue, will it still pop by queue and still admit then hang in next schedule epoch?
> 
> Yes, it could happen again. But, we have a backoff and configurable limit re-queuing mechanism so that we could avoid the endless re-queueing.

Got it, thanks for your reply.
Is there any plan to make kueue work better with schedule?
For example,  kueue can do schedule simulation in admission check after admited, even before admited (because it maybe chose different resourceflavor by simulation result)
And when schedule preempt some job or pod, kueue have some way to aware the pod status change.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-04-24T08:19:40Z

> > > > @kchopra456 The kueue doesn't consider actual available node resources. As an alternative, I think that you can use the `sequential_admission` feature. In the `sequential_admission` feature, if the unsuspended workload like PyTorchJob isn't ready in spite of timeout exceeding, the workload will be evicted and re-queued.
> > > > https://kueue.sigs.k8s.io/docs/tasks/setup_sequential_admission/
> > > 
> > > 
> > > After job requeue, will it still pop by queue and still admit then hang in next schedule epoch?
> > 
> > 
> > Yes, it could happen again. But, we have a backoff and configurable limit re-queuing mechanism so that we could avoid the endless re-queueing.
> 
> Got it, thanks for your reply. Is there any plan to make kueue work better with schedule? For example, kueue can do schedule simulation in admission check after admited, even before admited (because it maybe chose different resourceflavor by simulation result) And when schedule preempt some job or pod, kueue have some way to aware the pod status change.

We have no plan since pod scheduling is out of the scope of kueue, as we described in https://kueue.sigs.k8s.io/docs/overview/#why-use-kueue.

### Comment by [@AllenXu93](https://github.com/AllenXu93) — 2024-04-24T08:38:40Z

> > > > > @kchopra456 The kueue doesn't consider actual available node resources. As an alternative, I think that you can use the `sequential_admission` feature. In the `sequential_admission` feature, if the unsuspended workload like PyTorchJob isn't ready in spite of timeout exceeding, the workload will be evicted and re-queued.
> > > > > https://kueue.sigs.k8s.io/docs/tasks/setup_sequential_admission/
> > > > 
> > > > 
> > > > After job requeue, will it still pop by queue and still admit then hang in next schedule epoch?
> > > 
> > > 
> > > Yes, it could happen again. But, we have a backoff and configurable limit re-queuing mechanism so that we could avoid the endless re-queueing.
> > 
> > 
> > Got it, thanks for your reply. Is there any plan to make kueue work better with schedule? For example, kueue can do schedule simulation in admission check after admited, even before admited (because it maybe chose different resourceflavor by simulation result) And when schedule preempt some job or pod, kueue have some way to aware the pod status change.
> 
> We have no plan since pod scheduling is out of the scope of kueue, as we described in https://kueue.sigs.k8s.io/docs/overview/#why-use-kueue.

Maybe I don't have expressed clearly.
It don't mean that kueue to aware schedule or other module,  I think kueue can have a way to let other module work well with kueue. 
When kueue chose resourceflavor,  other module(like schedule ) can help kueue to choose a better resourceflavor that meet schedule need or descide whether or not admit,  when some thing happen to admitted workload(like pod was preempted), other module can tell kueue to recalculate/update queue's usage.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-05-01T13:00:09Z

> When kueue chose resourceflavor, other module(like schedule ) can help kueue to choose a better resourceflavor that meet schedule need or descide whether or not admit, when some thing happen to admitted workload(like pod was preempted), other module can tell kueue to recalculate/update queue's usage.

As my understanding, that is Pod's pending status. The kube-scheduler evaluates the Pod if the Pod fits any Nodes during the scheduling cycle, and then if there are not any fit Node, the kube-scheduler keeps using the Pending status in Pod.

After that, the Kueue detects the Pending status and re-queues Pod.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-05-31T13:52:13Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-06-30T14:18:30Z

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

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-06-30T14:18:35Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1476#issuecomment-2198578356):

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

### Comment by [@AllenXu93](https://github.com/AllenXu93) — 2024-06-30T14:19:00Z

您好，邮件已收到，我会尽快给您回复。
