# Issue #4626: Flaky Test: LeaderWorkerSet integration when LeaderWorkerSet created should allow to scale down LeaderReadyStartupPolicy

**Summary**: Flaky Test: LeaderWorkerSet integration when LeaderWorkerSet created should allow to scale down LeaderReadyStartupPolicy

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4626

**Last updated**: 2025-03-18T09:31:58Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-03-16T04:46:52Z
- **Updated**: 2025-03-18T09:31:58Z
- **Closed**: 2025-03-18T09:31:58Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 19

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

`End To End Suite: kindest/node:v1.32.0: [It] LeaderWorkerSet integration when LeaderWorkerSet created should allow to scale down LeaderReadyStartupPolicy` accidentally failed in CI

```shell
{Timed out after 45.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/leaderworkerset_test.go:409 with:
Expected
    <int32>: 2
to equal
    <int32>: 1 failed [FAILED] Timed out after 45.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/leaderworkerset_test.go:409 with:
Expected
    <int32>: 2
to equal
    <int32>: 1
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/leaderworkerset_test.go:418 @ 03/16/25 04:32:08.556

There were additional failures detected after the initial failure. These are visible in the timeline
}
```

**What you expected to happen**:

no errors

**How to reproduce it (as minimally and precisely as possible)**:

https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/4625/pull-kueue-test-e2e-main-1-32/1901125782999142400

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-16T04:47:01Z

/kind flake

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-17T08:42:07Z

I looked at the failure- the scale down test failed because the number of replicas didn't go down from 2 to 1 within 45s.

The LWS in question is in the lws-e2e-thznm namespace.

The kubelet logs:
```
Mar 16 04:31:21 kind-worker kubelet[202]: I0316 04:31:21.080604     202 kubelet.go:2474] "SyncLoop ADD" source="api" pods=["lws-e2e-thznm/lws-1"]
Mar 16 04:31:21 kind-worker kubelet[202]: I0316 04:31:21.081394     202 kubelet_pods.go:1833] "Generating pod status" podIsTerminal=false pod="lws-e2e-thznm/lws-1"
Mar 16 04:31:21 kind-worker kubelet[202]: I0316 04:31:21.082083     202 util.go:30] "No sandbox for pod can be found. Need to start a new one" pod="lws-e2e-thznm/lws-1"
Mar 16 04:31:21 kind-worker kubelet[202]: I0316 04:31:21.105677     202 volume_manager.go:404] "Waiting for volumes to attach and mount for pod" pod="lws-e2e-thznm/lws-1"
Mar 16 04:31:21 kind-worker kubelet[202]: I0316 04:31:21.135020     202 status_manager.go:911] "Patch status for pod" pod="lws-e2e-thznm/lws-1" podUID="4ba4f666-f410-4d32-a8c5-f961e3332096" patch="{\"metadata\":{\"uid\":\"4ba4f666-f410-4d32-a8c5-f961e3332096\"},\"status\":{\"$setElementOrder/conditions\":[{\"type\":\"PodReadyToStartContainers\"},{\"type\":\"Initialized\"},{\"type\":\"Ready\"},{\"type\":\"ContainersReady\"},{\"type\":\"PodScheduled\"}],\"conditions\":[{\"lastProbeTime\":null,\"lastTransitionTime\":\"2025-03-16T04:31:21Z\",\"status\":\"False\",\"type\":\"PodReadyToStartContainers\"},{\"lastProbeTime\":null,\"lastTransitionTime\":\"2025-03-16T04:31:21Z\",\"status\":\"True\",\"type\":\"Initialized\"},{\"lastProbeTime\":null,\"lastTransitionTime\":\"2025-03-16T04:31:21Z\",\"message\":\"containers with unready status: [c]\",\"reason\":\"ContainersNotReady\",\"status\":\"False\",\"type\":\"Ready\"},{\"lastProbeTime\":null,\"lastTransitionTime\":\"2025-03-16T04:31:21Z\",\"message\":\"containers with unready status: [c]\",\"reason\":\"ContainersNotReady\",\"status\":\"False\",\"type\":\"ContainersReady\"}],\"containerStatuses\":[{\"image\":\"registry.k8s.io/e2e-test-images/agnhost:2.53@sha256:99c6b4bb4a1e1df3f0b3752168c89358794d02258ebebc26bf21c29399011a85\",\"imageID\":\"\",\"lastState\":{},\"name\":\"c\",\"ready\":false,\"restartCount\":0,\"started\":false,\"state\":{\"waiting\":{\"reason\":\"ContainerCreating\"}},\"volumeMounts\":[{\"mountPath\":\"/var/run/secrets/kubernetes.io/serviceaccount\",\"name\":\"kube-api-access-znkgb\",\"readOnly\":true,\"recursiveReadOnly\":\"Disabled\"}]}],\"hostIP\":\"172.18.0.4\",\"hostIPs\":[{\"ip\":\"172.18.0.4\"}],\"startTime\":\"2025-03-16T04:31:21Z\"}}"
Mar 16 04:31:21 kind-worker kubelet[202]: I0316 04:31:21.135442     202 status_manager.go:920] "Status for pod updated successfully" pod="lws-e2e-thznm/lws-1" statusVersion=1 status={"phase":"Pending","conditions":[{"type":"PodReadyToStartContainers","status":"False","lastProbeTime":null,"lastTransitionTime":"2025-03-16T04:31:21Z"},{"type":"Initialized","status":"True","lastProbeTime":null,"lastTransitionTime":"2025-03-16T04:31:21Z"},{"type":"Ready","status":"False","lastProbeTime":null,"lastTransitionTime":"2025-03-16T04:31:21Z","reason":"ContainersNotReady","message":"containers with unready status: [c]"},{"type":"ContainersReady","status":"False","lastProbeTime":null,"lastTransitionTime":"2025-03-16T04:31:21Z","reason":"ContainersNotReady","message":"containers with unready status: [c]"},{"type":"PodScheduled","status":"True","lastProbeTime":null,"lastTransitionTime":"2025-03-16T04:31:21Z"}],"hostIP":"172.18.0.4","hostIPs":[{"ip":"172.18.0.4"}],"startTime":"2025-03-16T04:31:21Z","containerStatuses":[{"name":"c","state":{"waiting":{"reason":"ContainerCreating"}},"lastState":{},"ready":false,"restartCount":0,"image":"registry.k8s.io/e2e-test-images/agnhost:2.53@sha256:99c6b4bb4a1e1df3f0b3752168c89358794d02258ebebc26bf21c29399011a85","imageID":"","started":false,"volumeMounts":[{"name":"kube-api-access-znkgb","mountPath":"/var/run/secrets/kubernetes.io/serviceaccount","readOnly":true,"recursiveReadOnly":"Disabled"}]}],"qosClass":"Burstable"}
Mar 16 04:31:21 kind-worker kubelet[202]: I0316 04:31:21.226531     202 reconciler_common.go:251] "operationExecutor.VerifyControllerAttachedVolume started for volume \"kube-api-access-znkgb\" (UniqueName: \"kubernetes.io/projected/4ba4f666-f410-4d32-a8c5-f961e3332096-kube-api-access-znkgb\") pod \"lws-1\" (UID: \"4ba4f666-f410-4d32-a8c5-f961e3332096\") " pod="lws-e2e-thznm/lws-1"
Mar 16 04:31:21 kind-worker kubelet[202]: I0316 04:31:21.328148     202 reconciler_common.go:224] "operationExecutor.MountVolume started for volume \"kube-api-access-znkgb\" (UniqueName: \"kubernetes.io/projected/4ba4f666-f410-4d32-a8c5-f961e3332096-kube-api-access-znkgb\") pod \"lws-1\" (UID: \"4ba4f666-f410-4d32-a8c5-f961e3332096\") " pod="lws-e2e-thznm/lws-1"
Mar 16 04:31:21 kind-worker kubelet[202]: I0316 04:31:21.374447     202 operation_generator.go:614] "MountVolume.SetUp succeeded for volume \"kube-api-access-znkgb\" (UniqueName: \"kubernetes.io/projected/4ba4f666-f410-4d32-a8c5-f961e3332096-kube-api-access-znkgb\") pod \"lws-1\" (UID: \"4ba4f666-f410-4d32-a8c5-f961e3332096\") " pod="lws-e2e-thznm/lws-1"
Mar 16 04:31:21 kind-worker kubelet[202]: I0316 04:31:21.406515     202 volume_manager.go:440] "All volumes are attached and mounted for pod" pod="lws-e2e-thznm/lws-1"
Mar 16 04:31:21 kind-worker kubelet[202]: I0316 04:31:21.406865     202 util.go:30] "No sandbox for pod can be found. Need to start a new one" pod="lws-e2e-thznm/lws-1"
Mar 16 04:31:21 kind-worker kubelet[202]: I0316 04:31:21.407005     202 kuberuntime_manager.go:1122] "computePodActions got for pod" podActions="KillPod: true, CreateSandbox: true, UpdatePodResources: false, Attempt: 0, InitContainersToStart: [], ContainersToStart: [0], EphemeralContainersToStart: [],ContainersToUpdate: map[], ContainersToKill: map[]" pod="lws-e2e-thznm/lws-1"
Mar 16 04:31:21 kind-worker kubelet[202]: I0316 04:31:21.907013     202 kubelet_pods.go:276] "Creating hosts mount for container" pod="lws-e2e-thznm/lws-1" containerName="c" podIPs=["10.244.1.46"] path=true
Mar 16 04:31:21 kind-worker kubelet[202]: I0316 04:31:21.907975     202 event.go:389] "Event occurred" object="lws-e2e-thznm/lws-1" fieldPath="spec.containers{c}" kind="Pod" apiVersion="v1" type="Normal" reason="Pulled" message="Container image \"registry.k8s.io/e2e-test-images/agnhost:2.53@sha256:99c6b4bb4a1e1df3f0b3752168c89358794d02258ebebc26bf21c29399011a85\" already present on machine"
Mar 16 04:31:21 kind-worker kubelet[202]: I0316 04:31:21.967839     202 event.go:389] "Event occurred" object="lws-e2e-thznm/lws-1" fieldPath="spec.containers{c}" kind="Pod" apiVersion="v1" type="Normal" reason="Created" message="Created container: c"
Mar 16 04:31:22 kind-worker kubelet[202]: I0316 04:31:22.318990     202 event.go:389] "Event occurred" object="lws-e2e-thznm/lws-1" fieldPath="spec.containers{c}" kind="Pod" apiVersion="v1" type="Normal" reason="Started" message="Started container c"
Mar 16 04:31:22 kind-worker kubelet[202]: I0316 04:31:22.661747     202 kubelet.go:2506] "SyncLoop (PLEG): event for pod" pod="lws-e2e-thznm/lws-1" event={"ID":"4ba4f666-f410-4d32-a8c5-f961e3332096","Type":"ContainerStarted","Data":"0782dd0d297258a8f747621ef2b2e349c72bbede25c0d2740eb3eea125d0dbd7"}
Mar 16 04:31:22 kind-worker kubelet[202]: I0316 04:31:22.661920     202 kubelet.go:2506] "SyncLoop (PLEG): event for pod" pod="lws-e2e-thznm/lws-1" event={"ID":"4ba4f666-f410-4d32-a8c5-f961e3332096","Type":"ContainerStarted","Data":"f87c41877224033289de84a7c29c2d9d66f71ef7a88ec595780f882775ebc1d4"}
Mar 16 04:31:22 kind-worker kubelet[202]: I0316 04:31:22.662098     202 kubelet_pods.go:1833] "Generating pod status" podIsTerminal=false pod="lws-e2e-thznm/lws-1"
Mar 16 04:31:22 kind-worker kubelet[202]: I0316 04:31:22.662657     202 volume_manager.go:404] "Waiting for volumes to attach and mount for pod" pod="lws-e2e-thznm/lws-1"
Mar 16 04:31:22 kind-worker kubelet[202]: I0316 04:31:22.662871     202 volume_manager.go:440] "All volumes are attached and mounted for pod" pod="lws-e2e-thznm/lws-1"
Mar 16 04:31:22 kind-worker kubelet[202]: I0316 04:31:22.663065     202 kuberuntime_manager.go:1122] "computePodActions got for pod" podActions="KillPod: false, CreateSandbox: false, UpdatePodResources: false, Attempt: 0, InitContainersToStart: [], ContainersToStart: [], EphemeralContainersToStart: [],ContainersToUpdate: map[], ContainersToKill: map[]" pod="lws-e2e-thznm/lws-1"
Mar 16 04:31:22 kind-worker kubelet[202]: I0316 04:31:22.692124     202 status_manager.go:911] "Patch status for pod" pod="lws-e2e-thznm/lws-1" podUID="4ba4f666-f410-4d32-a8c5-f961e3332096" patch="{\"metadata\":{\"uid\":\"4ba4f666-f410-4d32-a8c5-f961e3332096\"},\"status\":{\"$setElementOrder/conditions\":[{\"type\":\"PodReadyToStartContainers\"},{\"type\":\"Initialized\"},{\"type\":\"Ready\"},{\"type\":\"ContainersReady\"},{\"type\":\"PodScheduled\"}],\"conditions\":[{\"lastTransitionTime\":\"2025-03-16T04:31:22Z\",\"status\":\"True\",\"type\":\"PodReadyToStartContainers\"},{\"lastTransitionTime\":\"2025-03-16T04:31:22Z\",\"message\":null,\"reason\":null,\"status\":\"True\",\"type\":\"Ready\"},{\"lastTransitionTime\":\"2025-03-16T04:31:22Z\",\"message\":null,\"reason\":null,\"status\":\"True\",\"type\":\"ContainersReady\"}],\"containerStatuses\":[{\"containerID\":\"containerd://0782dd0d297258a8f747621ef2b2e349c72bbede25c0d2740eb3eea125d0dbd7\",\"image\":\"registry.k8s.io/e2e-test-images/agnhost:2.53\",\"imageID\":\"docker.io/library/import-2025-03-16@sha256:b834a6ce4fdd44c6a61b08aad29a66af701a413fe3e41c7147d0786e10b0215e\",\"lastState\":{},\"name\":\"c\",\"ready\":true,\"restartCount\":0,\"started\":true,\"state\":{\"running\":{\"startedAt\":\"2025-03-16T04:31:22Z\"}},\"volumeMounts\":[{\"mountPath\":\"/var/run/secrets/kubernetes.io/serviceaccount\",\"name\":\"kube-api-access-znkgb\",\"readOnly\":true,\"recursiveReadOnly\":\"Disabled\"}]}],\"phase\":\"Running\",\"podIP\":\"10.244.1.46\",\"podIPs\":[{\"ip\":\"10.244.1.46\"}]}}"
Mar 16 04:31:22 kind-worker kubelet[202]: I0316 04:31:22.692563     202 status_manager.go:920] "Status for pod updated successfully" pod="lws-e2e-thznm/lws-1" statusVersion=2 status={"phase":"Running","conditions":[{"type":"PodReadyToStartContainers","status":"True","lastProbeTime":null,"lastTransitionTime":"2025-03-16T04:31:22Z"},{"type":"Initialized","status":"True","lastProbeTime":null,"lastTransitionTime":"2025-03-16T04:31:21Z"},{"type":"Ready","status":"True","lastProbeTime":null,"lastTransitionTime":"2025-03-16T04:31:22Z"},{"type":"ContainersReady","status":"True","lastProbeTime":null,"lastTransitionTime":"2025-03-16T04:31:22Z"},{"type":"PodScheduled","status":"True","lastProbeTime":null,"lastTransitionTime":"2025-03-16T04:31:21Z"}],"hostIP":"172.18.0.4","hostIPs":[{"ip":"172.18.0.4"}],"podIP":"10.244.1.46","podIPs":[{"ip":"10.244.1.46"}],"startTime":"2025-03-16T04:31:21Z","containerStatuses":[{"name":"c","state":{"running":{"startedAt":"2025-03-16T04:31:22Z"}},"lastState":{},"ready":true,"restartCount":0,"image":"registry.k8s.io/e2e-test-images/agnhost:2.53","imageID":"docker.io/library/import-2025-03-16@sha256:b834a6ce4fdd44c6a61b08aad29a66af701a413fe3e41c7147d0786e10b0215e","containerID":"containerd://0782dd0d297258a8f747621ef2b2e349c72bbede25c0d2740eb3eea125d0dbd7","started":true,"volumeMounts":[{"name":"kube-api-access-znkgb","mountPath":"/var/run/secrets/kubernetes.io/serviceaccount","readOnly":true,"recursiveReadOnly":"Disabled"}]}],"qosClass":"Burstable"}
Mar 16 04:31:22 kind-worker kubelet[202]: I0316 04:31:22.692818     202 pod_startup_latency_tracker.go:172] "Mark when the pod was running for the first time" pod="lws-e2e-thznm/lws-1" rv="3910"
Mar 16 04:31:22 kind-worker kubelet[202]: I0316 04:31:22.755080     202 pod_startup_latency_tracker.go:104] "Observed pod startup duration" pod="lws-e2e-thznm/lws-1" podStartSLOduration=2.755046846 podStartE2EDuration="2.755046846s" podCreationTimestamp="2025-03-16 04:31:20 +0000 UTC" firstStartedPulling="0001-01-01 00:00:00 +0000 UTC" lastFinishedPulling="0001-01-01 00:00:00 +0000 UTC" observedRunningTime="2025-03-16 04:31:22.692926465 +0000 UTC m=+270.504844009" watchObservedRunningTime="2025-03-16 04:31:22.755046846 +0000 UTC m=+270.566964380"
Mar 16 04:31:23 kind-worker kubelet[202]: I0316 04:31:23.611176     202 kubelet.go:2490] "SyncLoop DELETE" source="api" pods=["lws-e2e-thznm/lws-1"]
Mar 16 04:31:23 kind-worker kubelet[202]: I0316 04:31:23.611610     202 pod_workers.go:970] "Cancelling current pod sync" pod="lws-e2e-thznm/lws-1" podUID="4ba4f666-f410-4d32-a8c5-f961e3332096" workType="terminating"
Mar 16 04:31:23 kind-worker kubelet[202]: I0316 04:31:23.671276     202 kubelet_pods.go:1833] "Generating pod status" podIsTerminal=false pod="lws-e2e-thznm/lws-1"
Mar 16 04:31:23 kind-worker kubelet[202]: I0316 04:31:23.671860     202 kuberuntime_container.go:788] "Killing container with a grace period override" pod="lws-e2e-thznm/lws-1" podUID="4ba4f666-f410-4d32-a8c5-f961e3332096" containerName="c" containerID="containerd://0782dd0d297258a8f747621ef2b2e349c72bbede25c0d2740eb3eea125d0dbd7" gracePeriod=30
Mar 16 04:31:23 kind-worker kubelet[202]: I0316 04:31:23.671891     202 kuberuntime_container.go:809] "Killing container with a grace period" pod="lws-e2e-thznm/lws-1" podUID="4ba4f666-f410-4d32-a8c5-f961e3332096" containerName="c" containerID="containerd://0782dd0d297258a8f747621ef2b2e349c72bbede25c0d2740eb3eea125d0dbd7" gracePeriod=30
Mar 16 04:31:23 kind-worker kubelet[202]: I0316 04:31:23.677289     202 event.go:389] "Event occurred" object="lws-e2e-thznm/lws-1" fieldPath="spec.containers{c}" kind="Pod" apiVersion="v1" type="Normal" reason="Killing" message="Stopping container c"
Mar 16 04:31:23 kind-worker kubelet[202]: I0316 04:31:23.731009     202 status_manager.go:911] "Patch status for pod" pod="lws-e2e-thznm/lws-1" podUID="4ba4f666-f410-4d32-a8c5-f961e3332096" patch="{\"metadata\":{\"uid\":\"4ba4f666-f410-4d32-a8c5-f961e3332096\"}}"
Mar 16 04:31:23 kind-worker kubelet[202]: I0316 04:31:23.731385     202 status_manager.go:918] "Status for pod is up-to-date" pod="lws-e2e-thznm/lws-1" statusVersion=3
Mar 16 04:31:23 kind-worker kubelet[202]: I0316 04:31:23.731422     202 status_manager.go:976] "Delaying pod deletion as the phase is non-terminal" phase="Running" localPhase="Running" pod="lws-e2e-thznm/lws-1" podUID="4ba4f666-f410-4d32-a8c5-f961e3332096"
Mar 16 04:31:32 kind-worker kubelet[202]: I0316 04:31:32.658309     202 status_manager.go:976] "Delaying pod deletion as the phase is non-terminal" phase="Running" localPhase="Running" pod="lws-e2e-thznm/lws-1" podUID="4ba4f666-f410-4d32-a8c5-f961e3332096"
Mar 16 04:31:42 kind-worker kubelet[202]: I0316 04:31:42.648802     202 status_manager.go:976] "Delaying pod deletion as the phase is non-terminal" phase="Running" localPhase="Running" pod="lws-e2e-thznm/lws-1" podUID="4ba4f666-f410-4d32-a8c5-f961e3332096"
Mar 16 04:31:52 kind-worker kubelet[202]: I0316 04:31:52.648242     202 status_manager.go:976] "Delaying pod deletion as the phase is non-terminal" phase="Running" localPhase="Running" pod="lws-e2e-thznm/lws-1" podUID="4ba4f666-f410-4d32-a8c5-f961e3332096"
Mar 16 04:32:02 kind-worker kubelet[202]: I0316 04:32:02.649381     202 status_manager.go:976] "Delaying pod deletion as the phase is non-terminal" phase="Running" localPhase="Running" pod="lws-e2e-thznm/lws-1" podUID="4ba4f666-f410-4d32-a8c5-f961e3332096"
Mar 16 04:32:03 kind-worker kubelet[202]: I0316 04:32:03.751653     202 kuberuntime_container.go:818] "Container exited normally" pod="lws-e2e-thznm/lws-1" podUID="4ba4f666-f410-4d32-a8c5-f961e3332096" containerName="c" containerID="containerd://0782dd0d297258a8f747621ef2b2e349c72bbede25c0d2740eb3eea125d0dbd7"
Mar 16 04:32:03 kind-worker kubelet[202]: I0316 04:32:03.920395     202 kubelet.go:2506] "SyncLoop (PLEG): event for pod" pod="lws-e2e-thznm/lws-1" event={"ID":"4ba4f666-f410-4d32-a8c5-f961e3332096","Type":"ContainerDied","Data":"0782dd0d297258a8f747621ef2b2e349c72bbede25c0d2740eb3eea125d0dbd7"}
Mar 16 04:32:12 kind-worker kubelet[202]: I0316 04:32:12.648865     202 status_manager.go:976] "Delaying pod deletion as the phase is non-terminal" phase="Running" localPhase="Running" pod="lws-e2e-thznm/lws-1" podUID="4ba4f666-f410-4d32-a8c5-f961e3332096"
Mar 16 04:32:22 kind-worker kubelet[202]: I0316 04:32:22.648565     202 status_manager.go:976] "Delaying pod deletion as the phase is non-terminal" phase="Running" localPhase="Running" pod="lws-e2e-thznm/lws-1" podUID="4ba4f666-f410-4d32-a8c5-f961e3332096"
Mar 16 04:32:32 kind-worker kubelet[202]: I0316 04:32:32.648532     202 status_manager.go:976] "Delaying pod deletion as the phase is non-terminal" phase="Running" localPhase="Running" pod="lws-e2e-thznm/lws-1" podUID="4ba4f666-f410-4d32-a8c5-f961e3332096"
Mar 16 04:32:42 kind-worker kubelet[202]: I0316 04:32:42.649315     202 status_manager.go:976] "Delaying pod deletion as the phase is non-terminal" phase="Running" localPhase="Running" pod="lws-e2e-thznm/lws-1" podUID="4ba4f666-f410-4d32-a8c5-f961e3332096"
Mar 16 04:32:52 kind-worker kubelet[202]: I0316 04:32:52.649298     202 status_manager.go:976] "Delaying pod deletion as the phase is non-terminal" phase="Running" localPhase="Running" pod="lws-e2e-thznm/lws-1" podUID="4ba4f666-f410-4d32-a8c5-f961e3332096"
Mar 16 04:33:02 kind-worker kubelet[202]: I0316 04:33:02.649017     202 status_manager.go:976] "Delaying pod deletion as the phase is non-terminal" phase="Running" localPhase="Running" pod="lws-e2e-thznm/lws-1" podUID="4ba4f666-f410-4d32-a8c5-f961e3332096"
Mar 16 04:33:12 kind-worker kubelet[202]: I0316 04:33:12.648718     202 status_manager.go:976] "Delaying pod deletion as the phase is non-terminal" phase="Running" localPhase="Running" pod="lws-e2e-thznm/lws-1" podUID="4ba4f666-f410-4d32-a8c5-f961e3332096"
Mar 16 04:33:14 kind-worker kubelet[202]: I0316 04:33:14.647087     202 kubelet_pods.go:1833] "Generating pod status" podIsTerminal=true pod="lws-e2e-thznm/lws-1"
Mar 16 04:33:14 kind-worker kubelet[202]: I0316 04:33:14.647169     202 util.go:48] "No ready sandbox for pod can be found. Need to start a new one" pod="lws-e2e-thznm/lws-1"
Mar 16 04:33:14 kind-worker kubelet[202]: I0316 04:33:14.736045     202 status_manager.go:911] "Patch status for pod" pod="lws-e2e-thznm/lws-1" podUID="4ba4f666-f410-4d32-a8c5-f961e3332096" patch="{\"metadata\":{\"uid\":\"4ba4f666-f410-4d32-a8c5-f961e3332096\"},\"status\":{\"$setElementOrder/conditions\":[{\"type\":\"PodReadyToStartContainers\"},{\"type\":\"Initialized\"},{\"type\":\"Ready\"},{\"type\":\"ContainersReady\"},{\"type\":\"PodScheduled\"}],\"conditions\":[{\"lastTransitionTime\":\"2025-03-16T04:33:14Z\",\"status\":\"False\",\"type\":\"PodReadyToStartContainers\"},{\"reason\":\"PodCompleted\",\"type\":\"Initialized\"},{\"lastTransitionTime\":\"2025-03-16T04:33:14Z\",\"reason\":\"PodCompleted\",\"status\":\"False\",\"type\":\"Ready\"},{\"lastTransitionTime\":\"2025-03-16T04:33:14Z\",\"reason\":\"PodCompleted\",\"status\":\"False\",\"type\":\"ContainersReady\"}],\"containerStatuses\":[{\"containerID\":\"containerd://0782dd0d297258a8f747621ef2b2e349c72bbede25c0d2740eb3eea125d0dbd7\",\"image\":\"registry.k8s.io/e2e-test-images/agnhost:2.53\",\"imageID\":\"docker.io/library/import-2025-03-16@sha256:b834a6ce4fdd44c6a61b08aad29a66af701a413fe3e41c7147d0786e10b0215e\",\"lastState\":{},\"name\":\"c\",\"ready\":false,\"restartCount\":0,\"started\":false,\"state\":{\"terminated\":{\"containerID\":\"containerd://0782dd0d297258a8f747621ef2b2e349c72bbede25c0d2740eb3eea125d0dbd7\",\"exitCode\":0,\"finishedAt\":\"2025-03-16T04:31:23Z\",\"reason\":\"Completed\",\"startedAt\":\"2025-03-16T04:31:22Z\"}},\"volumeMounts\":[{\"mountPath\":\"/var/run/secrets/kubernetes.io/serviceaccount\",\"name\":\"kube-api-access-znkgb\",\"readOnly\":true,\"recursiveReadOnly\":\"Disabled\"}]}],\"phase\":\"Succeeded\"}}"
Mar 16 04:33:14 kind-worker kubelet[202]: I0316 04:33:14.736128     202 status_manager.go:920] "Status for pod updated successfully" pod="lws-e2e-thznm/lws-1" statusVersion=4 status={"phase":"Succeeded","conditions":[{"type":"PodReadyToStartContainers","status":"False","lastProbeTime":null,"lastTransitionTime":"2025-03-16T04:33:14Z"},{"type":"Initialized","status":"True","lastProbeTime":null,"lastTransitionTime":"2025-03-16T04:31:21Z","reason":"PodCompleted"},{"type":"Ready","status":"False","lastProbeTime":null,"lastTransitionTime":"2025-03-16T04:33:14Z","reason":"PodCompleted"},{"type":"ContainersReady","status":"False","lastProbeTime":null,"lastTransitionTime":"2025-03-16T04:33:14Z","reason":"PodCompleted"},{"type":"PodScheduled","status":"True","lastProbeTime":null,"lastTransitionTime":"2025-03-16T04:31:21Z"}],"hostIP":"172.18.0.4","hostIPs":[{"ip":"172.18.0.4"}],"podIP":"10.244.1.46","podIPs":[{"ip":"10.244.1.46"}],"startTime":"2025-03-16T04:31:21Z","containerStatuses":[{"name":"c","state":{"terminated":{"exitCode":0,"reason":"Completed","startedAt":"2025-03-16T04:31:22Z","finishedAt":"2025-03-16T04:31:23Z","containerID":"containerd://0782dd0d297258a8f747621ef2b2e349c72bbede25c0d2740eb3eea125d0dbd7"}},"lastState":{},"ready":false,"restartCount":0,"image":"registry.k8s.io/e2e-test-images/agnhost:2.53","imageID":"docker.io/library/import-2025-03-16@sha256:b834a6ce4fdd44c6a61b08aad29a66af701a413fe3e41c7147d0786e10b0215e","containerID":"containerd://0782dd0d297258a8f747621ef2b2e349c72bbede25c0d2740eb3eea125d0dbd7","started":false,"volumeMounts":[{"name":"kube-api-access-znkgb","mountPath":"/var/run/secrets/kubernetes.io/serviceaccount","readOnly":true,"recursiveReadOnly":"Disabled"}]}],"qosClass":"Burstable"}
Mar 16 04:33:15 kind-worker kubelet[202]: I0316 04:33:15.148257     202 kubelet.go:2506] "SyncLoop (PLEG): event for pod" pod="lws-e2e-thznm/lws-1" event={"ID":"4ba4f666-f410-4d32-a8c5-f961e3332096","Type":"ContainerDied","Data":"f87c41877224033289de84a7c29c2d9d66f71ef7a88ec595780f882775ebc1d4"}
Mar 16 04:33:15 kind-worker kubelet[202]: I0316 04:33:15.148290     202 kubelet_pods.go:1833] "Generating pod status" podIsTerminal=true pod="lws-e2e-thznm/lws-1"
Mar 16 04:33:15 kind-worker kubelet[202]: I0316 04:33:15.148478     202 util.go:48] "No ready sandbox for pod can be found. Need to start a new one" pod="lws-e2e-thznm/lws-1"
Mar 16 04:33:15 kind-worker kubelet[202]: I0316 04:33:15.148624     202 volume_manager.go:449] "Waiting for volumes to unmount for pod" pod="lws-e2e-thznm/lws-1"
Mar 16 04:33:15 kind-worker kubelet[202]: I0316 04:33:15.152425     202 status_manager.go:911] "Patch status for pod" pod="lws-e2e-thznm/lws-1" podUID="4ba4f666-f410-4d32-a8c5-f961e3332096" patch="{\"metadata\":{\"uid\":\"4ba4f666-f410-4d32-a8c5-f961e3332096\"}}"
Mar 16 04:33:15 kind-worker kubelet[202]: I0316 04:33:15.152479     202 status_manager.go:918] "Status for pod is up-to-date" pod="lws-e2e-thznm/lws-1" statusVersion=5
Mar 16 04:33:34 kind-worker kubelet[202]: I0316 04:33:34.049036     202 volume_manager.go:477] "All volumes are unmounted for pod" pod="lws-e2e-thznm/lws-1"
Mar 16 04:33:34 kind-worker kubelet[202]: I0316 04:33:34.049251     202 kubelet.go:2238] "Pod termination cleaned up volume paths" pod="lws-e2e-thznm/lws-1" podUID="4ba4f666-f410-4d32-a8c5-f961e3332096"
Mar 16 04:33:34 kind-worker kubelet[202]: I0316 04:33:34.094611     202 status_manager.go:911] "Patch status for pod" pod="lws-e2e-thznm/lws-1" podUID="4ba4f666-f410-4d32-a8c5-f961e3332096" patch="{\"metadata\":{\"uid\":\"4ba4f666-f410-4d32-a8c5-f961e3332096\"}}"
Mar 16 04:33:34 kind-worker kubelet[202]: I0316 04:33:34.094657     202 status_manager.go:918] "Status for pod is up-to-date" pod="lws-e2e-thznm/lws-1" statusVersion=6
Mar 16 04:33:34 kind-worker kubelet[202]: I0316 04:33:34.094680     202 status_manager.go:981] "The pod termination is finished as SyncTerminatedPod completes its execution" phase="Succeeded" localPhase="Succeeded" pod="lws-e2e-thznm/lws-1" podUID="4ba4f666-f410-4d32-a8c5-f961e3332096"
Mar 16 04:33:34 kind-worker kubelet[202]: I0316 04:33:34.126054     202 kubelet.go:2490] "SyncLoop DELETE" source="api" pods=["lws-e2e-thznm/lws-1"]
Mar 16 04:33:34 kind-worker kubelet[202]: I0316 04:33:34.142740     202 kubelet.go:2484] "SyncLoop REMOVE" source="api" pods=["lws-e2e-thznm/lws-1"]
Mar 16 04:33:34 kind-worker kubelet[202]: I0316 04:33:34.143928     202 kubelet.go:2322] "Pod has been deleted and must be killed" pod="lws-e2e-thznm/lws-1" podUID="4ba4f666-f410-4d32-a8c5-f961e3332096"
Mar 16 04:33:34 kind-worker kubelet[202]: I0316 04:33:34.143267     202 status_manager.go:949] "Pod fully terminated and removed from etcd" pod="lws-e2e-thznm/lws-1"
```
Key timeline: 
```
04:31:20.657 - LWS created / test starts
04:31:23.611 - scale down starts - DELETE request received by kubelet
04:32:08.556 - LongTimeout exceeded
04:33:14.736 - graceful termination completes as the Pod phase is Succeeded
```
Note that the failure is after we introduced waiting for deleting all pods in AfterEach: https://github.com/kubernetes-sigs/kueue/pull/4611, so it didn't happen due to pods from previous tests loading the cluster (which is great we did it).

The graceful termination took 1min 51s.

So, the remaining ideas I have:
1. increase the cpu for the problematic containers to 200m or even 500m if possible.
2. set gracePeriodTermination to 1s, as the tests don't assert how the Pod terminated
3. increase the timeout

cc @tenzen-y @mbobrovskyi @mszadkow

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-17T08:51:30Z

Oh I see this increase of CPU is already merged: https://github.com/kubernetes-sigs/kueue/pull/4627. This is great, maybe we will see these failures less often then, but I feel like 200m might still not be enough given the termination took nearly 2min in this case, but we can wait and see if this repeats.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-17T10:25:29Z

Ah it still happens: https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/4642/pull-kueue-test-e2e-main-1-30/1901574873466015744

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-17T11:07:57Z

> Ah it still happens: https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/4642/pull-kueue-test-e2e-main-1-30/1901574873466015744

All the pods were scheduled on kind-worker:
```
> cat scheduler.log | grep lws-e2e-bt54c | grep Success
2025-03-17T10:12:21.773520512Z stderr F I0317 10:12:21.773142       1 schedule_one.go:304] "Successfully bound pod to node" pod="lws-e2e-bt54c/lws-0" node="kind-worker" evaluatedNodes=3 feasibleNodes=1
2025-03-17T10:12:21.790983596Z stderr F I0317 10:12:21.790679       1 schedule_one.go:304] "Successfully bound pod to node" pod="lws-e2e-bt54c/lws-1" node="kind-worker" evaluatedNodes=3 feasibleNodes=1
2025-03-17T10:12:23.101886885Z stderr F I0317 10:12:23.101724       1 schedule_one.go:304] "Successfully bound pod to node" pod="lws-e2e-bt54c/lws-1-1" node="kind-worker" evaluatedNodes=3 feasibleNodes=1
2025-03-17T10:12:23.109690811Z stderr F I0317 10:12:23.109298       1 schedule_one.go:304] "Successfully bound pod to node" pod="lws-e2e-bt54c/lws-0-1" node="kind-worker" evaluatedNodes=3 feasibleNodes=1
2025-03-17T10:12:23.139494874Z stderr F I0317 10:12:23.139248       1 schedule_one.go:304] "Successfully bound pod to node" pod="lws-e2e-bt54c/lws-1-2" node="kind-worker" evaluatedNodes=3 feasibleNodes=1
2025-03-17T10:12:23.147068818Z stderr F I0317 10:12:23.146947       1 schedule_one.go:304] "Successfully bound pod to node" pod="lws-e2e-bt54c/lws-0-2" node="kind-worker" evaluatedNodes=3 feasibleNodes=1
```

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-17T11:15:18Z

Actually, this assert is a bit different, because it requires all 3 pods to be terminated within 45s. So, I think it is expected kubelet is expected to work more than when terminating a single pod.

Looking at the termination of `lws-e2e-bt54c/lws-0-1` on kind-worker (but other Pods also took long-ish):
```
Mar 17 10:12:23 kind-worker kubelet[247]: I0317 10:12:23.133334     247 status_manager.go:883] "Status for pod updated successfully" pod="lws-e2e-bt54c/lws-0-1" statusVersion=1 status={"phase":"Pending","conditions":[{"type":"PodReadyToStartContainers","status":"False","lastProbeTime":null,"lastTransitionTime":"2025-03-17T10:12:23Z"},{"type":"Initialized","status":"True","lastProbeTime":null,"lastTransitionTime":"2025-03-17T10:12:23Z"},{"type":"Ready","status":"False","lastProbeTime":null,"lastTransitionTime":"2025-03-17T10:12:23Z","reason":"ContainersNotReady","message":"containers with unready status: [c]"},{"type":"ContainersReady","status":"False","lastProbeTime":null,"lastTransitionTime":"2025-03-17T10:12:23Z","reason":"ContainersNotReady","message":"containers with unready status: [c]"},{"type":"PodScheduled","status":"True","lastProbeTime":null,"lastTransitionTime":"2025-03-17T10:12:23Z"}],"hostIP":"172.18.0.2","hostIPs":[{"ip":"172.18.0.2"}],"startTime":"2025-03-17T10:12:23Z","containerStatuses":[{"name":"c","state":{"waiting":{"reason":"ContainerCreating"}},"lastState":{},"ready":false,"restartCount":0,"image":"registry.k8s.io/e2e-test-images/agnhost:2.53@sha256:99c6b4bb4a1e1df3f0b3752168c89358794d02258ebebc26bf21c29399011a85","imageID":"","started":false}],"qosClass":"Burstable"}
Mar 17 10:12:25 kind-worker kubelet[247]: I0317 10:12:25.075254     247 status_manager.go:874] "Patch status for pod" pod="lws-e2e-bt54c/lws-0-2" podUID="d2bd8f17-5f5e-4eda-9654-2947e23cc6e7" patch="{\"metadata\":{\"uid\":\"d2bd8f17-5f5e-4eda-9654-2947e23cc6e7\"},\"status\":{\"$setElementOrder/conditions\":[{\"type\":\"PodReadyToStartContainers\"},{\"type\":\"Initialized\"},{\"type\":\"Ready\"},{\"type\":\"ContainersReady\"},{\"type\":\"PodScheduled\"}],\"conditions\":[{\"lastTransitionTime\":\"2025-03-17T10:12:25Z\",\"status\":\"True\",\"type\":\"PodReadyToStartContainers\"},{\"lastTransitionTime\":\"2025-03-17T10:12:25Z\",\"message\":null,\"reason\":null,\"status\":\"True\",\"type\":\"Ready\"},{\"lastTransitionTime\":\"2025-03-17T10:12:25Z\",\"message\":null,\"reason\":null,\"status\":\"True\",\"type\":\"ContainersReady\"}],\"containerStatuses\":[{\"containerID\":\"containerd://62fc0d94d0c7748b072c7b7208fb6faee1e22ec07a7497b88369ca3e2bdba27d\",\"image\":\"registry.k8s.io/e2e-test-images/agnhost:2.53\",\"imageID\":\"docker.io/library/import-2025-03-17@sha256:b834a6ce4fdd44c6a61b08aad29a66af701a413fe3e41c7147d0786e10b0215e\",\"lastState\":{},\"name\":\"c\",\"ready\":true,\"restartCount\":0,\"started\":true,\"state\":{\"running\":{\"startedAt\":\"2025-03-17T10:12:24Z\"}}}],\"phase\":\"Running\",\"podIP\":\"10.244.2.46\",\"podIPs\":[{\"ip\":\"10.244.2.46\"}]}}"
Mar 17 10:12:25 kind-worker kubelet[247]: I0317 10:12:25.480887     247 status_manager.go:874] "Patch status for pod" pod="lws-e2e-bt54c/lws-0-1" podUID="36a632b4-2b0a-485f-a3e4-9a91803b411c" patch="{\"metadata\":{\"uid\":\"36a632b4-2b0a-485f-a3e4-9a91803b411c\"},\"status\":{\"$setElementOrder/conditions\":[{\"type\":\"PodReadyToStartContainers\"},{\"type\":\"Initialized\"},{\"type\":\"Ready\"},{\"type\":\"ContainersReady\"},{\"type\":\"PodScheduled\"}],\"conditions\":[{\"lastTransitionTime\":\"2025-03-17T10:12:25Z\",\"status\":\"True\",\"type\":\"PodReadyToStartContainers\"},{\"lastTransitionTime\":\"2025-03-17T10:12:25Z\",\"message\":null,\"reason\":null,\"status\":\"True\",\"type\":\"Ready\"},{\"lastTransitionTime\":\"2025-03-17T10:12:25Z\",\"message\":null,\"reason\":null,\"status\":\"True\",\"type\":\"ContainersReady\"}],\"containerStatuses\":[{\"containerID\":\"containerd://4750b1ee9a74e91a64dfb3b0a8417077a68878a76e10569569f1002c2df3f827\",\"image\":\"registry.k8s.io/e2e-test-images/agnhost:2.53\",\"imageID\":\"docker.io/library/import-2025-03-17@sha256:b834a6ce4fdd44c6a61b08aad29a66af701a413fe3e41c7147d0786e10b0215e\",\"lastState\":{},\"name\":\"c\",\"ready\":true,\"restartCount\":0,\"started\":true,\"state\":{\"running\":{\"startedAt\":\"2025-03-17T10:12:24Z\"}}}],\"phase\":\"Running\",\"podIP\":\"10.244.2.44\",\"podIPs\":[{\"ip\":\"10.244.2.44\"}]}}"
Mar 17 10:12:25 kind-worker kubelet[247]: I0317 10:12:25.480983     247 status_manager.go:883] "Status for pod updated successfully" pod="lws-e2e-bt54c/lws-0-1" statusVersion=2 status={"phase":"Running","conditions":[{"type":"PodReadyToStartContainers","status":"True","lastProbeTime":null,"lastTransitionTime":"2025-03-17T10:12:25Z"},{"type":"Initialized","status":"True","lastProbeTime":null,"lastTransitionTime":"2025-03-17T10:12:23Z"},{"type":"Ready","status":"True","lastProbeTime":null,"lastTransitionTime":"2025-03-17T10:12:25Z"},{"type":"ContainersReady","status":"True","lastProbeTime":null,"lastTransitionTime":"2025-03-17T10:12:25Z"},{"type":"PodScheduled","status":"True","lastProbeTime":null,"lastTransitionTime":"2025-03-17T10:12:23Z"}],"hostIP":"172.18.0.2","hostIPs":[{"ip":"172.18.0.2"}],"podIP":"10.244.2.44","podIPs":[{"ip":"10.244.2.44"}],"startTime":"2025-03-17T10:12:23Z","containerStatuses":[{"name":"c","state":{"running":{"startedAt":"2025-03-17T10:12:24Z"}},"lastState":{},"ready":true,"restartCount":0,"image":"registry.k8s.io/e2e-test-images/agnhost:2.53","imageID":"docker.io/library/import-2025-03-17@sha256:b834a6ce4fdd44c6a61b08aad29a66af701a413fe3e41c7147d0786e10b0215e","containerID":"containerd://4750b1ee9a74e91a64dfb3b0a8417077a68878a76e10569569f1002c2df3f827","started":true}],"qosClass":"Burstable"}
Mar 17 10:12:26 kind-worker kubelet[247]: I0317 10:12:26.027958     247 status_manager.go:693] "Ignoring same status for pod" pod="lws-e2e-bt54c/lws-0-1" status={"phase":"Running","conditions":[{"type":"PodReadyToStartContainers","status":"True","lastProbeTime":null,"lastTransitionTime":"2025-03-17T10:12:25Z"},{"type":"Initialized","status":"True","lastProbeTime":null,"lastTransitionTime":"2025-03-17T10:12:23Z"},{"type":"Ready","status":"True","lastProbeTime":null,"lastTransitionTime":"2025-03-17T10:12:25Z"},{"type":"ContainersReady","status":"True","lastProbeTime":null,"lastTransitionTime":"2025-03-17T10:12:25Z"},{"type":"PodScheduled","status":"True","lastProbeTime":null,"lastTransitionTime":"2025-03-17T10:12:23Z"}],"hostIP":"172.18.0.2","hostIPs":[{"ip":"172.18.0.2"}],"podIP":"10.244.2.44","podIPs":[{"ip":"10.244.2.44"}],"startTime":"2025-03-17T10:12:23Z","containerStatuses":[{"name":"c","state":{"running":{"startedAt":"2025-03-17T10:12:24Z"}},"lastState":{},"ready":true,"restartCount":0,"image":"registry.k8s.io/e2e-test-images/agnhost:2.53","imageID":"docker.io/library/import-2025-03-17@sha256:b834a6ce4fdd44c6a61b08aad29a66af701a413fe3e41c7147d0786e10b0215e","containerID":"containerd://4750b1ee9a74e91a64dfb3b0a8417077a68878a76e10569569f1002c2df3f827","started":true}],"qosClass":"Burstable"}
Mar 17 10:13:18 kind-worker kubelet[247]: I0317 10:13:18.043798     247 status_manager.go:939] "Delaying pod deletion as the phase is non-terminal" phase="Running" localPhase="Running" pod="lws-e2e-bt54c/lws-0-1" podUID="36a632b4-2b0a-485f-a3e4-9a91803b411c"
Mar 17 10:13:18 kind-worker kubelet[247]: I0317 10:13:18.065597     247 status_manager.go:939] "Delaying pod deletion as the phase is non-terminal" phase="Running" localPhase="Running" pod="lws-e2e-bt54c/lws-0-2" podUID="d2bd8f17-5f5e-4eda-9654-2947e23cc6e7"
Mar 17 10:13:19 kind-worker kubelet[247]: I0317 10:13:19.878407     247 status_manager.go:939] "Delaying pod deletion as the phase is non-terminal" phase="Running" localPhase="Running" pod="lws-e2e-bt54c/lws-0-1" podUID="36a632b4-2b0a-485f-a3e4-9a91803b411c"
Mar 17 10:13:19 kind-worker kubelet[247]: I0317 10:13:19.878530     247 status_manager.go:939] "Delaying pod deletion as the phase is non-terminal" phase="Running" localPhase="Running" pod="lws-e2e-bt54c/lws-0-2" podUID="d2bd8f17-5f5e-4eda-9654-2947e23cc6e7"
Mar 17 10:13:29 kind-worker kubelet[247]: I0317 10:13:29.880225     247 status_manager.go:939] "Delaying pod deletion as the phase is non-terminal" phase="Running" localPhase="Running" pod="lws-e2e-bt54c/lws-0-1" podUID="36a632b4-2b0a-485f-a3e4-9a91803b411c"
Mar 17 10:13:29 kind-worker kubelet[247]: I0317 10:13:29.880300     247 status_manager.go:939] "Delaying pod deletion as the phase is non-terminal" phase="Running" localPhase="Running" pod="lws-e2e-bt54c/lws-0-2" podUID="d2bd8f17-5f5e-4eda-9654-2947e23cc6e7"
Mar 17 10:13:39 kind-worker kubelet[247]: I0317 10:13:39.873882     247 status_manager.go:939] "Delaying pod deletion as the phase is non-terminal" phase="Running" localPhase="Running" pod="lws-e2e-bt54c/lws-0-1" podUID="36a632b4-2b0a-485f-a3e4-9a91803b411c"
Mar 17 10:13:39 kind-worker kubelet[247]: I0317 10:13:39.874043     247 status_manager.go:939] "Delaying pod deletion as the phase is non-terminal" phase="Running" localPhase="Running" pod="lws-e2e-bt54c/lws-0-2" podUID="d2bd8f17-5f5e-4eda-9654-2947e23cc6e7"
Mar 17 10:13:49 kind-worker kubelet[247]: I0317 10:13:49.874491     247 status_manager.go:939] "Delaying pod deletion as the phase is non-terminal" phase="Running" localPhase="Running" pod="lws-e2e-bt54c/lws-0-1" podUID="36a632b4-2b0a-485f-a3e4-9a91803b411c"
Mar 17 10:13:49 kind-worker kubelet[247]: I0317 10:13:49.874609     247 status_manager.go:939] "Delaying pod deletion as the phase is non-terminal" phase="Running" localPhase="Running" pod="lws-e2e-bt54c/lws-0-2" podUID="d2bd8f17-5f5e-4eda-9654-2947e23cc6e7"
Mar 17 10:13:56 kind-worker kubelet[247]: I0317 10:13:56.128887     247 status_manager.go:874] "Patch status for pod" pod="lws-e2e-bt54c/lws-0-2" podUID="d2bd8f17-5f5e-4eda-9654-2947e23cc6e7" patch="{\"metadata\":{\"uid\":\"d2bd8f17-5f5e-4eda-9654-2947e23cc6e7\"},\"status\":{\"$setElementOrder/conditions\":[{\"type\":\"PodReadyToStartContainers\"},{\"type\":\"Initialized\"},{\"type\":\"Ready\"},{\"type\":\"ContainersReady\"},{\"type\":\"PodScheduled\"}],\"conditions\":[{\"lastTransitionTime\":\"2025-03-17T10:13:55Z\",\"status\":\"False\",\"type\":\"PodReadyToStartContainers\"},{\"reason\":\"PodCompleted\",\"type\":\"Initialized\"},{\"lastTransitionTime\":\"2025-03-17T10:13:55Z\",\"reason\":\"PodCompleted\",\"status\":\"False\",\"type\":\"Ready\"},{\"lastTransitionTime\":\"2025-03-17T10:13:55Z\",\"reason\":\"PodCompleted\",\"status\":\"False\",\"type\":\"ContainersReady\"}],\"containerStatuses\":[{\"containerID\":\"containerd://62fc0d94d0c7748b072c7b7208fb6faee1e22ec07a7497b88369ca3e2bdba27d\",\"image\":\"registry.k8s.io/e2e-test-images/agnhost:2.53\",\"imageID\":\"docker.io/library/import-2025-03-17@sha256:b834a6ce4fdd44c6a61b08aad29a66af701a413fe3e41c7147d0786e10b0215e\",\"lastState\":{},\"name\":\"c\",\"ready\":false,\"restartCount\":0,\"started\":false,\"state\":{\"terminated\":{\"containerID\":\"containerd://62fc0d94d0c7748b072c7b7208fb6faee1e22ec07a7497b88369ca3e2bdba27d\",\"exitCode\":0,\"finishedAt\":\"2025-03-17T10:13:18Z\",\"reason\":\"Completed\",\"startedAt\":\"2025-03-17T10:12:24Z\"}}}],\"phase\":\"Succeeded\",\"podIP\":null,\"podIPs\":null}}"
Mar 17 10:13:56 kind-worker kubelet[247]: I0317 10:13:56.542204     247 status_manager.go:944] "The pod termination is finished as SyncTerminatedPod completes its execution" phase="Succeeded" localPhase="Succeeded" pod="lws-e2e-bt54c/lws-0-2" podUID="d2bd8f17-5f5e-4eda-9654-2947e23cc6e7"
Mar 17 10:13:59 kind-worker kubelet[247]: I0317 10:13:59.874385     247 status_manager.go:939] "Delaying pod deletion as the phase is non-terminal" phase="Running" localPhase="Running" pod="lws-e2e-bt54c/lws-0-1" podUID="36a632b4-2b0a-485f-a3e4-9a91803b411c"
Mar 17 10:14:09 kind-worker kubelet[247]: I0317 10:14:09.874874     247 status_manager.go:939] "Delaying pod deletion as the phase is non-terminal" phase="Running" localPhase="Running" pod="lws-e2e-bt54c/lws-0-1" podUID="36a632b4-2b0a-485f-a3e4-9a91803b411c"
Mar 17 10:14:14 kind-worker kubelet[247]: I0317 10:14:14.009565     247 status_manager.go:874] "Patch status for pod" pod="lws-e2e-bt54c/lws-0-1" podUID="36a632b4-2b0a-485f-a3e4-9a91803b411c" patch="{\"metadata\":{\"uid\":\"36a632b4-2b0a-485f-a3e4-9a91803b411c\"},\"status\":{\"$setElementOrder/conditions\":[{\"type\":\"PodReadyToStartContainers\"},{\"type\":\"Initialized\"},{\"type\":\"Ready\"},{\"type\":\"ContainersReady\"},{\"type\":\"PodScheduled\"}],\"conditions\":[{\"lastTransitionTime\":\"2025-03-17T10:14:13Z\",\"status\":\"False\",\"type\":\"PodReadyToStartContainers\"},{\"reason\":\"PodCompleted\",\"type\":\"Initialized\"},{\"lastTransitionTime\":\"2025-03-17T10:14:13Z\",\"reason\":\"PodCompleted\",\"status\":\"False\",\"type\":\"Ready\"},{\"lastTransitionTime\":\"2025-03-17T10:14:13Z\",\"reason\":\"PodCompleted\",\"status\":\"False\",\"type\":\"ContainersReady\"}],\"containerStatuses\":[{\"containerID\":\"containerd://4750b1ee9a74e91a64dfb3b0a8417077a68878a76e10569569f1002c2df3f827\",\"image\":\"registry.k8s.io/e2e-test-images/agnhost:2.53\",\"imageID\":\"docker.io/library/import-2025-03-17@sha256:b834a6ce4fdd44c6a61b08aad29a66af701a413fe3e41c7147d0786e10b0215e\",\"lastState\":{},\"name\":\"c\",\"ready\":false,\"restartCount\":0,\"started\":false,\"state\":{\"terminated\":{\"containerID\":\"containerd://4750b1ee9a74e91a64dfb3b0a8417077a68878a76e10569569f1002c2df3f827\",\"exitCode\":0,\"finishedAt\":\"2025-03-17T10:13:18Z\",\"reason\":\"Completed\",\"startedAt\":\"2025-03-17T10:12:24Z\"}}}],\"phase\":\"Succeeded\",\"podIP\":null,\"podIPs\":null}}"
Mar 17 10:14:14 kind-worker kubelet[247]: I0317 10:14:14.009641     247 status_manager.go:883] "Status for pod updated successfully" pod="lws-e2e-bt54c/lws-0-1" statusVersion=4 status={"phase":"Succeeded","conditions":[{"type":"PodReadyToStartContainers","status":"False","lastProbeTime":null,"lastTransitionTime":"2025-03-17T10:14:13Z"},{"type":"Initialized","status":"True","lastProbeTime":null,"lastTransitionTime":"2025-03-17T10:12:23Z","reason":"PodCompleted"},{"type":"Ready","status":"False","lastProbeTime":null,"lastTransitionTime":"2025-03-17T10:14:13Z","reason":"PodCompleted"},{"type":"ContainersReady","status":"False","lastProbeTime":null,"lastTransitionTime":"2025-03-17T10:14:13Z","reason":"PodCompleted"},{"type":"PodScheduled","status":"True","lastProbeTime":null,"lastTransitionTime":"2025-03-17T10:12:23Z"}],"hostIP":"172.18.0.2","hostIPs":[{"ip":"172.18.0.2"}],"startTime":"2025-03-17T10:12:23Z","containerStatuses":[{"name":"c","state":{"terminated":{"exitCode":0,"reason":"Completed","startedAt":"2025-03-17T10:12:24Z","finishedAt":"2025-03-17T10:13:18Z","containerID":"containerd://4750b1ee9a74e91a64dfb3b0a8417077a68878a76e10569569f1002c2df3f827"}},"lastState":{},"ready":false,"restartCount":0,"image":"registry.k8s.io/e2e-test-images/agnhost:2.53","imageID":"docker.io/library/import-2025-03-17@sha256:b834a6ce4fdd44c6a61b08aad29a66af701a413fe3e41c7147d0786e10b0215e","containerID":"containerd://4750b1ee9a74e91a64dfb3b0a8417077a68878a76e10569569f1002c2df3f827","started":false}],"qosClass":"Burstable"}
Mar 17 10:14:14 kind-worker kubelet[247]: I0317 10:14:14.468765     247 status_manager.go:883] "Status for pod updated successfully" pod="lws-e2e-bt54c/lws-0-1" statusVersion=5 status={"phase":"Succeeded","conditions":[{"type":"PodReadyToStartContainers","status":"False","lastProbeTime":null,"lastTransitionTime":"2025-03-17T10:14:13Z"},{"type":"Initialized","status":"True","lastProbeTime":null,"lastTransitionTime":"2025-03-17T10:12:23Z","reason":"PodCompleted"},{"type":"Ready","status":"False","lastProbeTime":null,"lastTransitionTime":"2025-03-17T10:14:13Z","reason":"PodCompleted"},{"type":"ContainersReady","status":"False","lastProbeTime":null,"lastTransitionTime":"2025-03-17T10:14:13Z","reason":"PodCompleted"},{"type":"PodScheduled","status":"True","lastProbeTime":null,"lastTransitionTime":"2025-03-17T10:12:23Z"}],"hostIP":"172.18.0.2","hostIPs":[{"ip":"172.18.0.2"}],"podIP":"10.244.2.44","podIPs":[{"ip":"10.244.2.44"}],"startTime":"2025-03-17T10:12:23Z","containerStatuses":[{"name":"c","state":{"terminated":{"exitCode":0,"reason":"Completed","startedAt":"2025-03-17T10:12:24Z","finishedAt":"2025-03-17T10:13:18Z","containerID":"containerd://4750b1ee9a74e91a64dfb3b0a8417077a68878a76e10569569f1002c2df3f827"}},"lastState":{},"ready":false,"restartCount":0,"image":"registry.k8s.io/e2e-test-images/agnhost:2.53","imageID":"docker.io/library/import-2025-03-17@sha256:b834a6ce4fdd44c6a61b08aad29a66af701a413fe3e41c7147d0786e10b0215e","containerID":"containerd://4750b1ee9a74e91a64dfb3b0a8417077a68878a76e10569569f1002c2df3f827","started":false}],"qosClass":"Burstable"}
Mar 17 10:14:14 kind-worker kubelet[247]: I0317 10:14:14.472989     247 status_manager.go:944] "The pod termination is finished as SyncTerminatedPod completes its execution" phase="Succeeded" localPhase="Succeeded" pod="lws-e2e-bt54c/lws-0-1" podUID="36a632b4-2b0a-485f-a3e4-9a91803b411c"
```
So, DELETE was at `10:13:18`, and Succeeded phase was at `10:14:14`, i.e. 56s.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-17T11:15:57Z

We specified only CPU in LWS E2E. So, what about adding memory requests and limits as well?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-17T11:24:14Z

yes, we only assigned CPU, we should also probably set the memory. However, I think it will not help here, because the Pods don't seem to be memory-heavy. I think about two approaches:
1. increase CPU yet to 300m by default, as 56s is already close to 45s - previously we were observing >2min terminations
2. use 3*LongTimeout for this specific assert, because it actually requires 3 pods, not just one to terminate

I'm leaning to do both, WDYT @mbobrovskyi @tenzen-y ?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-17T11:27:36Z

> yes, we only assigned CPU, we should also probably set the memory. However, I think it will not help here, because the Pods don't seem to be memory-heavy. I think about two approaches:
> 
> 1. increase CPU yet to 300m by default, as 56s is already close to 45s - previously we were observing >2min terminations
> 2. use 3*LongTimeout for this specific assert, because it actually requires 3 pods, not just one to terminate
> 
> I'm leaning to do both, WDYT [@mbobrovskyi](https://github.com/mbobrovskyi) [@tenzen-y](https://github.com/tenzen-y) ?

If we take 2. we want to use SUM(Longtimeout, GracefulTerminationSeconds) instead of 3 x LongTimeout to avoid increasing timeout everywhere.
Any thoughts?

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-03-17T11:32:05Z

I think we should set terminationGracePeriodSeconds=1 everywhere to avoid waiting for this duration.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-17T11:34:43Z

I'm ok with that, we just need to be careful to check if the test doesn't assert on the end state of the Pods. Maybe some tests expect the pods to end successfully. If they don't, I'm fine with setting `terminationGracePeriodSeconds=1`.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-17T11:35:27Z

@mbobrovskyi can you please open the PR?

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-03-17T11:36:29Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-17T12:30:44Z

Actually, we cannot always just blindly use `terminationGracePeriodSeconds=1`. For example this test failed recently:
https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/4648/pull-kueue-test-e2e-main-1-32/1901605023159160832
```
{Timed out after 45.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/jobset_test.go:107 with:
Expected object to be comparable, diff:   (*v1.Condition)(
- 	nil,
+ 	s"&Condition{Type:Finished,Status:True,ObservedGeneration:0,LastTransitionTime:0001-01-01 00:00:00 +0000 UTC,Reason:Succeeded,Message:jobset completed successfully,}",
  )
 failed [FAILED] Timed out after 45.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/jobset_test.go:107 with:
Expected object to be comparable, diff:   (*v1.Condition)(
- 	nil,
+ 	s"&Condition{Type:Finished,Status:True,ObservedGeneration:0,LastTransitionTime:0001-01-01 00:00:00 +0000 UTC,Reason:Succeeded,Message:jobset completed successfully,}",
  )
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/jobset_test.go:113 @ 03/17/25 12:12:27.713
}
```
And the test assumes the JobSet completes successfully (See [code](https://github.com/kubernetes-sigs/kueue/blob/main/test/e2e/singlecluster/jobset_test.go#L104-L113)), so with `terminationGracePeriodSeconds=1` it would not. 

Unfortunately the test already is using 500m.  So, we would either need to relax the test, or we also need another approach for such cases. 

Maybe for such tests (assuming termination of multiple Pods we use VeryLongTimeout=5min, or DoubleLongTimeout=1min30s. Note that this test requires terminating 4 pods. WDYT @tenzen-y @mbobrovskyi ?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-17T12:32:50Z

Opened dedicated issue: https://github.com/kubernetes-sigs/kueue/issues/4651

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-03-17T14:16:10Z

> Actually, we cannot always just blindly use terminationGracePeriodSeconds=1. For example this test failed recently:
https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/4648/pull-kueue-test-e2e-main-1-32/1901605023159160832

I think this is a different issue and not related to it. We need to set `terminationGracePeriodSeconds = 1` for `BehaviorWaitForDeletion` and `BehaviorWaitForDeletionFailOnExit`. But here, we are using `BehaviorExitFast`, which simply stops the pod after running.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-03-17T14:37:52Z

/assign @mszadkow

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-03-17T14:38:16Z

/unassign

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-17T14:43:51Z

> I think this is a different issue and not related to it. We need to set terminationGracePeriodSeconds = 1 for BehaviorWaitForDeletion and BehaviorWaitForDeletionFailOnExit

Agree

> But here, we are using BehaviorExitFast, which simply stops the pod after running.

Yeah, we can solve it separately. Still for `BehaviorExitFast` we probably need longer timeout for a small number of tests.
