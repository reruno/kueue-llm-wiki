# Issue #4733: Flaky Test: End To End Suite: Pod groups when Single CQ should allow to preempt the lower priority group

**Summary**: Flaky Test: End To End Suite: Pod groups when Single CQ should allow to preempt the lower priority group

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4733

**Last updated**: 2025-03-24T15:24:34Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-03-21T05:59:30Z
- **Updated**: 2025-03-24T15:24:34Z
- **Closed**: 2025-03-24T15:24:34Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 13

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

Flaky E2E Test Case, `End To End Suite: kindest/node:v1.32.3: [It] Pod groups when Single CQ should allow to preempt the lower priority group` in unrelated branch.

```shell
{Timed out after 45.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/pod_test.go:484 with:
v1.PodStatus{Phase:"Succeeded", Conditions:[]v1.PodCondition{v1.PodCondition{Type:"TerminationTarget", Status:"True", LastProbeTime:time.Date(1, time.January, 1, 0, 0, 0, 0, time.UTC), LastTransitionTime:time.Date(2025, time.March, 21, 5, 54, 13, 0, time.Local), Reason:"WorkloadEvictedDueToPreempted", Message:"Preempted to accommodate a workload (UID: 9788b1f0-9a2c-4166-b205-926beddaacdd, JobUID: UNKNOWN) due to prioritization in the ClusterQueue"}, v1.PodCondition{Type:"PodReadyToStartContainers", Status:"False", LastProbeTime:time.Date(1, time.January, 1, 0, 0, 0, 0, time.UTC), LastTransitionTime:time.Date(2025, time.March, 21, 5, 54, 14, 0, time.Local), Reason:"", Message:""}, v1.PodCondition{Type:"Initialized", Status:"True", LastProbeTime:time.Date(1, time.January, 1, 0, 0, 0, 0, time.UTC), LastTransitionTime:time.Date(2025, time.March, 21, 5, 54, 12, 0, time.Local), Reason:"PodCompleted", Message:""}, v1.PodCondition{Type:"Ready", Status:"False", LastProbeTime:time.Date(1, time.January, 1, 0, 0, 0, 0, time.UTC), LastTransitionTime:time.Date(2025, time.March, 21, 5, 54, 14, 0, time.Local), Reason:"PodCompleted", Message:""}, v1.PodCondition{Type:"ContainersReady", Status:"False", LastProbeTime:time.Date(1, time.January, 1, 0, 0, 0, 0, time.UTC), LastTransitionTime:time.Date(2025, time.March, 21, 5, 54, 14, 0, time.Local), Reason:"PodCompleted", Message:""}, v1.PodCondition{Type:"PodScheduled", Status:"True", LastProbeTime:time.Date(1, time.January, 1, 0, 0, 0, 0, time.UTC), LastTransitionTime:time.Date(2025, time.March, 21, 5, 54, 12, 0, time.Local), Reason:"", Message:""}}, Message:"", Reason:"", NominatedNodeName:"", HostIP:"172.18.0.2", HostIPs:[]v1.HostIP{v1.HostIP{IP:"172.18.0.2"}}, PodIP:"10.244.1.142", PodIPs:[]v1.PodIP{v1.PodIP{IP:"10.244.1.142"}}, StartTime:time.Date(2025, time.March, 21, 5, 54, 12, 0, time.Local), InitContainerStatuses:[]v1.ContainerStatus(nil), ContainerStatuses:[]v1.ContainerStatus{v1.ContainerStatus{Name:"c", State:v1.ContainerState{Waiting:(*v1.ContainerStateWaiting)(nil), Running:(*v1.ContainerStateRunning)(nil), Terminated:(*v1.ContainerStateTerminated)(0xc00025f650)}, LastTerminationState:v1.ContainerState{Waiting:(*v1.ContainerStateWaiting)(nil), Running:(*v1.ContainerStateRunning)(nil), Terminated:(*v1.ContainerStateTerminated)(nil)}, Ready:false, RestartCount:0, Image:"registry.k8s.io/e2e-test-images/agnhost:2.53", ImageID:"registry.k8s.io/e2e-test-images/agnhost@sha256:99c6b4bb4a1e1df3f0b3752168c89358794d02258ebebc26bf21c29399011a85", ContainerID:"containerd://6270b0109a689462d230824991c0ef73f7aed792429144b12b2b4a1d6c70a421", Started:(*bool)(0xc000c0afd9), AllocatedResources:v1.ResourceList(nil), Resources:(*v1.ResourceRequirements)(nil), VolumeMounts:[]v1.VolumeMountStatus{v1.VolumeMountStatus{Name:"kube-api-access-8rmqj", MountPath:"/var/run/secrets/kubernetes.io/serviceaccount", ReadOnly:true, RecursiveReadOnly:(*v1.RecursiveReadOnlyMode)(0xc000c06860)}}, User:(*v1.ContainerUser)(nil), AllocatedResourcesStatus:[]v1.ResourceStatus(nil)}}, QOSClass:"Burstable", EphemeralContainerStatuses:[]v1.ContainerStatus(nil), Resize:"", ResourceClaimStatuses:[]v1.PodResourceClaimStatus(nil)}
Expected
    <v1.PodPhase>: Succeeded
to equal
    <v1.PodPhase>: Failed failed [FAILED] Timed out after 45.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/pod_test.go:484 with:
v1.PodStatus{Phase:"Succeeded", Conditions:[]v1.PodCondition{v1.PodCondition{Type:"TerminationTarget", Status:"True", LastProbeTime:time.Date(1, time.January, 1, 0, 0, 0, 0, time.UTC), LastTransitionTime:time.Date(2025, time.March, 21, 5, 54, 13, 0, time.Local), Reason:"WorkloadEvictedDueToPreempted", Message:"Preempted to accommodate a workload (UID: 9788b1f0-9a2c-4166-b205-926beddaacdd, JobUID: UNKNOWN) due to prioritization in the ClusterQueue"}, v1.PodCondition{Type:"PodReadyToStartContainers", Status:"False", LastProbeTime:time.Date(1, time.January, 1, 0, 0, 0, 0, time.UTC), LastTransitionTime:time.Date(2025, time.March, 21, 5, 54, 14, 0, time.Local), Reason:"", Message:""}, v1.PodCondition{Type:"Initialized", Status:"True", LastProbeTime:time.Date(1, time.January, 1, 0, 0, 0, 0, time.UTC), LastTransitionTime:time.Date(2025, time.March, 21, 5, 54, 12, 0, time.Local), Reason:"PodCompleted", Message:""}, v1.PodCondition{Type:"Ready", Status:"False", LastProbeTime:time.Date(1, time.January, 1, 0, 0, 0, 0, time.UTC), LastTransitionTime:time.Date(2025, time.March, 21, 5, 54, 14, 0, time.Local), Reason:"PodCompleted", Message:""}, v1.PodCondition{Type:"ContainersReady", Status:"False", LastProbeTime:time.Date(1, time.January, 1, 0, 0, 0, 0, time.UTC), LastTransitionTime:time.Date(2025, time.March, 21, 5, 54, 14, 0, time.Local), Reason:"PodCompleted", Message:""}, v1.PodCondition{Type:"PodScheduled", Status:"True", LastProbeTime:time.Date(1, time.January, 1, 0, 0, 0, 0, time.UTC), LastTransitionTime:time.Date(2025, time.March, 21, 5, 54, 12, 0, time.Local), Reason:"", Message:""}}, Message:"", Reason:"", NominatedNodeName:"", HostIP:"172.18.0.2", HostIPs:[]v1.HostIP{v1.HostIP{IP:"172.18.0.2"}}, PodIP:"10.244.1.142", PodIPs:[]v1.PodIP{v1.PodIP{IP:"10.244.1.142"}}, StartTime:time.Date(2025, time.March, 21, 5, 54, 12, 0, time.Local), InitContainerStatuses:[]v1.ContainerStatus(nil), ContainerStatuses:[]v1.ContainerStatus{v1.ContainerStatus{Name:"c", State:v1.ContainerState{Waiting:(*v1.ContainerStateWaiting)(nil), Running:(*v1.ContainerStateRunning)(nil), Terminated:(*v1.ContainerStateTerminated)(0xc00025f650)}, LastTerminationState:v1.ContainerState{Waiting:(*v1.ContainerStateWaiting)(nil), Running:(*v1.ContainerStateRunning)(nil), Terminated:(*v1.ContainerStateTerminated)(nil)}, Ready:false, RestartCount:0, Image:"registry.k8s.io/e2e-test-images/agnhost:2.53", ImageID:"registry.k8s.io/e2e-test-images/agnhost@sha256:99c6b4bb4a1e1df3f0b3752168c89358794d02258ebebc26bf21c29399011a85", ContainerID:"containerd://6270b0109a689462d230824991c0ef73f7aed792429144b12b2b4a1d6c70a421", Started:(*bool)(0xc000c0afd9), AllocatedResources:v1.ResourceList(nil), Resources:(*v1.ResourceRequirements)(nil), VolumeMounts:[]v1.VolumeMountStatus{v1.VolumeMountStatus{Name:"kube-api-access-8rmqj", MountPath:"/var/run/secrets/kubernetes.io/serviceaccount", ReadOnly:true, RecursiveReadOnly:(*v1.RecursiveReadOnlyMode)(0xc000c06860)}}, User:(*v1.ContainerUser)(nil), AllocatedResourcesStatus:[]v1.ResourceStatus(nil)}}, QOSClass:"Burstable", EphemeralContainerStatuses:[]v1.ContainerStatus(nil), Resize:"", ResourceClaimStatuses:[]v1.PodResourceClaimStatus(nil)}
Expected
    <v1.PodPhase>: Succeeded
to equal
    <v1.PodPhase>: Failed
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/pod_test.go:486 @ 03/21/25 05:54:58.464
}
```

**What you expected to happen**:

no errors

**How to reproduce it (as minimally and precisely as possible)**:

https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/4730/pull-kueue-test-e2e-release-0-11-1-32/1902957672265682944

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-21T06:00:51Z

/kind flake

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-21T06:03:11Z

cc @mbobrovskyi @mszadkow PTAL

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-03-21T10:26:04Z

The problem here is that preemption happened but we assume it will cause pods to close with `Failed` and it was `Succeed`...
```
g.Expect(p.Status.Phase).To(gomega.Equal(corev1.PodFailed), fmt.Sprintf("%#v", p.Status))
```
utterly strange, as "pause" argument for `agnhost` is straightforward:
SIGTERM -> exit 2
SIGKILL -> exit 1

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-21T10:31:21Z

Yes, FYI this is the image: https://github.com/kubernetes/kubernetes/blob/47a61c5c98822989d955e00d42f895234c1a1cb1/test/images/agnhost/pause/pause.go#L37-L56

So, it seems that indeed it handles SIGTERM and SIGINT with non-zero codes. However, I'm wondering what happens if we send SIGTERM before the SIGTERM trap is registered. Maybe we again hit the narrow path between Running, and Running with traps. Dunno, maybe check locally and insert sleep before registering the traps.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-21T10:33:27Z

I would try to recompile the image with adding sleep around here: https://github.com/kubernetes/kubernetes/blob/47a61c5c98822989d955e00d42f895234c1a1cb1/test/images/agnhost/pause/pause.go#L38. Maybe before this line Cobra registers its own SIGTERM trap which exists with 0, and only later is overwritten with Pause. Not sure, but this could explain it.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-21T10:58:36Z

Grepping the kubelet logs by the pods name and UID it seems it could be the scenario, as it was very racy. The DELETE was even before the phase was updating as Running. So the order of events in logs is Pending -> DELETE -> Running.
```
> cat kubelet.log | grep -e pod-e2e-tvsm2/default-priority-group-0 -e af51efce-60d0-4a13-b2d3-34e5ab7a78d0 | grep -e phase -e DELETE         
Mar 21 05:54:12 kind-worker kubelet[220]: I0321 05:54:12.959967     220 status_manager.go:920] "Status for pod updated successfully" pod="pod-e2e-tvsm2/default-priority-group-0" statusVersion=1 status={"phase":"Pending","conditions":[{"type":"PodReadyToStartContainers","status":"False","lastProbeTime":null,"lastTransitionTime":"2025-03-21T05:54:12Z"},{"type":"Initialized","status":"True","lastProbeTime":null,"lastTransitionTime":"2025-03-21T05:54:12Z"},{"type":"Ready","status":"False","lastProbeTime":null,"lastTransitionTime":"2025-03-21T05:54:12Z","reason":"ContainersNotReady","message":"containers with unready status: [c]"},{"type":"ContainersReady","status":"False","lastProbeTime":null,"lastTransitionTime":"2025-03-21T05:54:12Z","reason":"ContainersNotReady","message":"containers with unready status: [c]"},{"type":"PodScheduled","status":"True","lastProbeTime":null,"lastTransitionTime":"2025-03-21T05:54:12Z"}],"hostIP":"172.18.0.2","hostIPs":[{"ip":"172.18.0.2"}],"startTime":"2025-03-21T05:54:12Z","containerStatuses":[{"name":"c","state":{"waiting":{"reason":"ContainerCreating"}},"lastState":{},"ready":false,"restartCount":0,"image":"registry.k8s.io/e2e-test-images/agnhost:2.53@sha256:99c6b4bb4a1e1df3f0b3752168c89358794d02258ebebc26bf21c29399011a85","imageID":"","started":false,"volumeMounts":[{"name":"kube-api-access-8rmqj","mountPath":"/var/run/secrets/kubernetes.io/serviceaccount","readOnly":true,"recursiveReadOnly":"Disabled"}]}],"qosClass":"Burstable"}
Mar 21 05:54:13 kind-worker kubelet[220]: I0321 05:54:13.275786     220 kubelet.go:2484] "SyncLoop DELETE" source="api" pods=["pod-e2e-tvsm2/default-priority-group-0"]
Mar 21 05:54:13 kind-worker kubelet[220]: I0321 05:54:13.854890     220 status_manager.go:911] "Patch status for pod" pod="pod-e2e-tvsm2/default-priority-group-0" podUID="af51efce-60d0-4a13-b2d3-34e5ab7a78d0" patch="{\"metadata\":{\"uid\":\"af51efce-60d0-4a13-b2d3-34e5ab7a78d0\"},\"status\":{\"$setElementOrder/conditions\":[{\"type\":\"TerminationTarget\"},{\"type\":\"PodReadyToStartContainers\"},{\"type\":\"Initialized\"},{\"type\":\"Ready\"},{\"type\":\"ContainersReady\"},{\"type\":\"PodScheduled\"}],\"conditions\":[{\"lastTransitionTime\":\"2025-03-21T05:54:13Z\",\"status\":\"True\",\"type\":\"PodReadyToStartContainers\"},{\"lastTransitionTime\":\"2025-03-21T05:54:13Z\",\"message\":null,\"reason\":null,\"status\":\"True\",\"type\":\"Ready\"},{\"lastTransitionTime\":\"2025-03-21T05:54:13Z\",\"message\":null,\"reason\":null,\"status\":\"True\",\"type\":\"ContainersReady\"}],\"containerStatuses\":[{\"containerID\":\"containerd://6270b0109a689462d230824991c0ef73f7aed792429144b12b2b4a1d6c70a421\",\"image\":\"registry.k8s.io/e2e-test-images/agnhost:2.53\",\"imageID\":\"registry.k8s.io/e2e-test-images/agnhost@sha256:99c6b4bb4a1e1df3f0b3752168c89358794d02258ebebc26bf21c29399011a85\",\"lastState\":{},\"name\":\"c\",\"ready\":true,\"restartCount\":0,\"started\":true,\"state\":{\"running\":{\"startedAt\":\"2025-03-21T05:54:13Z\"}},\"volumeMounts\":[{\"mountPath\":\"/var/run/secrets/kubernetes.io/serviceaccount\",\"name\":\"kube-api-access-8rmqj\",\"readOnly\":true,\"recursiveReadOnly\":\"Disabled\"}]}],\"phase\":\"Running\",\"podIP\":\"10.244.1.142\",\"podIPs\":[{\"ip\":\"10.244.1.142\"}]}}"
Mar 21 05:54:13 kind-worker kubelet[220]: I0321 05:54:13.854974     220 status_manager.go:920] "Status for pod updated successfully" pod="pod-e2e-tvsm2/default-priority-group-0" statusVersion=2 status={"phase":"Running","cond
```

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-03-21T11:02:22Z

there is truth in what you say, it's even in the error log message:
Type:"Ready", Status:"False"
Type:"PodReadyToStartContainers", Status:"False"

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-03-21T20:41:59Z

I have added more logs to pause image:
```
Paused
Signals registered
received SIGTERM
```
Just out of curiosity I have added handler for SIGKILL, but preemption seems to send SIGTERM anyway...
To sum up:
Still no local reproduction, despite adding extra delay before registering signal handler.
PR that is linked that will make sure pod is ready before preemption.
However from outcome there is no difference if the pod is ready or just initialising, locally it works both ways...

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-24T06:24:42Z

I'm pretty sure I know what is going on. This is a bug in agnhost, take a look:

```golang

func pause(cmd *cobra.Command, args []string) {
        fmt.Println("Paused")
        sigCh := make(chan os.Signal, 1)
        done := make(chan int, 1)
        signal.Notify(sigCh, syscall.SIGINT)
        signal.Notify(sigCh, syscall.SIGTERM)
        go func() {
                sig := <-sigCh
                switch sig {
                case syscall.SIGINT:
                        done <- 1 
                        os.Exit(1)
                case syscall.SIGTERM:
                        done <- 2           // 1 : as we capture SIGTERM
                        os.Exit(2)          // 3 : we never actually reach here
                }
        }()
        result := <-done                    // 2a : we get the item and exit
        fmt.Printf("exiting %d\n", result)     
}                                           // 2b : exit here
```
In the unlikely run, the order of execution as above. You may test it by injecting `sleep(2s)` between 1 and 3.

So, I suggest:
- open a PR in agnohost, I believe we should only have `os.Exit(result)` at the bottom. No other calls to `os.Exit`.
- temporarily use `test-webserver` which should always end in non-zero looking at the code: https://github.com/kubernetes/kubernetes/blob/37afe38abf4edf76b0a3fb820e4e963263dda049/test/images/agnhost/test-webserver/test-webserver.go#L45-L63

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-03-24T09:13:01Z

OK, I will make the test first.

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-03-24T12:01:51Z

I can confirm first thing, we never see "exiting X" log right now.
Changing [pause](https://github.com/kubernetes/kubernetes/blob/37afe38abf4edf76b0a3fb820e4e963263dda049/test/images/agnhost/pause/pause.go) by removing lines 48 and 51 and adding `os.Exit(result)` after line 55 would do the trick.
I can confirm it works locally, but CI we need new published agnhost image.

I will use `test-web server` although this presents no difference locally, let me run this couple times in CI (in the PR).

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-24T12:07:56Z

> we never see "exiting X" log right now. 

by "never" you mean rarely? because I think when it fails, then it is actually logged, as pointed out in https://github.com/kubernetes-sigs/kueue/issues/4733#issuecomment-2747018044

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-24T13:30:51Z

Opened: https://github.com/kubernetes/kubernetes/issues/131021
