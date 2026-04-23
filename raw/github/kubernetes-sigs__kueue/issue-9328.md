# Issue #9328: [flaky test] Kueue when Creating a Job With Queueing Should partially admit the Job if configured and not fully fits

**Summary**: [flaky test] Kueue when Creating a Job With Queueing Should partially admit the Job if configured and not fully fits

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9328

**Last updated**: 2026-02-17T18:19:38Z

---

## Metadata

- **State**: open
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-02-17T17:53:48Z
- **Updated**: 2026-02-17T18:19:38Z
- **Closed**: —
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 4

## Description

<!--
Please use this template for reporting flaky tests.
Links to specific failures in Prow are appreciated.
-->

**Which test is flaking?**:
Kueue when Creating a Job With Queueing Should partially admit the Job if configured and not fully fits
**Link to failed CI job or steps to reproduce locally**:
https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/9325/pull-kueue-test-e2e-release-0-15-1-34/2023807744179441664
**Failure message or logs**:
```
End To End Suite: kindest/node:v1.34.0: [It] Kueue when Creating a Job With Queueing Should partially admit the Job if configured and not fully fits expand_less	47s
{Timed out after 45.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/e2e_test.go:400 with:
Expected
    <[]v1.Condition | len:2, cap:2>: [
        {
            Type: "QuotaReserved",
            Status: "True",
            ObservedGeneration: 1,
            LastTransitionTime: {
                Time: 2026-02-17T17:29:32Z,
            },
            Reason: "QuotaReserved",
            Message: "Quota reserved in ClusterQueue cluster-queue-e2e-tv92f",
        },
        {
            Type: "Admitted",
            Status: "True",
            ObservedGeneration: 1,
            LastTransitionTime: {
                Time: 2026-02-17T17:29:32Z,
            },
            Reason: "Admitted",
            Message: "The workload is admitted",
        },
    ]
to have condition type Finished and status True failed [FAILED] Timed out after 45.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/e2e_test.go:400 with:
Expected
    <[]v1.Condition | len:2, cap:2>: [
        {
            Type: "QuotaReserved",
            Status: "True",
            ObservedGeneration: 1,
            LastTransitionTime: {
                Time: 2026-02-17T17:29:32Z,
            },
            Reason: "QuotaReserved",
            Message: "Quota reserved in ClusterQueue cluster-queue-e2e-tv92f",
        },
        {
            Type: "Admitted",
            Status: "True",
            ObservedGeneration: 1,
            LastTransitionTime: {
                Time: 2026-02-17T17:29:32Z,
            },
            Reason: "Admitted",
            Message: "The workload is admitted",
        },
    ]
to have condition type Finished and status True
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/e2e_test.go:401 @ 02/17/26 17:30:17.675
}
```

**Anything else we need to know?**:

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-17T18:01:18Z

All 4 Pods were scheduled to `kind-worker` in the span of 5s, from [scheduler logs](https://storage.googleapis.com/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/9325/pull-kueue-test-e2e-release-0-15-1-34/2023807744179441664/artifacts/run-test-e2e-singlecluster-1.34.0/kind-control-plane/pods/kube-system_kube-scheduler-kind-control-plane_14095e8558fd689c940f507d032d4780/kube-scheduler/0.log)

```
2026-02-17T17:29:32.515637578Z stderr F I0217 17:29:32.514999       1 schedule_one.go:346] "Successfully bound pod to node" pod="e2e-tv92f/job-rmbzg" node="kind-worker" evaluatedNodes=3 feasibleNodes=1
2026-02-17T17:29:32.541234011Z stderr F I0217 17:29:32.541121       1 schedule_one.go:346] "Successfully bound pod to node" pod="e2e-tv92f/job-bh6rh" node="kind-worker" evaluatedNodes=3 feasibleNodes=1
2026-02-17T17:29:37.048737888Z stderr F I0217 17:29:37.048259       1 schedule_one.go:346] "Successfully bound pod to node" pod="e2e-tv92f/job-zvmdh" node="kind-worker" evaluatedNodes=3 feasibleNodes=1
2026-02-17T17:29:37.086585679Z stderr F I0217 17:29:37.086409       1 schedule_one.go:346] "Successfully bound pod to node" pod="e2e-tv92f/job-sgsdx" node="kind-worker" evaluatedNodes=3 feasibleNodes=1
```

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-17T18:05:59Z

This is unexpected I think but the one of the Pods failed, based on [kubelet logs](https://storage.googleapis.com/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/9325/pull-kueue-test-e2e-release-0-15-1-34/2023807744179441664/artifacts/run-test-e2e-singlecluster-1.34.0/kind-worker/kubelet.log) `e2e-tv92f/job-zvmdh`:

```
Feb 17 17:30:09 kind-worker kubelet[232]: I0217 17:30:09.701475     232 status_manager.go:848] "Ignoring same status for pod" pod="e2e-tv92f/job-zvmdh" status={"observedGeneration":1,"phase":"Failed","conditions":[{"type":"PodReadyToStartContainers","observedGeneration":1,"status":"True","lastProbeTime":null,"lastTransitionTime":"2026-02-17T17:30:08Z"},{"type":"Initialized","observedGeneration":1,"status":"True","lastProbeTime":null,"lastTransitionTime":"2026-02-17T17:29:37Z"},{"type":"Ready","observedGeneration":1,"status":"False","lastProbeTime":null,"lastTransitionTime":"2026-02-17T17:29:37Z","reason":"PodFailed"},{"type":"ContainersReady","observedGeneration":1,"status":"False","lastProbeTime":null,"lastTransitionTime":"2026-02-17T17:29:37Z","reason":"PodFailed"},{"type":"PodScheduled","observedGeneration":1,"status":"True","lastProbeTime":null,"lastTransitionTime":"2026-02-17T17:29:37Z"}],"hostIP":"172.18.0.2","hostIPs":[{"ip":"172.18.0.2"}],"podIP":"10.244.2.77","podIPs":[{"ip":"10.244.2.77"}],"startTime":"2026-02-17T17:29:37Z","containerStatuses":[{"name":"c","state":{"terminated":{"exitCode":128,"reason":"StartError","message":"failed to create containerd task: failed to create shim task: failed to start io pipe copy: unable to copy pipes: containerd-shim: opening w/o fifo \"/run/containerd/io.containerd.grpc.v1.cri/containers/00498b3fed0360310f38eeaa92cdbfc11ccd99d49a1b5ad9e04221df45c1e8d3/io/2120232854/00498b3fed0360310f38eeaa92cdbfc11ccd99d49a1b5ad9e04221df45c1e8d3-stderr\" failed: context deadline exceeded","startedAt":"1970-01-01T00:00:00Z","finishedAt":"2026-02-17T17:30:08Z","containerID":"containerd://00498b3fed0360310f38eeaa92cdbfc11ccd99d49a1b5ad9e04221df45c1e8d3"}},"lastState":{},"ready":false,"restartCount":0,"image":"registry.k8s.io/e2e-test-images/agnhost:2.59","imageID":"sha256:90625afcd0c7ba09e0c28d4ba6b945e8cba1ab4a236d76a6dc604d4e0c6e4f2a","containerID":"containerd://00498b3fed0360310f38eeaa92cdbfc11ccd99d49a1b5ad9e04221df45c1e8d3","started":false,"allocatedResources":{"cpu":"500m"},"resources":{"limits":{"cpu":"500m"},"requests":{"cpu":"500m"}},"volumeMounts":[{"name":"kube-api-access-rnjwg","mountPath":"/var/run/secrets/kubernetes.io/serviceaccount","readOnly":true,"recursiveReadOnly":"Disabled"}],"user":{"linux":{"uid":0,"gid":0,"supplementalGroups":[0,1,2,3,4,6,10,11,20,26,27]}}}],"qosClass":"Burstable"}
```
**"failed to create containerd task: failed to create shim task: failed to start io pipe copy: unable to copy pipes: containerd-shim: opening w/o fifo \"/run/containerd/io.containerd.grpc.v1.cri/containers/00498b3fed0360310f38eeaa92cdbfc11ccd99d49a1b5ad9e04221df45c1e8d3/io/2120232854/00498b3fed0360310f38eeaa92cdbfc11ccd99d49a1b5ad9e04221df45c1e8d3-stderr\" failed: context deadline exceeded","startedAt":"1970-01-01T00:00:00Z","finishedAt":"2026-02-17T17:30:08Z","containerID":"containerd://00498b3fed0360310f38eeaa92cdbfc11ccd99d49a1b5ad9e04221df45c1e8d3"}},"lastState":{},"ready":false,"restartCount":0,"image":"registry.k8s.io/e2e-test-images/agnhost:2.59","imageID":"sha256:90625afcd0c7ba09e0c28d4ba6b945e8cba1ab4a236d76a6dc604d4e0c6e4f2a","containerID":"containerd://00498b3fed0360310f38eeaa92cdbfc11ccd99d49a1b5ad9e04221df45c1e8d3","started":false,"allocatedResources":{"cpu":"500m"},"resources":{"limits":{"cpu":"500m"},"requests":{"cpu":"500m"}},"volumeMounts":[{"name":"kube-api-access-rnjwg","mountPath":"/var/run/secrets/kubernetes.io/serviceaccount","readOnly":true,"recursiveReadOnly":"Disabled"}],"user":{"linux":{"uid":0,"gid":0,"supplementalGroups":[0,1,2,3,4,6,10,11,20,26,27]}}}],"qosClass":"Burstable"}**

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-17T18:07:59Z

[containerd logs](https://storage.googleapis.com/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/9325/pull-kueue-test-e2e-release-0-15-1-34/2023807744179441664/artifacts/run-test-e2e-singlecluster-1.34.0/kind-worker/containerd.log) also show:

```
Feb 17 17:30:08 kind-worker containerd[112]: time="2026-02-17T17:30:08.388577799Z" level=error msg="Failed to pipe stdout of container \"00498b3fed0360310f38eeaa92cdbfc11ccd99d49a1b5ad9e04221df45c1e8d3\"" error="read /proc/self/fd/171: file already closed"
Feb 17 17:30:08 kind-worker containerd[112]: time="2026-02-17T17:30:08.471361940Z" level=error msg="StartContainer for \"00498b3fed0360310f38eeaa92cdbfc11ccd99d49a1b5ad9e04221df45c1e8d3\" failed" error="rpc error: code = DeadlineExceeded desc = failed to create containerd task: failed to create shim task: failed to start io pipe copy: unable to copy pipes: containerd-shim: opening w/o fifo \"/run/containerd/io.containerd.grpc.v1.cri/containers/00498b3fed0360310f38eeaa92cdbfc11ccd99d49a1b5ad9e04221df45c1e8d3/io/2120232854/00498b3fed0360310f38eeaa92cdbfc11ccd99d49a1b5ad9e04221df45c1e8d3-stderr\" failed: context deadline exceeded"
```

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-17T18:19:38Z

Ok, so it seems like starting the Pod failed due to a timeout as we have "context deadline exceeded", at ` 17:30:08 ` when the step "Wait for the workload to finish" started at `17:29:32.674` so before 45s timeout elapsed, suggesting this is some other timeout than the test's.
