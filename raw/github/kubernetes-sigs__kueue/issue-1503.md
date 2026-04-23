# Issue #1503: Support Kubeflow Jobs type for resource quota reclaim

**Summary**: Support Kubeflow Jobs type for resource quota reclaim

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1503

**Last updated**: 2023-12-29T08:29:21Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@panpan0000](https://github.com/panpan0000)
- **Created**: 2023-12-21T08:57:16Z
- **Updated**: 2023-12-29T08:29:21Z
- **Closed**: 2023-12-27T13:27:53Z
- **Labels**: `kind/support`
- **Assignees**: _none_
- **Comments**: 10

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

reclaim the resource quota when kubeflow jobs(PytorchJob, TFJobs...etc) completed.
so far, when the Job CRD existing while the pod completed, the queue's flavorUsage will still be occupied , and stop incoming pods/jobs . 

```
#(1) show queue usage before job running 
kubectl  get localqueue -o yaml
    flavorUsage:
    - name: default-flavor
      resources:
      - name: cpu
        total: "1"
      - name: memory
        total: 2Gi
      - name: nvidia.com/gpu
        total: "1"

#(2) run a Pytorchjob with 3 pods which sleep for 1s, requesting 4c-2g-1GPU for each.
 kubectl  get po  -w
NAME                 READY   STATUS      RESTARTS   AGE
job-sleep-master-0   0/1     Completed   0          14s
job-sleep-worker-0   0/1     Completed   0          16s
job-sleep-worker-1   0/1     Completed   0          15s

 kubectl  get pytorchjob
NAME        STATE       AGE
job-sleep   Succeeded   4m32s


#(3)show queue usage again after job completed 
kubectl  get localqueue -o yaml
    flavorUsage:
    - name: default-flavor
      resources:
      - name: cpu
        total: "13"
      - name: memory
        total: 8Gi
      - name: nvidia.com/gpu
        total: "4"

```


**Why is this needed**:

it makes no sense to kill the xxjob right after finish, we still need the Pytorchjob CRD for some reason.
but kueue should reclaim the resource to reduce the `flavorUsage` after job completed.

relevant issue : https://github.com/kubernetes-sigs/kueue/issues/1149




**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [ ] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-12-21T09:29:36Z

cc @kerthcet  @B1F030

### Comment by [@anishasthana](https://github.com/anishasthana) — 2023-12-21T14:39:40Z

@panpan0000 Do you have a sample job CR I could use for testing? I'd be happy to take a stab at this.

### Comment by [@panpan0000](https://github.com/panpan0000) — 2023-12-22T02:11:17Z

it's very easy to reproduce the issue but requires training-operator from kubeflow instsalled:
```
apiVersion: kubeflow.org/v1
kind: PyTorchJob
metadata:
  annotations:
  labels:
    kueue.x-k8s.io/queue-name: $YOUR_LOCAL_QUEUE_NAME_HERE
  name: echo-job
  namespace: default
spec:
  pytorchReplicaSpecs:
    Worker:
      replicas: 3
      template:
        metadata: {}
        spec:
          containers:
          - command: ["sleep", "1"]
            image: python:3.12.0
            name: pytorch
            resources:
              limits:
                cpu: "1"
                memory: 1Gi
                nvidia.com/gpu: 1
              requests:
                cpu: "1"
                memory: 1Gi
                nvidia.com/gpu: 1
  runPolicy:
    suspend: false
```

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-12-22T05:09:49Z

@panpan0000 I could not reproduce this issue. How to install kueue and training-operator? Also, which versions do you use kueue, training-operator, and kubernetes?

### Comment by [@panpan0000](https://github.com/panpan0000) — 2023-12-27T08:53:34Z

kueue 0.5.1
training-operator: v1.7.0
k8s: v1.27.5

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-12-27T09:01:03Z

> kueue 0.5.1 training-operator: v1.7.0 k8s: v1.27.5

Also, how did you install those components? Could you provide reproducing steps?

### Comment by [@panpan0000](https://github.com/panpan0000) — 2023-12-27T13:27:53Z

It's wired ... I just tried again the issue gone ...
maybe I was using kueue 0.5.0 at that time...
sorry for the confusion. I will reopen if the issue happen again.....

sorry again @tenzen-y

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-12-27T14:04:48Z

> It's wired ... I just tried again the issue gone ... maybe I was using kueue 0.5.0 at that time... sorry for the confusion. I will reopen if the issue happen again.....
> 
> sorry again @tenzen-y

No problem :)

/remove-kind feature
/kind support

### Comment by [@B1F030](https://github.com/B1F030) — 2023-12-29T08:27:41Z

I tried in kubernetes `v1.27.3`
To install kubeflow:
`kubectl apply -k "github.com/kubeflow/training-operator/manifests/overlays/standalone"`
Under both kueue `v0.5.0` and `v0.5.1`, I fail to reproduce it, the resource quota reclaim works well.
Maybe this situation is caused by other configuration, so I'm going to just record this process here.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-12-29T08:29:20Z

> I tried in kubernetes `v1.27.3` To install kubeflow: `kubectl apply -k "github.com/kubeflow/training-operator/manifests/overlays/standalone"` Under both kueue `v0.5.0` and `v0.5.1`, I fail to reproduce it, the resource quota reclaim works well. Maybe this situation is caused by other configuration, so I'm going to just record this process here.

It's a great recording :) Thanks.
