# Issue #4734: Flaky e2e test: Pod groups when Single CQ should allow to preempt the lower priority group

**Summary**: Flaky e2e test: Pod groups when Single CQ should allow to preempt the lower priority group

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4734

**Last updated**: 2025-03-21T06:04:01Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-03-21T05:59:30Z
- **Updated**: 2025-03-21T06:04:01Z
- **Closed**: 2025-03-21T06:03:33Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 5

## Description

/kind flake


**What happened**:

Failure on unrelated branch https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/4730/pull-kueue-test-e2e-release-0-11-1-32/1902957672265682944

**What you expected to happen**:

no failure

**How to reproduce it (as minimally and precisely as possible)**:

ci

**Anything else we need to know?**:

```
End To End Suite: kindest/node:v1.32.3: [It] Pod groups when Single CQ should allow to preempt the lower priority group expand_less	47s
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

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-21T05:59:45Z

cc @mbobrovskyi @mszadkow PTAL

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-21T06:01:42Z

Apparently BehaviorWaitForDeletionFailOnExit does not work as we thought since the Pod terminated in Succeeded.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-21T06:03:29Z

/close 
as a duplicate of https://github.com/kubernetes-sigs/kueue/issues/4733

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-03-21T06:03:34Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4734#issuecomment-2742405810):

>/close 
>as a duplicate of https://github.com/kubernetes-sigs/kueue/issues/4733


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-21T06:04:00Z

> /close as a duplicate of [#4733](https://github.com/kubernetes-sigs/kueue/issues/4733)

Oh, what a timing lol
