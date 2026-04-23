# Issue #4525: Flaky E2E Test: TopologyAwareScheduling when Creating a JobSet requesting TAS should admit a [Pod|PodGroup|JobSet] via TAS

**Summary**: Flaky E2E Test: TopologyAwareScheduling when Creating a JobSet requesting TAS should admit a [Pod|PodGroup|JobSet] via TAS

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4525

**Last updated**: 2025-03-19T08:13:09Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-03-07T20:43:09Z
- **Updated**: 2025-03-19T08:13:09Z
- **Closed**: 2025-03-19T08:13:07Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 12

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
The following cases failed in unrelated branch:

- `End To End Suite: kindest/node:v1.31.0: [It] TopologyAwareScheduling when Creating a JobSet requesting TAS should admit a JobSet via TAS`

```shell
{Timed out after 45.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/tas_test.go:279 with:
Expected
    <[]v1.Condition | len:2, cap:2>: [
        {
            Type: "QuotaReserved",
            Status: "True",
            ObservedGeneration: 1,
            LastTransitionTime: {
                Time: 2025-03-07T20:28:51Z,
            },
            Reason: "QuotaReserved",
            Message: "Quota reserved in ClusterQueue cluster-queue",
        },
        {
            Type: "Admitted",
            Status: "True",
            ObservedGeneration: 1,
            LastTransitionTime: {
                Time: 2025-03-07T20:28:51Z,
            },
            Reason: "Admitted",
            Message: "The workload is admitted",
        },
    ]
to have condition type Finished and status True failed [FAILED] Timed out after 45.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/tas_test.go:279 with:
Expected
    <[]v1.Condition | len:2, cap:2>: [
        {
            Type: "QuotaReserved",
            Status: "True",
            ObservedGeneration: 1,
            LastTransitionTime: {
                Time: 2025-03-07T20:28:51Z,
            },
            Reason: "QuotaReserved",
            Message: "Quota reserved in ClusterQueue cluster-queue",
        },
        {
            Type: "Admitted",
            Status: "True",
            ObservedGeneration: 1,
            LastTransitionTime: {
                Time: 2025-03-07T20:28:51Z,
            },
            Reason: "Admitted",
            Message: "The workload is admitted",
        },
    ]
to have condition type Finished and status True
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/tas_test.go:280 @ 03/07/25 20:29:36.691
}
```

- `End To End Suite: kindest/node:v1.31.0: [It] TopologyAwareScheduling when Creating a Pod requesting TAS should admit a single Pod via TAS`

```shell
{Timed out after 46.203s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/tas_test.go:381 with:
Expected
    <[]v1.Condition | len:2, cap:2>: [
        {
            Type: "QuotaReserved",
            Status: "True",
            ObservedGeneration: 1,
            LastTransitionTime: {
                Time: 2025-03-07T20:29:41Z,
            },
            Reason: "QuotaReserved",
            Message: "Quota reserved in ClusterQueue cluster-queue",
        },
        {
            Type: "Admitted",
            Status: "True",
            ObservedGeneration: 1,
            LastTransitionTime: {
                Time: 2025-03-07T20:29:41Z,
            },
            Reason: "Admitted",
            Message: "The workload is admitted",
        },
    ]
to have condition type Finished and status True failed [FAILED] Timed out after 46.203s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/tas_test.go:381 with:
Expected
    <[]v1.Condition | len:2, cap:2>: [
        {
            Type: "QuotaReserved",
            Status: "True",
            ObservedGeneration: 1,
            LastTransitionTime: {
                Time: 2025-03-07T20:29:41Z,
            },
            Reason: "QuotaReserved",
            Message: "Quota reserved in ClusterQueue cluster-queue",
        },
        {
            Type: "Admitted",
            Status: "True",
            ObservedGeneration: 1,
            LastTransitionTime: {
                Time: 2025-03-07T20:29:41Z,
            },
            Reason: "Admitted",
            Message: "The workload is admitted",
        },
    ]
to have condition type Finished and status True
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/tas_test.go:382 @ 03/07/25 20:30:29.397
}
```

- `End To End Suite: kindest/node:v1.31.0: [It] TopologyAwareScheduling when Creating a Pod requesting TAS should admit a Pod group via TAS`

```shell
{Timed out after 45.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/tas_test.go:446 with:
Expected
    <[]v1.Condition | len:2, cap:2>: [
        {
            Type: "QuotaReserved",
            Status: "True",
            ObservedGeneration: 1,
            LastTransitionTime: {
                Time: 2025-03-07T20:30:33Z,
            },
            Reason: "QuotaReserved",
            Message: "Quota reserved in ClusterQueue cluster-queue",
        },
        {
            Type: "Admitted",
            Status: "True",
            ObservedGeneration: 1,
            LastTransitionTime: {
                Time: 2025-03-07T20:30:33Z,
            },
            Reason: "Admitted",
            Message: "The workload is admitted",
        },
    ]
to have condition type Finished and status True failed [FAILED] Timed out after 45.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/tas_test.go:446 with:
Expected
    <[]v1.Condition | len:2, cap:2>: [
        {
            Type: "QuotaReserved",
            Status: "True",
            ObservedGeneration: 1,
            LastTransitionTime: {
                Time: 2025-03-07T20:30:33Z,
            },
            Reason: "QuotaReserved",
            Message: "Quota reserved in ClusterQueue cluster-queue",
        },
        {
            Type: "Admitted",
            Status: "True",
            ObservedGeneration: 1,
            LastTransitionTime: {
                Time: 2025-03-07T20:30:33Z,
            },
            Reason: "Admitted",
            Message: "The workload is admitted",
        },
    ]
to have condition type Finished and status True
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/tas_test.go:447 @ 03/07/25 20:31:19.631
}
```

**What you expected to happen**:
No errors

**How to reproduce it (as minimally and precisely as possible)**:

https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/4511/pull-kueue-test-e2e-main-1-31/1898105306647367680

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-16T11:09:43Z

The same failure happened in periodic Jobs: https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-main-1-29/1901206729471823872


<img width="1479" alt="Image" src="https://github.com/user-attachments/assets/d2b891f2-a66f-4789-bd0a-5a37cce44c3a" />

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-17T10:55:51Z

Ok, I looked into this flake too. The first failure corresponds to JobSet in namespace `e2e-tas-54snf`. Looking into kubelet logs:
```
> cat kubelet.log | grep e2e-tas-54snf | grep -e ADD -e Running 
Mar 07 20:28:52 kind-worker kubelet[253]: I0307 20:28:52.861505     253 kubelet.go:2407] "SyncLoop ADD" source="api" pods=["e2e-tas-54snf/test-jobset-rj2-0-0-d8d8s"]
Mar 07 20:28:52 kind-worker kubelet[253]: I0307 20:28:52.872149     253 kubelet.go:2407] "SyncLoop ADD" source="api" pods=["e2e-tas-54snf/test-jobset-rj1-0-0-pcc5k"]
Mar 07 20:28:56 kind-worker kubelet[253]: I0307 20:28:56.283584     253 status_manager.go:872] "Patch status for pod" pod="e2e-tas-54snf/test-jobset-rj2-0-0-d8d8s" podUID="9f5dfc2c-2121-48b7-abfb-42c5f779fdc5" patch="{\"metadata\":{\"uid\":\"9f5dfc2c-2121-48b7-abfb-42c5f779fdc5\"},\"status\":{\"$setElementOrder/conditions\":[{\"type\":\"PodReadyToStartContainers\"},{\"type\":\"Initialized\"},{\"type\":\"Ready\"},{\"type\":\"ContainersReady\"},{\"type\":\"PodScheduled\"}],\"conditions\":[{\"lastTransitionTime\":\"2025-03-07T20:28:56Z\",\"status\":\"True\",\"type\":\"PodReadyToStartContainers\"},{\"lastTransitionTime\":\"2025-03-07T20:28:56Z\",\"message\":null,\"reason\":null,\"status\":\"True\",\"type\":\"Ready\"},{\"lastTransitionTime\":\"2025-03-07T20:28:56Z\",\"message\":null,\"reason\":null,\"status\":\"True\",\"type\":\"ContainersReady\"}],\"containerStatuses\":[{\"containerID\":\"containerd://eb7da3031e930098f8dfe254b44502645cebda26560988f155747ad3ce219802\",\"image\":\"registry.k8s.io/e2e-test-images/agnhost:2.53\",\"imageID\":\"docker.io/library/import-2025-03-07@sha256:b834a6ce4fdd44c6a61b08aad29a66af701a413fe3e41c7147d0786e10b0215e\",\"lastState\":{},\"name\":\"c\",\"ready\":true,\"restartCount\":0,\"started\":true,\"state\":{\"running\":{\"startedAt\":\"2025-03-07T20:28:55Z\"}},\"volumeMounts\":[{\"mountPath\":\"/var/run/secrets/kubernetes.io/serviceaccount\",\"name\":\"kube-api-access-8svfm\",\"readOnly\":true,\"recursiveReadOnly\":\"Disabled\"}]}],\"phase\":\"Running\",\"podIP\":\"10.244.2.20\",\"podIPs\":[{\"ip\":\"10.244.2.20\"}]}}"
Mar 07 20:28:56 kind-worker kubelet[253]: I0307 20:28:56.283742     253 status_manager.go:881] "Status for pod updated successfully" pod="e2e-tas-54snf/test-jobset-rj2-0-0-d8d8s" statusVersion=2 status={"phase":"Running","conditions":[{"type":"PodReadyToStartContainers","status":"True","lastProbeTime":null,"lastTransitionTime":"2025-03-07T20:28:56Z"},{"type":"Initialized","status":"True","lastProbeTime":null,"lastTransitionTime":"2025-03-07T20:28:52Z"},{"type":"Ready","status":"True","lastProbeTime":null,"lastTransitionTime":"2025-03-07T20:28:56Z"},{"type":"ContainersReady","status":"True","lastProbeTime":null,"lastTransitionTime":"2025-03-07T20:28:56Z"},{"type":"PodScheduled","status":"True","lastProbeTime":null,"lastTransitionTime":"2025-03-07T20:28:52Z"}],"hostIP":"172.18.0.4","hostIPs":[{"ip":"172.18.0.4"}],"podIP":"10.244.2.20","podIPs":[{"ip":"10.244.2.20"}],"startTime":"2025-03-07T20:28:52Z","containerStatuses":[{"name":"c","state":{"running":{"startedAt":"2025-03-07T20:28:55Z"}},"lastState":{},"ready":true,"restartCount":0,"image":"registry.k8s.io/e2e-test-images/agnhost:2.53","imageID":"docker.io/library/import-2025-03-07@sha256:b834a6ce4fdd44c6a61b08aad29a66af701a413fe3e41c7147d0786e10b0215e","containerID":"containerd://eb7da3031e930098f8dfe254b44502645cebda26560988f155747ad3ce219802","started":true,"volumeMounts":[{"name":"kube-api-access-8svfm","mountPath":"/var/run/secrets/kubernetes.io/serviceaccount","readOnly":true,"recursiveReadOnly":"Disabled"}]}],"qosClass":"Burstable"}
Mar 07 20:28:56 kind-worker kubelet[253]: I0307 20:28:56.403395     253 status_manager.go:872] "Patch status for pod" pod="e2e-tas-54snf/test-jobset-rj1-0-0-pcc5k" podUID="0d8ccfd6-6cf7-4e27-a31f-9f789c71d2da" patch="{\"metadata\":{\"uid\":\"0d8ccfd6-6cf7-4e27-a31f-9f789c71d2da\"},\"status\":{\"$setElementOrder/conditions\":[{\"type\":\"PodReadyToStartContainers\"},{\"type\":\"Initialized\"},{\"type\":\"Ready\"},{\"type\":\"ContainersReady\"},{\"type\":\"PodScheduled\"}],\"conditions\":[{\"lastTransitionTime\":\"2025-03-07T20:28:56Z\",\"status\":\"True\",\"type\":\"PodReadyToStartContainers\"},{\"lastTransitionTime\":\"2025-03-07T20:28:56Z\",\"message\":null,\"reason\":null,\"status\":\"True\",\"type\":\"Ready\"},{\"lastTransitionTime\":\"2025-03-07T20:28:56Z\",\"message\":null,\"reason\":null,\"status\":\"True\",\"type\":\"ContainersReady\"}],\"containerStatuses\":[{\"containerID\":\"containerd://cc23d0385ca627e88a6101180b6a73be4c0a6d100b8b9878670c0e1b294cdfd2\",\"image\":\"registry.k8s.io/e2e-test-images/agnhost:2.53\",\"imageID\":\"docker.io/library/import-2025-03-07@sha256:b834a6ce4fdd44c6a61b08aad29a66af701a413fe3e41c7147d0786e10b0215e\",\"lastState\":{},\"name\":\"c\",\"ready\":true,\"restartCount\":0,\"started\":true,\"state\":{\"running\":{\"startedAt\":\"2025-03-07T20:28:55Z\"}},\"volumeMounts\":[{\"mountPath\":\"/var/run/secrets/kubernetes.io/serviceaccount\",\"name\":\"kube-api-access-tt2qh\",\"readOnly\":true,\"recursiveReadOnly\":\"Disabled\"}]}],\"phase\":\"Running\",\"podIP\":\"10.244.2.21\",\"podIPs\":[{\"ip\":\"10.244.2.21\"}]}}"
Mar 07 20:28:56 kind-worker kubelet[253]: I0307 20:28:56.404719     253 status_manager.go:881] "Status for pod updated successfully" pod="e2e-tas-54snf/test-jobset-rj1-0-0-pcc5k" statusVersion=2 status={"phase":"Running","conditions":[{"type":"PodReadyToStartContainers","status":"True","lastProbeTime":null,"lastTransitionTime":"2025-03-07T20:28:56Z"},{"type":"Initialized","status":"True","lastProbeTime":null,"lastTransitionTime":"2025-03-07T20:28:52Z"},{"type":"Ready","status":"True","lastProbeTime":null,"lastTransitionTime":"2025-03-07T20:28:56Z"},{"type":"ContainersReady","status":"True","lastProbeTime":null,"lastTransitionTime":"2025-03-07T20:28:56Z"},{"type":"PodScheduled","status":"True","lastProbeTime":null,"lastTransitionTime":"2025-03-07T20:28:52Z"}],"hostIP":"172.18.0.4","hostIPs":[{"ip":"172.18.0.4"}],"podIP":"10.244.2.21","podIPs":[{"ip":"10.244.2.21"}],"startTime":"2025-03-07T20:28:52Z","containerStatuses":[{"name":"c","state":{"running":{"startedAt":"2025-03-07T20:28:55Z"}},"lastState":{},"ready":true,"restartCount":0,"image":"registry.k8s.io/e2e-test-images/agnhost:2.53","imageID":"docker.io/library/import-2025-03-07@sha256:b834a6ce4fdd44c6a61b08aad29a66af701a413fe3e41c7147d0786e10b0215e","containerID":"containerd://cc23d0385ca627e88a6101180b6a73be4c0a6d100b8b9878670c0e1b294cdfd2","started":true,"volumeMounts":[{"name":"kube-api-access-tt2qh","mountPath":"/var/run/secrets/kubernetes.io/serviceaccount","readOnly":true,"recursiveReadOnly":"Disabled"}]}],"qosClass":"Burstable"}
Mar 07 20:28:56 kind-worker kubelet[253]: I0307 20:28:56.407344     253 pod_startup_latency_tracker.go:104] "Observed pod startup duration" pod="e2e-tas-54snf/test-jobset-rj2-0-0-d8d8s" podStartSLOduration=5.407312819 podStartE2EDuration="5.407312819s" podCreationTimestamp="2025-03-07 20:28:51 +0000 UTC" firstStartedPulling="0001-01-01 00:00:00 +0000 UTC" lastFinishedPulling="0001-01-01 00:00:00 +0000 UTC" observedRunningTime="2025-03-07 20:28:56.283954195 +0000 UTC m=+258.943716690" watchObservedRunningTime="2025-03-07 20:28:56.407312819 +0000 UTC m=+259.067075334"
Mar 07 20:28:56 kind-worker kubelet[253]: I0307 20:28:56.408499     253 pod_startup_latency_tracker.go:104] "Observed pod startup duration" pod="e2e-tas-54snf/test-jobset-rj1-0-0-pcc5k" podStartSLOduration=5.408482972 podStartE2EDuration="5.408482972s" podCreationTimestamp="2025-03-07 20:28:51 +0000 UTC" firstStartedPulling="0001-01-01 00:00:00 +0000 UTC" lastFinishedPulling="0001-01-01 00:00:00 +0000 UTC" observedRunningTime="2025-03-07 20:28:56.407017996 +0000 UTC m=+259.066780521" watchObservedRunningTime="2025-03-07 20:28:56.408482972 +0000 UTC m=+259.068245487"
Mar 07 20:28:57 kind-worker kubelet[253]: I0307 20:28:57.220141     253 status_manager.go:691] "Ignoring same status for pod" pod="e2e-tas-54snf/test-jobset-rj1-0-0-pcc5k" status={"phase":"Running","conditions":[{"type":"PodReadyToStartContainers","status":"True","lastProbeTime":null,"lastTransitionTime":"2025-03-07T20:28:56Z"},{"type":"Initialized","status":"True","lastProbeTime":null,"lastTransitionTime":"2025-03-07T20:28:52Z"},{"type":"Ready","status":"True","lastProbeTime":null,"lastTransitionTime":"2025-03-07T20:28:56Z"},{"type":"ContainersReady","status":"True","lastProbeTime":null,"lastTransitionTime":"2025-03-07T20:28:56Z"},{"type":"PodScheduled","status":"True","lastProbeTime":null,"lastTransitionTime":"2025-03-07T20:28:52Z"}],"hostIP":"172.18.0.4","hostIPs":[{"ip":"172.18.0.4"}],"podIP":"10.244.2.21","podIPs":[{"ip":"10.244.2.21"}],"startTime":"2025-03-07T20:28:52Z","containerStatuses":[{"name":"c","state":{"running":{"startedAt":"2025-03-07T20:28:55Z"}},"lastState":{},"ready":true,"restartCount":0,"image":"registry.k8s.io/e2e-test-images/agnhost:2.53","imageID":"docker.io/library/import-2025-03-07@sha256:b834a6ce4fdd44c6a61b08aad29a66af701a413fe3e41c7147d0786e10b0215e","containerID":"containerd://cc23d0385ca627e88a6101180b6a73be4c0a6d100b8b9878670c0e1b294cdfd2","started":true,"volumeMounts":[{"name":"kube-api-access-tt2qh","mountPath":"/var/run/secrets/kubernetes.io/serviceaccount","readOnly":true,"recursiveReadOnly":"Disabled"}]}],"qosClass":"Burstable"}
Mar 07 20:28:57 kind-worker kubelet[253]: I0307 20:28:57.222448     253 status_manager.go:691] "Ignoring same status for pod" pod="e2e-tas-54snf/test-jobset-rj2-0-0-d8d8s" status={"phase":"Running","conditions":[{"type":"PodReadyToStartContainers","status":"True","lastProbeTime":null,"lastTransitionTime":"2025-03-07T20:28:56Z"},{"type":"Initialized","status":"True","lastProbeTime":null,"lastTransitionTime":"2025-03-07T20:28:52Z"},{"type":"Ready","status":"True","lastProbeTime":null,"lastTransitionTime":"2025-03-07T20:28:56Z"},{"type":"ContainersReady","status":"True","lastProbeTime":null,"lastTransitionTime":"2025-03-07T20:28:56Z"},{"type":"PodScheduled","status":"True","lastProbeTime":null,"lastTransitionTime":"2025-03-07T20:28:52Z"}],"hostIP":"172.18.0.4","hostIPs":[{"ip":"172.18.0.4"}],"podIP":"10.244.2.20","podIPs":[{"ip":"10.244.2.20"}],"startTime":"2025-03-07T20:28:52Z","containerStatuses":[{"name":"c","state":{"running":{"startedAt":"2025-03-07T20:28:55Z"}},"lastState":{},"ready":true,"restartCount":0,"image":"registry.k8s.io/e2e-test-images/agnhost:2.53","imageID":"docker.io/library/import-2025-03-07@sha256:b834a6ce4fdd44c6a61b08aad29a66af701a413fe3e41c7147d0786e10b0215e","containerID":"containerd://eb7da3031e930098f8dfe254b44502645cebda26560988f155747ad3ce219802","started":true,"volumeMounts":[{"name":"kube-api-access-8svfm","mountPath":"/var/run/secrets/kubernetes.io/serviceaccount","readOnly":true,"recursiveReadOnly":"Disabled"}]}],"qosClass":"Burstable"}
Mar 07 20:29:37 kind-worker kubelet[253]: I0307 20:29:37.125490     253 status_manager.go:937] "Delaying pod deletion as the phase is non-terminal" phase="Running" localPhase="Running" pod="e2e-tas-54snf/test-jobset-rj1-0-0-pcc5k" podUID="0d8ccfd6-6cf7-4e27-a31f-9f789c71d2da"
Mar 07 20:29:37 kind-worker kubelet[253]: I0307 20:29:37.565906     253 kubelet.go:2407] "SyncLoop ADD" source="api" pods=["e2e-tas-54snf/test-jobset-rj1-0-0-chvdh"]
```
We can see the container didn't stop within 45s. 

Extending the grep (not requiring Running) we see the Pod terminated gracefully at `20:29:45`, so after 53s:

```
Mar 07 20:29:45 kind-worker kubelet[253]: I0307 20:29:45.955725     253 kuberuntime_container.go:817] "Container exited normally" pod="e2e-tas-54snf/test-jobset-rj1-0-0-pcc5k" podUID="0d8ccfd6-6cf7-4e27-a31f-9f789c71d2da" containerName="c" containerID="containerd://cc23d0385ca627e88a6101180b6a73be4c0a6d100b8b9878670c0e1b294cdfd2"
```

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-17T10:56:50Z

cc @tenzen-y @mbobrovskyi @mszadkow seems like most of the flakes currently are due to long graceful termination of Pods. Maybe for TAS it is more likely as we also started to run the Ray operator there, which is heavy and takes the node resources.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-17T11:20:33Z

> cc [@tenzen-y](https://github.com/tenzen-y) [@mbobrovskyi](https://github.com/mbobrovskyi) [@mszadkow](https://github.com/mszadkow) seems like most of the flakes currently are due to long graceful termination of Pods. Maybe for TAS it is more likely as we also started to run the Ray operator there, which is heavy and takes the node resources.

IIUC, we were considering leveraging terminationGracePeriodSeconds. Could we see the result if we apply it to all?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-17T11:29:05Z

> IIUC, we were considering leveraging terminationGracePeriodSeconds. Could we see the result if we apply it to all?

Well, it is not so easy as the flakes are mostly reproducible only on CI, so we need to merge it first.

I think this is likely to help, and we already use it in some tests. The only downside is that then the end state of the pod might be 0 or 137 (after sigkill), but we don't assert on the end result for the Pods in most cases anyway. So, I'm fine to set `terminationGracePeriodSeconds=1` for tests where we don't assert the end state of the pod.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-17T11:30:27Z

> > IIUC, we were considering leveraging terminationGracePeriodSeconds. Could we see the result if we apply it to all?
> 
> Well, it is not so easy as the flakes are mostly reproducible only on CI, so we need to merge it first.
> 
> I think this is likely to help, and we already use it in some tests. The only downside is that then the end state of the pod might be 0 or 137 (after sigkill), but we don't assert on the end result for the Pods in most cases anyway. So, I'm fine to set `terminationGracePeriodSeconds=1` for tests where we don't assert the end state of the pod.

SGTM

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-03-17T12:49:26Z

/assign

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-03-17T15:48:19Z

Hmm, there is little we can do for JobSet as `terminationGracePeriodSeconds` is already set by default to 0...
Also all containers in this test suite (test/e2e/singlecluster/tas_test.go) are "exiting fast", meaning they go straight to finished state, but sure maybe adding `terminationGracePeriodSeconds` to pod and job could help

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-17T16:01:53Z

> Hmm, there is little we can do for JobSet as terminationGracePeriodSeconds is already set by default to 0...

Can you provide reference for that? I'm surprised since our pods complete with Succeeded phase. Sending SIGKILL means 137 exit code, unless I'm missing something.

However, as mentioned in the  [comment](https://github.com/kubernetes-sigs/kueue/issues/4626#issuecomment-2729681268)  (and discussion around) I would not use sigkill if we use `BehaviorExitFast`.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-17T16:02:59Z

Since the JobSet only creates 2 pods I think we can start by bumping 200m to 500m.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-19T08:13:03Z

/close
Doing reset of e2e-related flakes as agreed in https://github.com/kubernetes-sigs/kueue/issues/4674#issuecomment-2734095182.

The reason is that we recently bumped up the job resources, and it is expected to help for most of the flakes were attributed to long termination of a job. So, this way we can avoid people looking into an already solved problem.

For more details check the PR [kubernetes/test-infra#34529](https://github.com/kubernetes/test-infra/pull/34529) as discussed here: [#4669](https://github.com/kubernetes-sigs/kueue/issues/4669).

If the failure re-occurs feel free to re-open or open a new one.

Also, feel free to re-open if you have some evidence / hints that constrained resources is not the reason for the failure.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-03-19T08:13:08Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4525#issuecomment-2735675701):

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
