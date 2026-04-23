# Issue #4669: [Flaky test] Pod groups when Single CQ Failed Pod can be replaced in group

**Summary**: [Flaky test] Pod groups when Single CQ Failed Pod can be replaced in group

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4669

**Last updated**: 2025-03-19T08:10:47Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-03-18T10:44:50Z
- **Updated**: 2025-03-19T08:10:47Z
- **Closed**: 2025-03-19T08:10:45Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 15

## Description

**What happened**:

Flaked on unrelated branch https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/4658/pull-kueue-test-e2e-main-1-31/1901938587444711424

**What you expected to happen**:

no flakes

**How to reproduce it (as minimally and precisely as possible)**:

ci

**Anything else we need to know?**:

```
End To End Suite: kindest/node:v1.31.0: [It] Pod groups when Single CQ Failed Pod can be replaced in group expand_less	1m14s
{Timed out after 45.000s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/pod_test.go:218 with:
Expected
    <v1.PodPhase>: Running
to equal
    <v1.PodPhase>: Failed failed [FAILED] Timed out after 45.000s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/pod_test.go:218 with:
Expected
    <v1.PodPhase>: Running
to equal
    <v1.PodPhase>: Failed
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/pod_test.go:219 @ 03/18/25 10:22:06.676

There were additional failures detected after the initial failure. These are visible in the timeline
}
```
based on line numbers it happened already after https://github.com/kubernetes-sigs/kueue/pull/4660 which was believed to fix it.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-18T10:45:59Z

cc @mszadkow

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-18T10:51:29Z

Based on timestamps this is the namespace `pod-e2e-dx5dg`

All pods were scheduled to kind-worker (in particular the group-0 pod in question):

```
2025-03-18T10:21:19.143418583Z stderr F I0318 10:21:19.142499       1 schedule_one.go:314] "Successfully bound pod to node" pod="pod-e2e-dx5dg/group-2" node="kind-worker" evaluatedNodes=3 feasibleNodes=1
2025-03-18T10:21:19.154444091Z stderr F I0318 10:21:19.154076       1 schedule_one.go:314] "Successfully bound pod to node" pod="pod-e2e-dx5dg/group-0" node="kind-worker" evaluatedNodes=3 feasibleNodes=1
2025-03-18T10:21:19.154478761Z stderr F I0318 10:21:19.154260       1 schedule_one.go:314] "Successfully bound pod to node" pod="pod-e2e-dx5dg/group-1" node="kind-worker" evaluatedNodes=3 feasibleNodes=1
```

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-18T10:58:31Z

```
Mar 18 10:21:19 kind-worker kubelet[246]: I0318 10:21:19.149698     246 kubelet.go:2407] "SyncLoop ADD" source="api" pods=["pod-e2e-dx5dg/group-0"]
Mar 18 10:21:19 kind-worker kubelet[246]: I0318 10:21:19.151540     246 kubelet_pods.go:1774] "Generating pod status" podIsTerminal=false pod="pod-e2e-dx5dg/group-0"
Mar 18 10:21:19 kind-worker kubelet[246]: I0318 10:21:19.151791     246 util.go:30] "No sandbox for pod can be found. Need to start a new one" pod="pod-e2e-dx5dg/group-0"
Mar 18 10:21:19 kind-worker kubelet[246]: I0318 10:21:19.188114     246 volume_manager.go:404] "Waiting for volumes to attach and mount for pod" pod="pod-e2e-dx5dg/group-0"
Mar 18 10:21:19 kind-worker kubelet[246]: I0318 10:21:19.253480     246 reconciler_common.go:245] "operationExecutor.VerifyControllerAttachedVolume started for volume \"kube-api-access-v5gs9\" (UniqueName: \"kubernetes.io/projected/8bb7de3e-72f0-4102-adbd-53897040775e-kube-api-access-v5gs9\") pod \"group-0\" (UID: \"8bb7de3e-72f0-4102-adbd-53897040775e\") " pod="pod-e2e-dx5dg/group-0"
Mar 18 10:21:19 kind-worker kubelet[246]: I0318 10:21:19.303190     246 status_manager.go:872] "Patch status for pod" pod="pod-e2e-dx5dg/group-0" podUID="8bb7de3e-72f0-4102-adbd-53897040775e" patch="{\"metadata\":{\"uid\":\"8bb7de3e-72f0-4102-adbd-53897040775e\"},\"status\":{\"$setElementOrder/conditions\":[{\"type\":\"PodReadyToStartContainers\"},{\"type\":\"Initialized\"},{\"type\":\"Ready\"},{\"type\":\"ContainersReady\"},{\"type\":\"PodScheduled\"}],\"conditions\":[{\"lastProbeTime\":null,\"lastTransitionTime\":\"2025-03-18T10:21:19Z\",\"status\":\"False\",\"type\":\"PodReadyToStartContainers\"},{\"lastProbeTime\":null,\"lastTransitionTime\":\"2025-03-18T10:21:19Z\",\"status\":\"True\",\"type\":\"Initialized\"},{\"lastProbeTime\":null,\"lastTransitionTime\":\"2025-03-18T10:21:19Z\",\"message\":\"containers with unready status: [c]\",\"reason\":\"ContainersNotReady\",\"status\":\"False\",\"type\":\"Ready\"},{\"lastProbeTime\":null,\"lastTransitionTime\":\"2025-03-18T10:21:19Z\",\"message\":\"containers with unready status: [c]\",\"reason\":\"ContainersNotReady\",\"status\":\"False\",\"type\":\"ContainersReady\"}],\"containerStatuses\":[{\"image\":\"registry.k8s.io/e2e-test-images/agnhost:2.53@sha256:99c6b4bb4a1e1df3f0b3752168c89358794d02258ebebc26bf21c29399011a85\",\"imageID\":\"\",\"lastState\":{},\"name\":\"c\",\"ready\":false,\"restartCount\":0,\"started\":false,\"state\":{\"waiting\":{\"reason\":\"ContainerCreating\"}},\"volumeMounts\":[{\"mountPath\":\"/var/run/secrets/kubernetes.io/serviceaccount\",\"name\":\"kube-api-access-v5gs9\",\"readOnly\":true,\"recursiveReadOnly\":\"Disabled\"}]}],\"hostIP\":\"172.18.0.2\",\"hostIPs\":[{\"ip\":\"172.18.0.2\"}],\"startTime\":\"2025-03-18T10:21:19Z\"}}"
Mar 18 10:21:19 kind-worker kubelet[246]: I0318 10:21:19.303854     246 status_manager.go:881] "Status for pod updated successfully" pod="pod-e2e-dx5dg/group-0" statusVersion=1 status={"phase":"Pending","conditions":[{"type":"PodReadyToStartContainers","status":"False","lastProbeTime":null,"lastTransitionTime":"2025-03-18T10:21:19Z"},{"type":"Initialized","status":"True","lastProbeTime":null,"lastTransitionTime":"2025-03-18T10:21:19Z"},{"type":"Ready","status":"False","lastProbeTime":null,"lastTransitionTime":"2025-03-18T10:21:19Z","reason":"ContainersNotReady","message":"containers with unready status: [c]"},{"type":"ContainersReady","status":"False","lastProbeTime":null,"lastTransitionTime":"2025-03-18T10:21:19Z","reason":"ContainersNotReady","message":"containers with unready status: [c]"},{"type":"PodScheduled","status":"True","lastProbeTime":null,"lastTransitionTime":"2025-03-18T10:21:19Z"}],"hostIP":"172.18.0.2","hostIPs":[{"ip":"172.18.0.2"}],"startTime":"2025-03-18T10:21:19Z","containerStatuses":[{"name":"c","state":{"waiting":{"reason":"ContainerCreating"}},"lastState":{},"ready":false,"restartCount":0,"image":"registry.k8s.io/e2e-test-images/agnhost:2.53@sha256:99c6b4bb4a1e1df3f0b3752168c89358794d02258ebebc26bf21c29399011a85","imageID":"","started":false,"volumeMounts":[{"name":"kube-api-access-v5gs9","mountPath":"/var/run/secrets/kubernetes.io/serviceaccount","readOnly":true,"recursiveReadOnly":"Disabled"}]}],"qosClass":"Burstable"}
Mar 18 10:21:19 kind-worker kubelet[246]: I0318 10:21:19.354978     246 reconciler_common.go:218] "operationExecutor.MountVolume started for volume \"kube-api-access-v5gs9\" (UniqueName: \"kubernetes.io/projected/8bb7de3e-72f0-4102-adbd-53897040775e-kube-api-access-v5gs9\") pod \"group-0\" (UID: \"8bb7de3e-72f0-4102-adbd-53897040775e\") " pod="pod-e2e-dx5dg/group-0"
Mar 18 10:21:20 kind-worker kubelet[246]: I0318 10:21:20.161231     246 operation_generator.go:637] "MountVolume.SetUp succeeded for volume \"kube-api-access-v5gs9\" (UniqueName: \"kubernetes.io/projected/8bb7de3e-72f0-4102-adbd-53897040775e-kube-api-access-v5gs9\") pod \"group-0\" (UID: \"8bb7de3e-72f0-4102-adbd-53897040775e\") " pod="pod-e2e-dx5dg/group-0"
Mar 18 10:21:20 kind-worker kubelet[246]: I0318 10:21:20.391957     246 volume_manager.go:440] "All volumes are attached and mounted for pod" pod="pod-e2e-dx5dg/group-0"
Mar 18 10:21:20 kind-worker kubelet[246]: I0318 10:21:20.392041     246 util.go:30] "No sandbox for pod can be found. Need to start a new one" pod="pod-e2e-dx5dg/group-0"
Mar 18 10:21:20 kind-worker kubelet[246]: I0318 10:21:20.392064     246 kuberuntime_manager.go:1053] "computePodActions got for pod" podActions="KillPod: true, CreateSandbox: true, UpdatePodResources: false, Attempt: 0, InitContainersToStart: [], ContainersToStart: [0], EphemeralContainersToStart: [],ContainersToUpdate: map[], ContainersToKill: map[]" pod="pod-e2e-dx5dg/group-0"
Mar 18 10:21:20 kind-worker kubelet[246]: I0318 10:21:20.827341     246 kubelet_pods.go:261] "Creating hosts mount for container" pod="pod-e2e-dx5dg/group-0" containerName="c" podIPs=["10.244.1.17"] path=true
Mar 18 10:21:20 kind-worker kubelet[246]: I0318 10:21:20.828498     246 event.go:389] "Event occurred" object="pod-e2e-dx5dg/group-0" fieldPath="spec.containers{c}" kind="Pod" apiVersion="v1" type="Normal" reason="Pulled" message="Container image \"registry.k8s.io/e2e-test-images/agnhost:2.53@sha256:99c6b4bb4a1e1df3f0b3752168c89358794d02258ebebc26bf21c29399011a85\" already present on machine"
Mar 18 10:21:20 kind-worker kubelet[246]: I0318 10:21:20.871339     246 event.go:389] "Event occurred" object="pod-e2e-dx5dg/group-0" fieldPath="spec.containers{c}" kind="Pod" apiVersion="v1" type="Normal" reason="Created" message="Created container c"
Mar 18 10:21:21 kind-worker kubelet[246]: I0318 10:21:21.298011     246 event.go:389] "Event occurred" object="pod-e2e-dx5dg/group-0" fieldPath="spec.containers{c}" kind="Pod" apiVersion="v1" type="Normal" reason="Started" message="Started container c"
Mar 18 10:21:21 kind-worker kubelet[246]: I0318 10:21:21.516037     246 kubelet.go:2439] "SyncLoop (PLEG): event for pod" pod="pod-e2e-dx5dg/group-0" event={"ID":"8bb7de3e-72f0-4102-adbd-53897040775e","Type":"ContainerStarted","Data":"62e04a72b1c5bb855056e55b44513a36a9f338baa5ee997b5ea20858b61fa058"}
Mar 18 10:21:21 kind-worker kubelet[246]: I0318 10:21:21.516131     246 kubelet.go:2439] "SyncLoop (PLEG): event for pod" pod="pod-e2e-dx5dg/group-0" event={"ID":"8bb7de3e-72f0-4102-adbd-53897040775e","Type":"ContainerStarted","Data":"86c8014e2400986b752c3d7825a3b6d859509a55b288964aa2f2dbbd69ffd484"}
Mar 18 10:21:21 kind-worker kubelet[246]: I0318 10:21:21.516178     246 kubelet_pods.go:1774] "Generating pod status" podIsTerminal=false pod="pod-e2e-dx5dg/group-0"
Mar 18 10:21:21 kind-worker kubelet[246]: I0318 10:21:21.516571     246 volume_manager.go:404] "Waiting for volumes to attach and mount for pod" pod="pod-e2e-dx5dg/group-0"
Mar 18 10:21:21 kind-worker kubelet[246]: I0318 10:21:21.516640     246 volume_manager.go:440] "All volumes are attached and mounted for pod" pod="pod-e2e-dx5dg/group-0"
Mar 18 10:21:21 kind-worker kubelet[246]: I0318 10:21:21.516716     246 kuberuntime_manager.go:1053] "computePodActions got for pod" podActions="KillPod: false, CreateSandbox: false, UpdatePodResources: false, Attempt: 0, InitContainersToStart: [], ContainersToStart: [], EphemeralContainersToStart: [],ContainersToUpdate: map[], ContainersToKill: map[]" pod="pod-e2e-dx5dg/group-0"
Mar 18 10:21:21 kind-worker kubelet[246]: I0318 10:21:21.586198     246 status_manager.go:872] "Patch status for pod" pod="pod-e2e-dx5dg/group-0" podUID="8bb7de3e-72f0-4102-adbd-53897040775e" patch="{\"metadata\":{\"uid\":\"8bb7de3e-72f0-4102-adbd-53897040775e\"},\"status\":{\"$setElementOrder/conditions\":[{\"type\":\"PodReadyToStartContainers\"},{\"type\":\"Initialized\"},{\"type\":\"Ready\"},{\"type\":\"ContainersReady\"},{\"type\":\"PodScheduled\"}],\"conditions\":[{\"lastTransitionTime\":\"2025-03-18T10:21:21Z\",\"status\":\"True\",\"type\":\"PodReadyToStartContainers\"},{\"lastTransitionTime\":\"2025-03-18T10:21:21Z\",\"message\":null,\"reason\":null,\"status\":\"True\",\"type\":\"Ready\"},{\"lastTransitionTime\":\"2025-03-18T10:21:21Z\",\"message\":null,\"reason\":null,\"status\":\"True\",\"type\":\"ContainersReady\"}],\"containerStatuses\":[{\"containerID\":\"containerd://62e04a72b1c5bb855056e55b44513a36a9f338baa5ee997b5ea20858b61fa058\",\"image\":\"registry.k8s.io/e2e-test-images/agnhost:2.53\",\"imageID\":\"docker.io/library/import-2025-03-18@sha256:b834a6ce4fdd44c6a61b08aad29a66af701a413fe3e41c7147d0786e10b0215e\",\"lastState\":{},\"name\":\"c\",\"ready\":true,\"restartCount\":0,\"started\":true,\"state\":{\"running\":{\"startedAt\":\"2025-03-18T10:21:21Z\"}},\"volumeMounts\":[{\"mountPath\":\"/var/run/secrets/kubernetes.io/serviceaccount\",\"name\":\"kube-api-access-v5gs9\",\"readOnly\":true,\"recursiveReadOnly\":\"Disabled\"}]}],\"phase\":\"Running\",\"podIP\":\"10.244.1.17\",\"podIPs\":[{\"ip\":\"10.244.1.17\"}]}}"
Mar 18 10:21:21 kind-worker kubelet[246]: I0318 10:21:21.586345     246 status_manager.go:881] "Status for pod updated successfully" pod="pod-e2e-dx5dg/group-0" statusVersion=2 status={"phase":"Running","conditions":[{"type":"PodReadyToStartContainers","status":"True","lastProbeTime":null,"lastTransitionTime":"2025-03-18T10:21:21Z"},{"type":"Initialized","status":"True","lastProbeTime":null,"lastTransitionTime":"2025-03-18T10:21:19Z"},{"type":"Ready","status":"True","lastProbeTime":null,"lastTransitionTime":"2025-03-18T10:21:21Z"},{"type":"ContainersReady","status":"True","lastProbeTime":null,"lastTransitionTime":"2025-03-18T10:21:21Z"},{"type":"PodScheduled","status":"True","lastProbeTime":null,"lastTransitionTime":"2025-03-18T10:21:19Z"}],"hostIP":"172.18.0.2","hostIPs":[{"ip":"172.18.0.2"}],"podIP":"10.244.1.17","podIPs":[{"ip":"10.244.1.17"}],"startTime":"2025-03-18T10:21:19Z","containerStatuses":[{"name":"c","state":{"running":{"startedAt":"2025-03-18T10:21:21Z"}},"lastState":{},"ready":true,"restartCount":0,"image":"registry.k8s.io/e2e-test-images/agnhost:2.53","imageID":"docker.io/library/import-2025-03-18@sha256:b834a6ce4fdd44c6a61b08aad29a66af701a413fe3e41c7147d0786e10b0215e","containerID":"containerd://62e04a72b1c5bb855056e55b44513a36a9f338baa5ee997b5ea20858b61fa058","started":true,"volumeMounts":[{"name":"kube-api-access-v5gs9","mountPath":"/var/run/secrets/kubernetes.io/serviceaccount","readOnly":true,"recursiveReadOnly":"Disabled"}]}],"qosClass":"Burstable"}
Mar 18 10:21:21 kind-worker kubelet[246]: I0318 10:21:21.586441     246 pod_startup_latency_tracker.go:172] "Mark when the pod was running for the first time" pod="pod-e2e-dx5dg/group-0" rv="3637"
Mar 18 10:21:21 kind-worker kubelet[246]: I0318 10:21:21.676439     246 pod_startup_latency_tracker.go:104] "Observed pod startup duration" pod="pod-e2e-dx5dg/group-0" podStartSLOduration=3.676410453 podStartE2EDuration="3.676410453s" podCreationTimestamp="2025-03-18 10:21:18 +0000 UTC" firstStartedPulling="0001-01-01 00:00:00 +0000 UTC" lastFinishedPulling="0001-01-01 00:00:00 +0000 UTC" observedRunningTime="2025-03-18 10:21:21.586452803 +0000 UTC m=+274.111251646" watchObservedRunningTime="2025-03-18 10:21:21.676410453 +0000 UTC m=+274.201209316"
Mar 18 10:21:21 kind-worker kubelet[246]: I0318 10:21:21.676696     246 kubelet.go:2423] "SyncLoop DELETE" source="api" pods=["pod-e2e-dx5dg/group-0"]
Mar 18 10:21:21 kind-worker kubelet[246]: I0318 10:21:21.676747     246 pod_workers.go:970] "Cancelling current pod sync" pod="pod-e2e-dx5dg/group-0" podUID="8bb7de3e-72f0-4102-adbd-53897040775e" workType="terminating"
Mar 18 10:21:22 kind-worker kubelet[246]: I0318 10:21:22.519390     246 kubelet_pods.go:1774] "Generating pod status" podIsTerminal=false pod="pod-e2e-dx5dg/group-0"
Mar 18 10:21:22 kind-worker kubelet[246]: I0318 10:21:22.519778     246 kuberuntime_container.go:787] "Killing container with a grace period override" pod="pod-e2e-dx5dg/group-0" podUID="8bb7de3e-72f0-4102-adbd-53897040775e" containerName="c" containerID="containerd://62e04a72b1c5bb855056e55b44513a36a9f338baa5ee997b5ea20858b61fa058" gracePeriod=1
Mar 18 10:21:22 kind-worker kubelet[246]: I0318 10:21:22.519925     246 kuberuntime_container.go:808] "Killing container with a grace period" pod="pod-e2e-dx5dg/group-0" podUID="8bb7de3e-72f0-4102-adbd-53897040775e" containerName="c" containerID="containerd://62e04a72b1c5bb855056e55b44513a36a9f338baa5ee997b5ea20858b61fa058" gracePeriod=2
Mar 18 10:21:22 kind-worker kubelet[246]: I0318 10:21:22.520840     246 event.go:389] "Event occurred" object="pod-e2e-dx5dg/group-0" fieldPath="spec.containers{c}" kind="Pod" apiVersion="v1" type="Normal" reason="Killing" message="Stopping container c"
Mar 18 10:21:22 kind-worker kubelet[246]: I0318 10:21:22.622568     246 status_manager.go:872] "Patch status for pod" pod="pod-e2e-dx5dg/group-0" podUID="8bb7de3e-72f0-4102-adbd-53897040775e" patch="{\"metadata\":{\"uid\":\"8bb7de3e-72f0-4102-adbd-53897040775e\"}}"
Mar 18 10:21:22 kind-worker kubelet[246]: I0318 10:21:22.622656     246 status_manager.go:879] "Status for pod is up-to-date" pod="pod-e2e-dx5dg/group-0" statusVersion=3
Mar 18 10:21:22 kind-worker kubelet[246]: I0318 10:21:22.622680     246 status_manager.go:937] "Delaying pod deletion as the phase is non-terminal" phase="Running" localPhase="Running" pod="pod-e2e-dx5dg/group-0" podUID="8bb7de3e-72f0-4102-adbd-53897040775e"
Mar 18 10:21:27 kind-worker kubelet[246]: I0318 10:21:27.622036     246 status_manager.go:937] "Delaying pod deletion as the phase is non-terminal" phase="Running" localPhase="Running" pod="pod-e2e-dx5dg/group-0" podUID="8bb7de3e-72f0-4102-adbd-53897040775e"
Mar 18 10:21:37 kind-worker kubelet[246]: I0318 10:21:37.621561     246 status_manager.go:937] "Delaying pod deletion as the phase is non-terminal" phase="Running" localPhase="Running" pod="pod-e2e-dx5dg/group-0" podUID="8bb7de3e-72f0-4102-adbd-53897040775e"
Mar 18 10:21:47 kind-worker kubelet[246]: I0318 10:21:47.621956     246 status_manager.go:937] "Delaying pod deletion as the phase is non-terminal" phase="Running" localPhase="Running" pod="pod-e2e-dx5dg/group-0" podUID="8bb7de3e-72f0-4102-adbd-53897040775e"
Mar 18 10:21:57 kind-worker kubelet[246]: I0318 10:21:57.622068     246 status_manager.go:937] "Delaying pod deletion as the phase is non-terminal" phase="Running" localPhase="Running" pod="pod-e2e-dx5dg/group-0" podUID="8bb7de3e-72f0-4102-adbd-53897040775e"
Mar 18 10:21:59 kind-worker kubelet[246]: I0318 10:21:59.227747     246 kuberuntime_container.go:817] "Container exited normally" pod="pod-e2e-dx5dg/group-0" podUID="8bb7de3e-72f0-4102-adbd-53897040775e" containerName="c" containerID="containerd://62e04a72b1c5bb855056e55b44513a36a9f338baa5ee997b5ea20858b61fa058"
Mar 18 10:21:59 kind-worker kubelet[246]: I0318 10:21:59.648493     246 kubelet.go:2439] "SyncLoop (PLEG): event for pod" pod="pod-e2e-dx5dg/group-0" event={"ID":"8bb7de3e-72f0-4102-adbd-53897040775e","Type":"ContainerDied","Data":"62e04a72b1c5bb855056e55b44513a36a9f338baa5ee997b5ea20858b61fa058"}
Mar 18 10:22:07 kind-worker kubelet[246]: I0318 10:22:07.625568     246 status_manager.go:937] "Delaying pod deletion as the phase is non-terminal" phase="Running" localPhase="Running" pod="pod-e2e-dx5dg/group-0" podUID="8bb7de3e-72f0-4102-adbd-53897040775e"
Mar 18 10:22:16 kind-worker kubelet[246]: I0318 10:22:16.646544     246 kubelet_pods.go:1774] "Generating pod status" podIsTerminal=true pod="pod-e2e-dx5dg/group-0"
Mar 18 10:22:16 kind-worker kubelet[246]: I0318 10:22:16.646618     246 util.go:48] "No ready sandbox for pod can be found. Need to start a new one" pod="pod-e2e-dx5dg/group-0"
Mar 18 10:22:16 kind-worker kubelet[246]: I0318 10:22:16.700503     246 kubelet.go:2439] "SyncLoop (PLEG): event for pod" pod="pod-e2e-dx5dg/group-0" event={"ID":"8bb7de3e-72f0-4102-adbd-53897040775e","Type":"ContainerDied","Data":"86c8014e2400986b752c3d7825a3b6d859509a55b288964aa2f2dbbd69ffd484"}
Mar 18 10:22:16 kind-worker kubelet[246]: I0318 10:22:16.700530     246 kubelet_pods.go:1774] "Generating pod status" podIsTerminal=true pod="pod-e2e-dx5dg/group-0"
Mar 18 10:22:16 kind-worker kubelet[246]: I0318 10:22:16.700639     246 util.go:48] "No ready sandbox for pod can be found. Need to start a new one" pod="pod-e2e-dx5dg/group-0"
Mar 18 10:22:16 kind-worker kubelet[246]: I0318 10:22:16.700720     246 volume_manager.go:449] "Waiting for volumes to unmount for pod" pod="pod-e2e-dx5dg/group-0"
Mar 18 10:22:16 kind-worker kubelet[246]: I0318 10:22:16.700759     246 volume_manager.go:478] "All volumes are unmounted for pod" pod="pod-e2e-dx5dg/group-0"
Mar 18 10:22:16 kind-worker kubelet[246]: I0318 10:22:16.700835     246 kubelet.go:2178] "Pod termination cleaned up volume paths" pod="pod-e2e-dx5dg/group-0" podUID="8bb7de3e-72f0-4102-adbd-53897040775e"
Mar 18 10:22:16 kind-worker kubelet[246]: I0318 10:22:16.781294     246 status_manager.go:872] "Patch status for pod" pod="pod-e2e-dx5dg/group-0" podUID="8bb7de3e-72f0-4102-adbd-53897040775e" patch="{\"metadata\":{\"uid\":\"8bb7de3e-72f0-4102-adbd-53897040775e\"},\"status\":{\"$setElementOrder/conditions\":[{\"type\":\"PodReadyToStartContainers\"},{\"type\":\"Initialized\"},{\"type\":\"Ready\"},{\"type\":\"ContainersReady\"},{\"type\":\"PodScheduled\"}],\"conditions\":[{\"lastTransitionTime\":\"2025-03-18T10:22:16Z\",\"status\":\"False\",\"type\":\"PodReadyToStartContainers\"},{\"lastTransitionTime\":\"2025-03-18T10:22:16Z\",\"reason\":\"PodFailed\",\"status\":\"False\",\"type\":\"Ready\"},{\"lastTransitionTime\":\"2025-03-18T10:22:16Z\",\"reason\":\"PodFailed\",\"status\":\"False\",\"type\":\"ContainersReady\"}],\"containerStatuses\":[{\"containerID\":\"containerd://62e04a72b1c5bb855056e55b44513a36a9f338baa5ee997b5ea20858b61fa058\",\"image\":\"registry.k8s.io/e2e-test-images/agnhost:2.53\",\"imageID\":\"docker.io/library/import-2025-03-18@sha256:b834a6ce4fdd44c6a61b08aad29a66af701a413fe3e41c7147d0786e10b0215e\",\"lastState\":{},\"name\":\"c\",\"ready\":false,\"restartCount\":0,\"started\":false,\"state\":{\"terminated\":{\"containerID\":\"containerd://62e04a72b1c5bb855056e55b44513a36a9f338baa5ee997b5ea20858b61fa058\",\"exitCode\":2,\"finishedAt\":\"2025-03-18T10:21:22Z\",\"reason\":\"Error\",\"startedAt\":\"2025-03-18T10:21:21Z\"}},\"volumeMounts\":[{\"mountPath\":\"/var/run/secrets/kubernetes.io/serviceaccount\",\"name\":\"kube-api-access-v5gs9\",\"readOnly\":true,\"recursiveReadOnly\":\"Disabled\"}]}],\"phase\":\"Failed\"}}"
Mar 18 10:22:16 kind-worker kubelet[246]: I0318 10:22:16.781386     246 status_manager.go:881] "Status for pod updated successfully" pod="pod-e2e-dx5dg/group-0" statusVersion=4 status={"phase":"Failed","conditions":[{"type":"PodReadyToStartContainers","status":"False","lastProbeTime":null,"lastTransitionTime":"2025-03-18T10:22:16Z"},{"type":"Initialized","status":"True","lastProbeTime":null,"lastTransitionTime":"2025-03-18T10:21:19Z"},{"type":"Ready","status":"False","lastProbeTime":null,"lastTransitionTime":"2025-03-18T10:22:16Z","reason":"PodFailed"},{"type":"ContainersReady","status":"False","lastProbeTime":null,"lastTransitionTime":"2025-03-18T10:22:16Z","reason":"PodFailed"},{"type":"PodScheduled","status":"True","lastProbeTime":null,"lastTransitionTime":"2025-03-18T10:21:19Z"}],"hostIP":"172.18.0.2","hostIPs":[{"ip":"172.18.0.2"}],"podIP":"10.244.1.17","podIPs":[{"ip":"10.244.1.17"}],"startTime":"2025-03-18T10:21:19Z","containerStatuses":[{"name":"c","state":{"terminated":{"exitCode":2,"reason":"Error","startedAt":"2025-03-18T10:21:21Z","finishedAt":"2025-03-18T10:21:22Z","containerID":"containerd://62e04a72b1c5bb855056e55b44513a36a9f338baa5ee997b5ea20858b61fa058"}},"lastState":{},"ready":false,"restartCount":0,"image":"registry.k8s.io/e2e-test-images/agnhost:2.53","imageID":"docker.io/library/import-2025-03-18@sha256:b834a6ce4fdd44c6a61b08aad29a66af701a413fe3e41c7147d0786e10b0215e","containerID":"containerd://62e04a72b1c5bb855056e55b44513a36a9f338baa5ee997b5ea20858b61fa058","started":false,"volumeMounts":[{"name":"kube-api-access-v5gs9","mountPath":"/var/run/secrets/kubernetes.io/serviceaccount","readOnly":true,"recursiveReadOnly":"Disabled"}]}],"qosClass":"Burstable"}
Mar 18 10:22:16 kind-worker kubelet[246]: I0318 10:22:16.784602     246 status_manager.go:872] "Patch status for pod" pod="pod-e2e-dx5dg/group-0" podUID="8bb7de3e-72f0-4102-adbd-53897040775e" patch="{\"metadata\":{\"uid\":\"8bb7de3e-72f0-4102-adbd-53897040775e\"}}"
Mar 18 10:22:16 kind-worker kubelet[246]: I0318 10:22:16.784647     246 status_manager.go:879] "Status for pod is up-to-date" pod="pod-e2e-dx5dg/group-0" statusVersion=6
Mar 18 10:22:16 kind-worker kubelet[246]: I0318 10:22:16.784665     246 status_manager.go:942] "The pod termination is finished as SyncTerminatedPod completes its execution" phase="Failed" localPhase="Failed" pod="pod-e2e-dx5dg/group-0" podUID="8bb7de3e-72f0-4102-adbd-53897040775e"
Mar 18 10:22:16 kind-worker kubelet[246]: I0318 10:22:16.814191     246 kubelet.go:2423] "SyncLoop DELETE" source="api" pods=["pod-e2e-dx5dg/group-0"]
Mar 18 10:22:16 kind-worker kubelet[246]: I0318 10:22:16.943441     246 status_manager.go:910] "Pod fully terminated and removed from etcd" pod="pod-e2e-dx5dg/group-0"
Mar 18 10:22:16 kind-worker kubelet[246]: I0318 10:22:16.943774     246 kubelet.go:2417] "SyncLoop REMOVE" source="api" pods=["pod-e2e-dx5dg/group-0"]
Mar 18 10:22:16 kind-worker kubelet[246]: I0318 10:22:16.943833     246 kubelet.go:2262] "Pod has been deleted and must be killed" pod="pod-e2e-dx5dg/group-0" podUID="8bb7de3e-72f0-4102-adbd-53897040775e"
```

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-18T11:03:23Z

So, DELETE happened at `Mar 18 10:21:21 ` and we see rightfully 
```
Mar 18 10:21:22 kind-worker kubelet[246]: I0318 10:21:22.519778     246 kuberuntime_container.go:787] "Killing container with a grace period override" pod="pod-e2e-dx5dg/group-0" podUID="8bb7de3e-72f0-4102-adbd-53897040775e" containerName="c" containerID="containerd://62e04a72b1c5bb855056e55b44513a36a9f338baa5ee997b5ea20858b61fa058" gracePeriod=1
```
that the pod was killed with grace period override. Still, it took a lot of time, and we got
```
Mar 18 10:21:59 kind-worker kubelet[246]: I0318 10:21:59.227747     246 kuberuntime_container.go:817] "Container exited normally" pod="pod-e2e-dx5dg/group-0" podUID="8bb7de3e-72f0-4102-adbd-53897040775e" containerName="c" containerID="containerd://62e04a72b1c5bb855056e55b44513a36a9f338baa5ee997b5ea20858b61fa058"
```
and the status was finally patched as Failed only at `10:22:16`, so after nearly 1min.
```
Mar 18 10:22:16 kind-worker kubelet[246]: I0318 10:22:16.781294     246 status_manager.go:872] "Patch status for pod"
```
I'm not sure what is going on, but terminating pods with sigkill is kubelet task, so it seems that it is kubelet that is actually overloaded.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-18T11:04:11Z

cc @tenzen-y @mszadkow @mbobrovskyi any more ideas, or we maybe introduce a new timeout, something like `DoubleLongTimeout=1min30s`, to avoid bumping `LongTimeout`?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-18T11:09:04Z

/kind flake

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-18T11:12:47Z

Or alternatively, maybe we should bump the resources in test-infra? I guess it could be justified given adding some more operators to the testing recently.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-18T11:16:55Z

I also looked into containerd logs for some hints:
```
> cat containerd.log | grep -e 86c8014e2400986b752c3d7825a3b6d859509a55b288964aa2f2dbbd69ffd484 -e 62e04a72b1c5bb855056e55b44513a36a9f338baa5ee997b5ea20858b61fa058    
Mar 18 10:21:20 kind-worker containerd[110]: time="2025-03-18T10:21:20.821903619Z" level=info msg="RunPodSandbox for &PodSandboxMetadata{Name:group-0,Uid:8bb7de3e-72f0-4102-adbd-53897040775e,Namespace:pod-e2e-dx5dg,Attempt:0,} returns sandbox id \"86c8014e2400986b752c3d7825a3b6d859509a55b288964aa2f2dbbd69ffd484\""
Mar 18 10:21:20 kind-worker containerd[110]: time="2025-03-18T10:21:20.833061040Z" level=info msg="CreateContainer within sandbox \"86c8014e2400986b752c3d7825a3b6d859509a55b288964aa2f2dbbd69ffd484\" for container &ContainerMetadata{Name:c,Attempt:0,}"
Mar 18 10:21:20 kind-worker containerd[110]: time="2025-03-18T10:21:20.870562025Z" level=info msg="CreateContainer within sandbox \"86c8014e2400986b752c3d7825a3b6d859509a55b288964aa2f2dbbd69ffd484\" for &ContainerMetadata{Name:c,Attempt:0,} returns container id \"62e04a72b1c5bb855056e55b44513a36a9f338baa5ee997b5ea20858b61fa058\""
Mar 18 10:21:20 kind-worker containerd[110]: time="2025-03-18T10:21:20.872048470Z" level=info msg="StartContainer for \"62e04a72b1c5bb855056e55b44513a36a9f338baa5ee997b5ea20858b61fa058\""
Mar 18 10:21:21 kind-worker containerd[110]: time="2025-03-18T10:21:21.293142774Z" level=info msg="StartContainer for \"62e04a72b1c5bb855056e55b44513a36a9f338baa5ee997b5ea20858b61fa058\" returns successfully"
Mar 18 10:21:22 kind-worker containerd[110]: time="2025-03-18T10:21:22.521444907Z" level=info msg="StopContainer for \"62e04a72b1c5bb855056e55b44513a36a9f338baa5ee997b5ea20858b61fa058\" with timeout 2 (s)"
Mar 18 10:21:22 kind-worker containerd[110]: time="2025-03-18T10:21:22.522137523Z" level=info msg="Stop container \"62e04a72b1c5bb855056e55b44513a36a9f338baa5ee997b5ea20858b61fa058\" with signal terminated"
Mar 18 10:21:24 kind-worker containerd[110]: time="2025-03-18T10:21:24.541039858Z" level=info msg="Kill container \"62e04a72b1c5bb855056e55b44513a36a9f338baa5ee997b5ea20858b61fa058\""
Mar 18 10:21:32 kind-worker containerd[110]: time="2025-03-18T10:21:32.558785038Z" level=error msg="failed to handle container TaskExit event container_id:\"62e04a72b1c5bb855056e55b44513a36a9f338baa5ee997b5ea20858b61fa058\" id:\"62e04a72b1c5bb855056e55b44513a36a9f338baa5ee997b5ea20858b61fa058\" pid:4020 exit_status:2 exited_at:{seconds:1742293282 nanos:547387052}" error="failed to stop container: failed to delete task: context deadline exceeded: unknown"
Mar 18 10:21:52 kind-worker containerd[110]: time="2025-03-18T10:21:52.551980894Z" level=info msg="TaskExit event container_id:\"62e04a72b1c5bb855056e55b44513a36a9f338baa5ee997b5ea20858b61fa058\" id:\"62e04a72b1c5bb855056e55b44513a36a9f338baa5ee997b5ea20858b61fa058\" pid:4020 exit_status:2 exited_at:{seconds:1742293282 nanos:547387052}"
Mar 18 10:21:54 kind-worker containerd[110]: time="2025-03-18T10:21:54.552580823Z" level=error msg="get state for 62e04a72b1c5bb855056e55b44513a36a9f338baa5ee997b5ea20858b61fa058" error="context deadline exceeded: unknown"
Mar 18 10:21:59 kind-worker containerd[110]: time="2025-03-18T10:21:59.165037793Z" level=info msg="shim disconnected" id=62e04a72b1c5bb855056e55b44513a36a9f338baa5ee997b5ea20858b61fa058 namespace=k8s.io
Mar 18 10:21:59 kind-worker containerd[110]: time="2025-03-18T10:21:59.165280818Z" level=warning msg="cleaning up after shim disconnected" id=62e04a72b1c5bb855056e55b44513a36a9f338baa5ee997b5ea20858b61fa058 namespace=k8s.io
Mar 18 10:21:59 kind-worker containerd[110]: time="2025-03-18T10:21:59.221643419Z" level=info msg="Ensure that container 62e04a72b1c5bb855056e55b44513a36a9f338baa5ee997b5ea20858b61fa058 in task-service has been cleanup successfully"
Mar 18 10:21:59 kind-worker containerd[110]: time="2025-03-18T10:21:59.223319276Z" level=info msg="StopContainer for \"62e04a72b1c5bb855056e55b44513a36a9f338baa5ee997b5ea20858b61fa058\" returns successfully"
Mar 18 10:21:59 kind-worker containerd[110]: time="2025-03-18T10:21:59.228369037Z" level=info msg="StopPodSandbox for \"86c8014e2400986b752c3d7825a3b6d859509a55b288964aa2f2dbbd69ffd484\""
Mar 18 10:21:59 kind-worker containerd[110]: time="2025-03-18T10:21:59.228460979Z" level=info msg="Container to stop \"62e04a72b1c5bb855056e55b44513a36a9f338baa5ee997b5ea20858b61fa058\" must be in running or unknown state, current state \"CONTAINER_EXITED\""
Mar 18 10:22:09 kind-worker containerd[110]: time="2025-03-18T10:22:09.282425039Z" level=error msg="failed to handle sandbox TaskExit event container_id:\"86c8014e2400986b752c3d7825a3b6d859509a55b288964aa2f2dbbd69ffd484\" id:\"86c8014e2400986b752c3d7825a3b6d859509a55b288964aa2f2dbbd69ffd484\" pid:3915 exit_status:137 exited_at:{seconds:1742293319 nanos:281077149}" error="failed to stop sandbox: failed to delete task: context deadline exceeded: unknown"
Mar 18 10:22:10 kind-worker containerd[110]: time="2025-03-18T10:22:10.551517977Z" level=info msg="TaskExit event container_id:\"86c8014e2400986b752c3d7825a3b6d859509a55b288964aa2f2dbbd69ffd484\" id:\"86c8014e2400986b752c3d7825a3b6d859509a55b288964aa2f2dbbd69ffd484\" pid:3915 exit_status:137 exited_at:{seconds:1742293319 nanos:281077149}"
Mar 18 10:22:12 kind-worker containerd[110]: time="2025-03-18T10:22:12.552164538Z" level=error msg="get state for 86c8014e2400986b752c3d7825a3b6d859509a55b288964aa2f2dbbd69ffd484" error="context deadline exceeded: unknown"
Mar 18 10:22:16 kind-worker containerd[110]: time="2025-03-18T10:22:16.502585897Z" level=info msg="shim disconnected" id=86c8014e2400986b752c3d7825a3b6d859509a55b288964aa2f2dbbd69ffd484 namespace=k8s.io
Mar 18 10:22:16 kind-worker containerd[110]: time="2025-03-18T10:22:16.502630818Z" level=warning msg="cleaning up after shim disconnected" id=86c8014e2400986b752c3d7825a3b6d859509a55b288964aa2f2dbbd69ffd484 namespace=k8s.io
Mar 18 10:22:16 kind-worker containerd[110]: time="2025-03-18T10:22:16.522748892Z" level=info msg="Ensure that sandbox 86c8014e2400986b752c3d7825a3b6d859509a55b288964aa2f2dbbd69ffd484 in task-service has been cleanup successfully"
Mar 18 10:22:16 kind-worker containerd[110]: time="2025-03-18T10:22:16.639711097Z" level=info msg="TearDown network for sandbox \"86c8014e2400986b752c3d7825a3b6d859509a55b288964aa2f2dbbd69ffd484\" successfully"
Mar 18 10:22:16 kind-worker containerd[110]: time="2025-03-18T10:22:16.639762569Z" level=info msg="StopPodSandbox for \"86c8014e2400986b752c3d7825a3b6d859509a55b288964aa2f2dbbd69ffd484\" returns successfully"
Mar 18 10:22:16 kind-worker containerd[110]: time="2025-03-18T10:22:16.701901088Z" level=info msg="RemoveContainer for \"62e04a72b1c5bb855056e55b44513a36a9f338baa5ee997b5ea20858b61fa058\""
Mar 18 10:22:16 kind-worker containerd[110]: time="2025-03-18T10:22:16.861494402Z" level=info msg="RemoveContainer for \"62e04a72b1c5bb855056e55b44513a36a9f338baa5ee997b5ea20858b61fa058\" returns successfully"
Mar 18 10:22:51 kind-worker containerd[110]: time="2025-03-18T10:22:51.262222376Z" level=info msg="StopPodSandbox for \"86c8014e2400986b752c3d7825a3b6d859509a55b288964aa2f2dbbd69ffd484\""
Mar 18 10:22:51 kind-worker containerd[110]: time="2025-03-18T10:22:51.286053498Z" level=info msg="TearDown network for sandbox \"86c8014e2400986b752c3d7825a3b6d859509a55b288964aa2f2dbbd69ffd484\" successfully"
Mar 18 10:22:51 kind-worker containerd[110]: time="2025-03-18T10:22:51.286271353Z" level=info msg="StopPodSandbox for \"86c8014e2400986b752c3d7825a3b6d859509a55b288964aa2f2dbbd69ffd484\" returns successfully"
Mar 18 10:22:51 kind-worker containerd[110]: time="2025-03-18T10:22:51.286858566Z" level=info msg="RemovePodSandbox for \"86c8014e2400986b752c3d7825a3b6d859509a55b288964aa2f2dbbd69ffd484\""
Mar 18 10:22:51 kind-worker containerd[110]: time="2025-03-18T10:22:51.287107572Z" level=info msg="Forcibly stopping sandbox \"86c8014e2400986b752c3d7825a3b6d859509a55b288964aa2f2dbbd69ffd484\""
Mar 18 10:22:51 kind-worker containerd[110]: time="2025-03-18T10:22:51.312465250Z" level=info msg="TearDown network for sandbox \"86c8014e2400986b752c3d7825a3b6d859509a55b288964aa2f2dbbd69ffd484\" successfully"
Mar 18 10:22:51 kind-worker containerd[110]: time="2025-03-18T10:22:51.416992958Z" level=warning msg="Failed to get podSandbox status for container event for sandboxID \"86c8014e2400986b752c3d7825a3b6d859509a55b288964aa2f2dbbd69ffd484\": an error occurred when try to find sandbox: not found. Sending the event with nil podSandboxStatus."
Mar 18 10:22:51 kind-worker containerd[110]: time="2025-03-18T10:22:51.417281145Z" level=info msg="RemovePodSandbox \"86c8014e2400986b752c3d7825a3b6d859509a55b288964aa2f2dbbd69ffd484\" returns successfully"
```
maybe logs like **failed to handle container TaskExit event container_id** indicate containerd had some issues stopping the container indeed, but I'm not sure how to read / interpret these logs. In any case, the Pod terminated, it just took longer that we expected.

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-03-18T11:30:27Z

> Or alternatively, maybe we should bump the resources in test-infra? I guess it could be justified given adding some more operators to the testing recently.

We didn't change tests behaviour neither it's related to anything Kueue controls...
I am leaning into this option, just like you have said, more operators, more tests, etc.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-18T11:35:44Z

I agree, I think we have exhausted options which are under Kueue control. At this point I see only two approaches:
1. increase timeouts to 1min30s
2. increase resources in test-infra

I'm leaning to 2. as well. We are spending too much time investigating the flakes. Since kubelet takes >1min to kill a pod it is a sign the system is under too much load imo.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-18T11:54:51Z

Using the monitoring in https://monitoring-eks.prow.k8s.io/d/96Q8oOOZk/builds?orgId=1&from=now-7d&to=now&var-org=kubernetes-sigs&var-repo=kueue&var-job=pull-kueue-test-e2e-main-1-31&var-build=All&refresh=30s we checked with @tenzen-y the resource usage during the build. 

First, you can find the JobID is `fd1a29d7-85bd-4f1b-b8a4-5c8758a91b03`, and this is present in [prowjob.json](https://storage.googleapis.com/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/4658/pull-kueue-test-e2e-main-1-31/1901938587444711424/prowjob.json)

Now, [focusing on the Job](https://monitoring-eks.prow.k8s.io/d/96Q8oOOZk/builds?orgId=1&from=1742292148654&to=1742294530878&var-org=kubernetes-sigs&var-repo=kueue&var-job=pull-kueue-test-e2e-main-1-31&var-build=All) we see: 

![Image](https://github.com/user-attachments/assets/f0bb5552-461d-4460-9972-de6469c4b1c9)

I think the timestamps are just shifted by 1h, as the Job started `"creationTimestamp": "2025-03-18T10:07:50Z",`, and the failure log indicates:`In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/pod_test.go:219 @ 03/18/25 10:22:06.676` aligning perfectly with the spike.

So, we got confirmation that the tests spike at 8 cpus, I think it is justified to bump to 10cpu in test-infra.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-18T11:57:17Z

Thank you for summarizing it, as we synced offline, we agree with increasing resources.

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-03-18T12:17:53Z

https://github.com/kubernetes/test-infra/pull/34529

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-19T08:10:40Z

/close
Doing reset of e2e-related flakes as agreed in https://github.com/kubernetes-sigs/kueue/issues/4674#issuecomment-2734095182.

The reason is that we recently bumped up the job resources, and it is expected to help for most of the flakes were attributed to long termination of a job. So, this way we can avoid people looking into an already solved problem.

For more details check the PR [kubernetes/test-infra#34529](https://github.com/kubernetes/test-infra/pull/34529) as discussed here: [#4669](https://github.com/kubernetes-sigs/kueue/issues/4669).

If the failure re-occurs feel free to re-open or open a new one.

Also, feel free to re-open if you have some evidence / hints that constrained resources is not the reason for the failure.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-03-19T08:10:45Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4669#issuecomment-2735669693):

>/close
>Doing reset of e2e-related flakes as agreed in https://github.com/kubernetes-sigs/kueue/issues/4674#issuecomment-2734095182.
>
>The reason is that we recently bumped up the job resources, and it is expected to help for most of the flakes were attributed to long termination of a job. So, this way we can avoid people looking into an already solved problem.
>
>For more details check the PR [kubernetes/test-infra#34529](https://github.com/kubernetes/test-infra/pull/34529) as discussed here: [#4669](https://github.com/kubernetes-sigs/kueue/issues/4669).
>
>If the failure re-occurs feel free to re-open or open a new one.
>
>Also, feel free to re-open if you have some evidence / hints that constrained resources is not the reason for the failure.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
