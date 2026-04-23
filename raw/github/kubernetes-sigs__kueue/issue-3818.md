# Issue #3818: Unexpectedly High Memory Usage during idle state

**Summary**: Unexpectedly High Memory Usage during idle state

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3818

**Last updated**: 2024-12-14T13:00:30Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kalki7](https://github.com/kalki7)
- **Created**: 2024-12-12T02:32:03Z
- **Updated**: 2024-12-14T13:00:30Z
- **Closed**: 2024-12-13T15:54:27Z
- **Labels**: `kind/bug`
- **Assignees**: [@mimowo](https://github.com/mimowo)
- **Comments**: 28

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**: Firstly, I raised the resource limit to 16gb for the kueue-controller-manager and had submitted over 90,000 jobs to the kueue when I'd noticed the kueue-controller-manager memory usage jump to ~10gb. After all the jobs have been completed, I still notice that the kueue-controller-manager is using ~5gb memory. This is the memory usage during an idle state after all the jobs have completed.

`kubectl top pod -n kueue-system`
<img width="491" alt="image" src="https://github.com/user-attachments/assets/9c1ad16e-3ef8-4589-a51b-a3ed876dc985" />


**What you expected to happen**: I was expecting the memory usage to drop down to ~500mb since that was the original limit for the kueue-controller-manager.

**How to reproduce it (as minimally and precisely as possible)**: Submit a large number of jobs, which each job taking a considerable amount if time (average job execution time : 5m). Submit a whole lot of them, and monitor the memory usage.

**Anything else we need to know?**:

**Environment**:
- Kubernetes version: 1.30.5-gke.1443001
- Kueue version: v0.9.1
- Cloud provider or hardware configuration: GCP - Google Kubernetes Engine
- OS (e.g: `cat /etc/os-release`): linux/amd64
- GoVersion: go1.22.6 X:boringcrypto
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-12T06:03:32Z

> After all the jobs have been completed, I still notice that the kueue-controller-manager is using ~5gb memory.

Are the Jobs & corresponding workloads deleted? I guess if they are completed, but still exist they are present in the caches of controller-runtime. Does the usage go down if you delete the Jobs & workloads?

### Comment by [@kalki7](https://github.com/kalki7) — 2024-12-12T08:17:41Z

The Jobs and their workloads have a TTL and I double checked to ensure they're all deleted. It's only post the deletion that I noticed the memory usage still high. The usage hasn't gone down even though the jobs have been deleted. 

Is there any way to clear the caches of the kueue-contoller-manager?

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-12T08:21:19Z

> The Jobs and their workloads have a TTL and I double checked to ensure they're all deleted. It's only post the deletion that I noticed the memory usage still high. 

I see, this is worrying in that case. cc @mwysokin 

> Is there any way to clear the caches of the kueue-contoller-manager?

I don't think so there is anything other than: `kubectl rollout restart deploy/kueue-controller-manager -nkueue-system` for now. 

I think this needs investigation to determine what actually keeps the memory.

### Comment by [@kalki7](https://github.com/kalki7) — 2024-12-12T08:22:59Z

When I restart the deployment, yes it does clear out cache. I've verified this. But is there any way for me to assist you folks with this investigation ? Do let me know !

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-12T08:31:16Z

Good question, since the memory leaks even after Jobs deletion I suspect this is not informer cache in controller-runtime, but internal Kueue cache. 

I think we could try to repro this with integration tests and see the state of the cache with debugger. 

In the meanwhile - can you try to use this https://github.com/kubernetes-sigs/kueue/blob/main/hack/dump_cache.sh script, after some Jobs are deleted - to see if something is left in the cache after them?

### Comment by [@kalki7](https://github.com/kalki7) — 2024-12-12T08:57:35Z

`{"level":"error","ts":"2024-12-12T08:50:51.116824557Z","caller":"controller/controller.go:316","msg":"Reconciler error","controller":"clusterqueue","controllerGroup":"kueue.x-k8s.io","controllerKind":"ClusterQueue","ClusterQueue":{"name":"cluster-queue"},"namespace":"","name":"cluster-queue","reconcileID":"9a925db0-0aef-46be-9921-4bc80ecb03cd","error":"Operation cannot be fulfilled on clusterqueues.kueue.x-k8s.io \"cluster-queue\": the object has been modified; please apply your changes to the latest version and try again","stacktrace":"sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).reconcileHandler\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:316\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).processNextWorkItem\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:263\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).Start.func2.2\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:224"}`


Here's something I noticed, could this be a cause ?
For reference, I've added my cluster queue definition as well. Is there something I need to specifically be looking for.

```apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: cluster-queue
spec:
  namespaceSelector: {} 
  queueingStrategy: BestEffortFIFO
  resourceGroups:
  - coveredResources: ["cpu","memory","pods"]
    flavors:
    - name: "train-flavour"
      resources:
      - name: "cpu"
        nominalQuota: 2250
      - name: "memory"
        nominalQuota: 4500G
      - name: "pods"
        nominalQuota: 2100
    - name: "bulk-flavour"
      resources:
      - name: "cpu"
        nominalQuota: 1400
      - name: "memory"
        nominalQuota: 11200G
      - name: "pods"
        nominalQuota: 1200
    - name: "demand-flavour"
      resources:
      - name: "cpu"
        nominalQuota: 1400
      - name: "memory"
        nominalQuota: 11200G
      - name: "pods"
        nominalQuota: 1200 
```

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-12T09:09:13Z

> Here's something I noticed, could this be a cause ?

Possibly, but not directly. This error basically means that the update operation is rejected by the kube API server, because the ResourceVersion sent by the client (Kueue in this case is old). This can happen for example if two controllers (like Kueue and Job controller) send requests to modify the same object. In rare scenarios it may also happen for two competing controllers within Kueue, or even in case of one controller, if the informer caches take long to update. 
However, ideally, such a failure should be retry on the next Reconcile invocation, so should it is not necessarily a problem on its own.

Thanks, for the cluster details, I will try to also repro on my end. In the meanwhile, the results of the cache dump script could be very telling.

### Comment by [@kalki7](https://github.com/kalki7) — 2024-12-12T09:26:11Z

@mimowo This is the following issue I'm faced with while trying to run that script

`http: TLS handshake error from <ip>:45632: EOF`

Apart from that it's just dumping the usual logs. However, when I triggered a small number of jobs into the queue this was the memory pattern.

<img width="491" alt="image" src="https://github.com/user-attachments/assets/06a5bc42-72cc-4d60-9b38-573eefa68268" />

It looks like the memory cleared out for the small number of jobs (~2k) right after the jobs were deleted.

<img width="491" alt="image" src="https://github.com/user-attachments/assets/f2881fc2-5690-4838-a97f-c16f0b647b24" />

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-12T09:45:08Z

This complicates the picture since the memory returned cleans up for the small number of jobs. Do you use Kueue with a single replica or multiple replicas?

### Comment by [@kalki7](https://github.com/kalki7) — 2024-12-12T10:36:00Z

Kueue with a single replica, never tried multiple

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-13T07:37:31Z

/assign 
I will investigate this deeper today

### Comment by [@kalki7](https://github.com/kalki7) — 2024-12-13T09:26:21Z

Tried the cache dump again, but got hit with 
 `Targeting container "manager". If you don't see processes from this container it may be because the container runtime doesn't support this feature.`
 
 Nevertheless adding another observation here, after running the exact same batch of ~30k jobs, twice 

<img width="1045" alt="image" src="https://github.com/user-attachments/assets/96caca44-378d-4165-bbde-eab317a376fa" />

The memory in cache after the first time, was **1.92gb**, but after the second run, it was only **3.02gb**. If it were retaining the same set of objects, I would assume that the cache retention should've doubled, but did not. I'm not sure what to make of this, but I hope it would be of some help

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-13T09:37:45Z

@kalki7 can you run the experiment for comparison with 0.8.4 - I suspect we have a regression in 0.9

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-13T11:52:07Z

I have a repro locally: create 100 big jobs, then delete them all
![image](https://github.com/user-attachments/assets/31c8e3b5-588e-4b92-8a62-7c5407d4d136)
I think at this point I'm good to continue, I feel you can skip testing on 0.8 - I will do it next.

EDIT: on 0.8.4 there is no visible leak by the experiment:

![image](https://github.com/user-attachments/assets/36190b7e-b413-4b45-ba86-00252fdaf815)

### Comment by [@mwysokin](https://github.com/mwysokin) — 2024-12-13T12:03:22Z

How did it work in older versions? I don't think we should be jumping into conclusions without comparing it with past data points. 

Also these items are so small that I'm not sure that we should expect OS and go to always free literally all the memory. Sometimes it leaves some allocatable memory since it saw in the past jumps in memory consumption. 

Another worth to run test would be running this test in a loop for 50-100 times and seeing if there's a trend like additional memory keeps growing or whether after a certain point it stabilizes (the former would point to a memory leek and the latter would suggest my theory about OS leaving some allocatable memory just in case).

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-13T12:16:38Z

Yeah, I did a couple of more repeats on 0.9.1 before posting and all of them demonstrated the same pattern - it was not going down to previous range, but staying 2x more.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-13T12:42:31Z

Ok, I think most of the leak  (maybe all) is due to graduating MultiKueue. I disabled `--feature-gates=MultiKueue=false` and getting much better results:
![image](https://github.com/user-attachments/assets/c6de6d53-1ad1-4640-a00d-4feffd0087d6)
This is one screen, but I confirm the pattern twice.
It is not returning quite back to the startup level, but I think it might be the effect of warming some low-level caches.

I suspect this is the issue: https://github.com/kubernetes-sigs/kueue/blob/cc65f7e7701df31e77959ef664384616abd54f9e/pkg/controller/admissionchecks/multikueue/workload.go#L60

### Comment by [@kalki7](https://github.com/kalki7) — 2024-12-13T13:10:30Z

@mimowo your suspicions are **true**, on v0.8.4 it's cleared out memory entirely. The issue seems to be with 0.9.1 (or 0.9)

### Comment by [@kalki7](https://github.com/kalki7) — 2024-12-13T13:32:10Z

While we're on the topic, I just wanted to understand since (or if you could point me in the general direction to find out) if and how kueue uses the etcd cluster memory for queueing workloads.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-13T13:41:26Z

Sure, the entry point for scheduling is [here](https://github.com/kubernetes-sigs/kueue/blob/cc65f7e7701df31e77959ef664384616abd54f9e/pkg/scheduler/scheduler.go#L184) where we take the  heads of workloads. Underneath the workloads are kept in-memory using [heaps](https://github.com/kubernetes-sigs/kueue/blob/cc65f7e7701df31e77959ef664384616abd54f9e/pkg/queue/cluster_queue.go#L56) per CQ.
We also use a snapshot of the queues for visibility on-demand endpoint: https://kueue.sigs.k8s.io/docs/tasks/manage/monitor_pending_workloads/pending_workloads_on_demand/. The good starting point for taking the snapshot is [here](https://github.com/kubernetes-sigs/kueue/blob/cc65f7e7701df31e77959ef664384616abd54f9e/pkg/visibility/api/v1beta1/pending_workloads_cq.go#L62-L92).

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-13T13:51:17Z

after a code change (I will push soon) on main:
![image](https://github.com/user-attachments/assets/117cba1b-883a-4849-8c54-06927e2dce24)

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-13T13:57:29Z

@kalki7 would you be able to test the code change independently on your system before we merge https://github.com/kubernetes-sigs/kueue/pull/3835? I don't think it is a blocker to merge, but would be great to get the independent confirmation.

### Comment by [@PBundyra](https://github.com/PBundyra) — 2024-12-13T15:43:48Z

Thanks for collaborating @kalki7

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-13T15:53:33Z

Yes, thank you @kalki7 for raising the issue and repeated tests on your side. I also confirmed the issue with debugger and extra logging, it was very real. We aim to release 0.9.2 along with 0.10.0 on Monday.

### Comment by [@kalki7](https://github.com/kalki7) — 2024-12-13T21:07:11Z

@mimowo  I'd be more than happy to test it out, although I will need some help on understanding how to do so. And thank you for the prompt responses and fix as well !! 

Do let me know however I can help !

### Comment by [@mwysokin](https://github.com/mwysokin) — 2024-12-13T23:18:57Z

@kalki7 The easiest way would be to install Kueue from the tip of the main branch: https://kueue.sigs.k8s.io/docs/installation/#install-the-latest-development-version

### Comment by [@kalki7](https://github.com/kalki7) — 2024-12-14T12:34:29Z

@mwysokin @mwysokin 

Using **kueue:main** as on 12th Dec, 2024 12:30pm UTC, along with increased resource limits for kueue-controller. For the same set of jobs (~30k) as previously mentioned on this ticket. 

I can confirm that there is no memory leak and that CPU utilisation is a lot more optimised.

<img width="1045" alt="image" src="https://github.com/user-attachments/assets/c47022dd-e5ed-4666-8c05-4ed5e3918e3c" />

This looks great !

### Comment by [@kalki7](https://github.com/kalki7) — 2024-12-14T12:43:47Z

I think that we can get rid of https://github.com/kubernetes-sigs/kueue/issues/1618 since this seems to fix what's mentioned over there as well ! 

And out of curiosity is there a way to avoid using cluster memory and keep the workload only on kueue memory until the workload has been accepted. Since, the sheer scale at which I'm going to run the next experiment might bring down the manage GKE Cluster whose etcd memory is limited to 6gb.
