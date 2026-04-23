# Issue #3901: Flaky Test: TopologyAwareScheduling for StatefulSet when Creating a StatefulSet Should place pods based on the ranks-ordering

**Summary**: Flaky Test: TopologyAwareScheduling for StatefulSet when Creating a StatefulSet Should place pods based on the ranks-ordering

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3901

**Last updated**: 2025-01-30T15:39:48Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2024-12-23T07:07:23Z
- **Updated**: 2025-01-30T15:39:48Z
- **Closed**: 2025-01-30T15:39:46Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 6

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
Failed on "End To End TAS Suite: kindest/node:v1.31.1: [It] TopologyAwareScheduling for StatefulSet when Creating a StatefulSet Should place pods based on the ranks-ordering".

```shell
{Timed out after 45.000s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/tas/statefulset_test.go:94 with:
Expected
    <int32>: 2
to equal
    <int32>: 3 failed [FAILED] Timed out after 45.000s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/tas/statefulset_test.go:94 with:
Expected
    <int32>: 2
to equal
    <int32>: 3
In [It] at: /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/tas/statefulset_test.go:95 @ 12/20/24 04:52:06.225
}
```

**What you expected to happen**:
No errors.

**How to reproduce it (as minimally and precisely as possible)**:
https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-tas-e2e-main/1869966151665061888

<img width="1216" alt="Screenshot 2024-12-23 at 16 06 26" src="https://github.com/user-attachments/assets/2c0bc897-908d-4f19-b674-7846f6f31899" />

https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-tas-e2e-main/1870690934111342592

<img width="1389" alt="Screenshot 2024-12-23 at 16 09 46" src="https://github.com/user-attachments/assets/dbada589-09ff-4325-bfaa-dda3ae5d17b7" />

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-12-23T07:07:30Z

/kind flake

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-01-02T16:36:12Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-29T12:19:01Z

This looks very similar as https://github.com/kubernetes-sigs/kueue/issues/4056

From kube-scheduler logs we see it took very long to schedule sts-0 (after a couple of attempts) on kind-worker:

```
2024-12-20T04:51:19.752570988Z stderr F I1220 04:51:19.752136       1 schedule_one.go:314] "Successfully bound pod to node" pod="e2e-tas-pytorchjob-qbdbb/ranks-pytorch-worker-0" node="kind-worker" evaluatedNodes=9 feasibleNodes=1
2024-12-20T04:51:19.755504498Z stderr F I1220 04:51:19.753420       1 schedule_one.go:314] "Successfully bound pod to node" pod="e2e-tas-pytorchjob-qbdbb/ranks-pytorch-master-0" node="kind-worker" evaluatedNodes=9 feasibleNodes=1
2024-12-20T04:51:19.758923723Z stderr F I1220 04:51:19.758735       1 schedule_one.go:314] "Successfully bound pod to node" pod="e2e-tas-pytorchjob-qbdbb/ranks-pytorch-worker-2" node="kind-worker3" evaluatedNodes=9 feasibleNodes=1
2024-12-20T04:51:22.34747273Z stderr F I1220 04:51:22.347134       1 schedule_one.go:1055] "Unable to schedule pod; no fit; waiting" pod="e2e-tas-sts-fpmn5/sts-0" err="0/9 nodes are available: 1 Insufficient example.com/gpu, 1 node(s) had untolerated taint {node-role.kubernetes.io/control-plane: }, 7 node(s) didn't match Pod's node affinity/selector. preemption: 0/9 nodes are available: 1 No preemption victims found for incoming pod, 8 Preemption is not helpful for scheduling."
2024-12-20T04:51:23.559822035Z stderr F I1220 04:51:23.559606       1 schedule_one.go:1055] "Unable to schedule pod; no fit; waiting" pod="e2e-tas-sts-fpmn5/sts-0" err="0/9 nodes are available: 1 Insufficient example.com/gpu, 1 node(s) had untolerated taint {node-role.kubernetes.io/control-plane: }, 7 node(s) didn't match Pod's node affinity/selector. preemption: 0/9 nodes are available: 1 No preemption victims found for incoming pod, 8 Preemption is not helpful for scheduling."
2024-12-20T04:51:53.73463161Z stderr F I1220 04:51:53.734290       1 schedule_one.go:1055] "Unable to schedule pod; no fit; waiting" pod="e2e-tas-sts-fpmn5/sts-0" err="0/9 nodes are available: 1 Insufficient example.com/gpu, 1 node(s) had untolerated taint {node-role.kubernetes.io/control-plane: }, 7 node(s) didn't match Pod's node affinity/selector. preemption: 0/9 nodes are available: 1 No preemption victims found for incoming pod, 8 Preemption is not helpful for scheduling."
2024-12-20T04:51:57.976612319Z stderr F I1220 04:51:57.976422       1 schedule_one.go:314] "Successfully bound pod to node" pod="e2e-tas-sts-fpmn5/sts-0" node="kind-worker" evaluatedNodes=9 feasibleNodes=1
2024-12-20T04:52:00.251831538Z stderr F I1220 04:52:00.251579       1 schedule_one.go:314] "Successfully bound pod to node" pod="e2e-tas-sts-fpmn5/sts-1" node="kind-worker2" evaluatedNodes=9 feasibleNodes=1
2024-12-20T04:52:04.755951787Z stderr F I1220 04:52:04.755556       1 schedule_one.go:314] "Successfully bound pod to node" pod="e2e-tas-sts-fpmn5/sts-2" node="kind-worker3" evaluatedNodes=9 feasibleNodes=1
```
and it left very little time to schedule sts-2.

Now, the scheduling of sts-0 was blocked apparently by `ranks-pytorch-worker-0` which took long to terminate (or at least it seems so from kubelet logs we currently have):

```
Dec 20 04:51:19 kind-worker kubelet[240]: I1220 04:51:19.763925     240 reconciler_common.go:245] "operationExecutor.VerifyControllerAttachedVolume started for volume \"kube-api-access-chkkb\" (UniqueName: \"kubernetes.io/projected/db7f7520-c7b0-49bf-b701-51df87cb2f9c-kube-api-access-chkkb\") pod \"ranks-pytorch-master-0\" (UID: \"db7f7520-c7b0-49bf-b701-51df87cb2f9c\") " pod="e2e-tas-pytorchjob-qbdbb/ranks-pytorch-master-0"
Dec 20 04:51:19 kind-worker kubelet[240]: I1220 04:51:19.764095     240 reconciler_common.go:245] "operationExecutor.VerifyControllerAttachedVolume started for volume \"kube-api-access-8j7zc\" (UniqueName: \"kubernetes.io/projected/47d51763-7a7e-4457-88e7-a0851195e144-kube-api-access-8j7zc\") pod \"ranks-pytorch-worker-0\" (UID: \"47d51763-7a7e-4457-88e7-a0851195e144\") " pod="e2e-tas-pytorchjob-qbdbb/ranks-pytorch-worker-0"
Dec 20 04:51:20 kind-worker kubelet[240]: I1220 04:51:20.556682     240 kubelet_volumes.go:163] "Cleaned up orphaned pod volumes dir" podUID="e48fa20d-231b-4838-9826-068064b8f7c9" path="/var/lib/kubelet/pods/e48fa20d-231b-4838-9826-068064b8f7c9/volumes"
Dec 20 04:51:23 kind-worker kubelet[240]: I1220 04:51:23.167353     240 pod_startup_latency_tracker.go:104] "Observed pod startup duration" pod="e2e-tas-pytorchjob-qbdbb/ranks-pytorch-master-0" podStartSLOduration=4.004360562 podStartE2EDuration="5.167326465s" podCreationTimestamp="2024-12-20 04:51:18 +0000 UTC" firstStartedPulling="2024-12-20 04:51:20.646820401 +0000 UTC m=+218.276954529" lastFinishedPulling="2024-12-20 04:51:21.809786304 +0000 UTC m=+219.439920432" observedRunningTime="2024-12-20 04:51:23.154384213 +0000 UTC m=+220.784518381" watchObservedRunningTime="2024-12-20 04:51:23.167326465 +0000 UTC m=+220.797460613"
Dec 20 04:51:23 kind-worker kubelet[240]: I1220 04:51:23.589635     240 reconciler_common.go:159] "operationExecutor.UnmountVolume started for volume \"kube-api-access-chkkb\" (UniqueName: \"kubernetes.io/projected/db7f7520-c7b0-49bf-b701-51df87cb2f9c-kube-api-access-chkkb\") pod \"db7f7520-c7b0-49bf-b701-51df87cb2f9c\" (UID: \"db7f7520-c7b0-49bf-b701-51df87cb2f9c\") "
Dec 20 04:51:23 kind-worker kubelet[240]: I1220 04:51:23.593241     240 operation_generator.go:803] UnmountVolume.TearDown succeeded for volume "kubernetes.io/projected/db7f7520-c7b0-49bf-b701-51df87cb2f9c-kube-api-access-chkkb" (OuterVolumeSpecName: "kube-api-access-chkkb") pod "db7f7520-c7b0-49bf-b701-51df87cb2f9c" (UID: "db7f7520-c7b0-49bf-b701-51df87cb2f9c"). InnerVolumeSpecName "kube-api-access-chkkb". PluginName "kubernetes.io/projected", VolumeGidValue ""
Dec 20 04:51:23 kind-worker kubelet[240]: I1220 04:51:23.689782     240 reconciler_common.go:288] "Volume detached for volume \"kube-api-access-chkkb\" (UniqueName: \"kubernetes.io/projected/db7f7520-c7b0-49bf-b701-51df87cb2f9c-kube-api-access-chkkb\") on node \"kind-worker\" DevicePath \"\""
Dec 20 04:51:24 kind-worker kubelet[240]: I1220 04:51:24.147954     240 scope.go:117] "RemoveContainer" containerID="43692e40b6e68b4883e9d18dbc91466916d1a6be64eda0c29cf0db861663e002"
Dec 20 04:51:24 kind-worker kubelet[240]: I1220 04:51:24.152932     240 scope.go:117] "RemoveContainer" containerID="43692e40b6e68b4883e9d18dbc91466916d1a6be64eda0c29cf0db861663e002"
Dec 20 04:51:24 kind-worker kubelet[240]: E1220 04:51:24.153447     240 log.go:32] "ContainerStatus from runtime service failed" err="rpc error: code = NotFound desc = an error occurred when try to find container \"43692e40b6e68b4883e9d18dbc91466916d1a6be64eda0c29cf0db861663e002\": not found" containerID="43692e40b6e68b4883e9d18dbc91466916d1a6be64eda0c29cf0db861663e002"
Dec 20 04:51:24 kind-worker kubelet[240]: I1220 04:51:24.153501     240 pod_container_deletor.go:53] "DeleteContainer returned error" containerID={"Type":"containerd","ID":"43692e40b6e68b4883e9d18dbc91466916d1a6be64eda0c29cf0db861663e002"} err="failed to get container status \"43692e40b6e68b4883e9d18dbc91466916d1a6be64eda0c29cf0db861663e002\": rpc error: code = NotFound desc = an error occurred when try to find container \"43692e40b6e68b4883e9d18dbc91466916d1a6be64eda0c29cf0db861663e002\": not found"
Dec 20 04:51:24 kind-worker kubelet[240]: I1220 04:51:24.556603     240 kubelet_volumes.go:163] "Cleaned up orphaned pod volumes dir" podUID="db7f7520-c7b0-49bf-b701-51df87cb2f9c" path="/var/lib/kubelet/pods/db7f7520-c7b0-49bf-b701-51df87cb2f9c/volumes"
Dec 20 04:51:53 kind-worker kubelet[240]: I1220 04:51:53.589253     240 reconciler_common.go:159] "operationExecutor.UnmountVolume started for volume \"kube-api-access-8j7zc\" (UniqueName: \"kubernetes.io/projected/47d51763-7a7e-4457-88e7-a0851195e144-kube-api-access-8j7zc\") pod \"47d51763-7a7e-4457-88e7-a0851195e144\" (UID: \"47d51763-7a7e-4457-88e7-a0851195e144\") "
Dec 20 04:51:53 kind-worker kubelet[240]: I1220 04:51:53.592655     240 operation_generator.go:803] UnmountVolume.TearDown succeeded for volume "kubernetes.io/projected/47d51763-7a7e-4457-88e7-a0851195e144-kube-api-access-8j7zc" (OuterVolumeSpecName: "kube-api-access-8j7zc") pod "47d51763-7a7e-4457-88e7-a0851195e144" (UID: "47d51763-7a7e-4457-88e7-a0851195e144"). InnerVolumeSpecName "kube-api-access-8j7zc". PluginName "kubernetes.io/projected", VolumeGidValue ""
Dec 20 04:51:53 kind-worker kubelet[240]: I1220 04:51:53.690204     240 reconciler_common.go:288] "Volume detached for volume \"kube-api-access-8j7zc\" (UniqueName: \"kubernetes.io/projected/47d51763-7a7e-4457-88e7-a0851195e144-kube-api-access-
```

So I believe what could help also here:
1. improve kubelet logging to clearly see when the Pod transitions to Failed
2. wait for the Pods to be gone if AfterEach for the PyTorch tests (or any other e2e test in the suite) to improve debuggability
3. increase timeout to VeryLongTimeout (especially as STS needs to schedule 3 pods one by one)

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-01-29T13:09:07Z

I also found on the logs [ here](https://storage.googleapis.com/kubernetes-ci-logs/logs/periodic-kueue-test-tas-e2e-main/1869966151665061888/artifacts/run-test-tas-e2e-1.31.1/kind-worker4/pods/kueue-system_kueue-controller-manager-df7869fdb-ps5t7_74372daf-de53-428e-81b0-805b864cc151/manager/0.log):

```
2024-12-20T04:52:01.629896949Z stderr F 2024-12-20T04:52:01.629692026Z	ERROR	controller/controller.go:316	Reconciler error	{"controller": "tas-topology-controller", "controllerGroup": "kueue.x-k8s.io", "controllerKind": "Topology", "Topology": {"name":"datacenter"}, "namespace": "", "name": "datacenter", "reconcileID": "1c73ac45-46e9-4591-ae3e-59d810a4d286", "error": "topologies.kueue.x-k8s.io \"datacenter\" is forbidden: User \"system:serviceaccount:kueue-system:kueue-controller-manager\" cannot update resource \"topologies\" in API group \"kueue.x-k8s.io\" at the cluster scope"}
2024-12-20T04:52:01.629936239Z stderr F sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).reconcileHandler
2024-12-20T04:52:01.629940549Z stderr F 	/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:316
2024-12-20T04:52:01.629944459Z stderr F sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).processNextWorkItem
2024-12-20T04:52:01.629948009Z stderr F 	/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:263
2024-12-20T04:52:01.629951709Z stderr F sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).Start.func2.2
2024-12-20T04:52:01.629955079Z stderr F 	/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:224
```

This error should be resolved in https://github.com/kubernetes-sigs/kueue/pull/3910.

UPDATED: But I think it is not related to this issue.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-30T15:39:43Z

/close 
As in https://github.com/kubernetes-sigs/kueue/issues/4056#issuecomment-2624842571

There is a good chance https://github.com/kubernetes-sigs/kueue/pull/4094 fixes the issue already.  Let's re-open when it occurs again. 

In the meanwhile we can track the effort of increasing the log level in a dedicated issue, opened: https://github.com/kubernetes-sigs/kueue/issues/4111

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-01-30T15:39:47Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3901#issuecomment-2624843962):

>/close 
>As in https://github.com/kubernetes-sigs/kueue/issues/4056#issuecomment-2624842571
>
>There is a good chance https://github.com/kubernetes-sigs/kueue/pull/4094 fixes the issue already.  Let's re-open when it occurs again. 
>
>In the meanwhile we can track the effort of increasing the log level in a dedicated issue, opened: https://github.com/kubernetes-sigs/kueue/issues/4111


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
