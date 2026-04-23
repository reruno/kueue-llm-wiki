# Issue #9752: Failure Recovery Policy when the kubelet on a node goes down should unblock the stuck pod's parents that are being deleted with foreground propagation

**Summary**: Failure Recovery Policy when the kubelet on a node goes down should unblock the stuck pod's parents that are being deleted with foreground propagation

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9752

**Last updated**: 2026-04-17T17:09:33Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-03-09T08:58:00Z
- **Updated**: 2026-04-17T17:09:33Z
- **Closed**: 2026-04-17T17:09:32Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@kshalot](https://github.com/kshalot)
- **Comments**: 4

## Description


**Which test is flaking?**:
 Failure Recovery Policy when the kubelet on a node goes down should unblock the stuck pod's parents that are being deleted with foreground propagation 
**Link to failed CI job or steps to reproduce locally**:
https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-customconfigs-release-0-15/2030824044005167104
**Failure message or logs**:
```
End To End Custom Configs handling Suite: kindest/node:v1.35.0: [It] Failure Recovery Policy when the kubelet on a node goes down should unblock the stuck pod's parents that are being deleted with foreground propagation expand_less	46s
{Timed out after 45.001s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/customconfigs/failure_recovery_policy_test.go:140 with:
Expected
    <int32>: 0
to equal
    <int32>: 1 failed [FAILED] Timed out after 45.001s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/customconfigs/failure_recovery_policy_test.go:140 with:
Expected
    <int32>: 0
to equal
    <int32>: 1
In [BeforeEach] at: /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/customconfigs/failure_recovery_policy_test.go:142 @ 03/09/26 02:03:45.81
}
```

**Anything else we need to know?**:

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-09T08:58:28Z

cc @kshalot ptal

### Comment by [@kshalot](https://github.com/kshalot) — 2026-03-09T10:52:58Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2026-04-17T17:09:25Z

Ok I checked the logs here, based on https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-customconfigs-release-0-15/2030824044005167104

So, we see the JOb in namespace `frp-plpm8` didn't got running. When I check kube-scheduler logs for the namespace by grep we see:

```
2026-03-09T02:03:00.865045975Z stderr F I0309 02:03:00.864858       1 eventhandlers.go:233] "Add event for unscheduled pod" pod="frp-plpm8/test-job-dqw79"
2026-03-09T02:03:00.865275857Z stderr F I0309 02:03:00.865160       1 schedule_one.go:99] "Attempting to schedule pod" pod="frp-plpm8/test-job-dqw79"
2026-03-09T02:03:00.866189052Z stderr F I0309 02:03:00.866022       1 pod_binding.go:51] "Attempting to bind pod to node" pod="frp-plpm8/test-job-dqw79" node="kind-worker"
2026-03-09T02:03:00.870062895Z stderr F I0309 02:03:00.869881       1 eventhandlers.go:391] "Add event for scheduled pod" pod="frp-plpm8/test-job-dqw79"
2026-03-09T02:03:00.870280126Z stderr F I0309 02:03:00.870084       1 eventhandlers.go:352] "Delete event for unscheduled pod" pod="frp-plpm8/test-job-dqw79"
2026-03-09T02:03:00.870428567Z stderr F I0309 02:03:00.870266       1 schedule_one.go:337] "Successfully bound pod to node" pod="frp-plpm8/test-job-dqw79" node="kind-worker" evaluatedNodes=3 feasibleNodes=2
2026-03-09T02:03:03.940913149Z stderr F I0309 02:03:03.940307       1 eventhandlers.go:461] "Delete event for scheduled pod" pod="frp-plpm8/test-job-dqw79"
```
So the Pod "frp-plpm8/test-job-dqw79" was deleted very quickly after scheduling, no wonder the Job wasn't running.

So, I went to kube-controller-manager logs to see why the Pod was deleted, and we see:
```
2026-03-09T02:03:01.871427141Z stderr F I0309 02:03:01.871253       1 taint_eviction.go:111] "Deleting pod" controller="taint-eviction-controller" pod="frp-plpm8/test-job-dqw79"
2026-03-09T02:03:01.871592422Z stderr F I0309 02:03:01.871461       1 event.go:389] "Event occurred" logger="taint-eviction-controller" object="frp-plpm8/test-job-dqw79" fieldPath="" kind="Pod" apiVersion="v1" type="Normal" reason="TaintManagerEviction" message="Marking for deletion Pod frp-plpm8/test-job-dqw79"
```
So it is pretty clear because the node was tainted.

This got me thinking this is before https://github.com/kubernetes-sigs/kueue/pull/10120, and indeed the failed test was running on commit De6ffb9993eb58303b4a9f99bcb1636508a254bb which is from Match 6th, way before the fix for waiting for the Node to be ready and fully operational.

So, I think the issue is already fixed by https://github.com/kubernetes-sigs/kueue/pull/10120

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-04-17T17:09:33Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/9752#issuecomment-4269901178):

>Ok I checked the logs here, based on https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-customconfigs-release-0-15/2030824044005167104
>
>So, we see the JOb in namespace `frp-plpm8` didn't got running. When I check kube-scheduler logs for the namespace by grep we see:
>
>```
>2026-03-09T02:03:00.865045975Z stderr F I0309 02:03:00.864858       1 eventhandlers.go:233] "Add event for unscheduled pod" pod="frp-plpm8/test-job-dqw79"
>2026-03-09T02:03:00.865275857Z stderr F I0309 02:03:00.865160       1 schedule_one.go:99] "Attempting to schedule pod" pod="frp-plpm8/test-job-dqw79"
>2026-03-09T02:03:00.866189052Z stderr F I0309 02:03:00.866022       1 pod_binding.go:51] "Attempting to bind pod to node" pod="frp-plpm8/test-job-dqw79" node="kind-worker"
>2026-03-09T02:03:00.870062895Z stderr F I0309 02:03:00.869881       1 eventhandlers.go:391] "Add event for scheduled pod" pod="frp-plpm8/test-job-dqw79"
>2026-03-09T02:03:00.870280126Z stderr F I0309 02:03:00.870084       1 eventhandlers.go:352] "Delete event for unscheduled pod" pod="frp-plpm8/test-job-dqw79"
>2026-03-09T02:03:00.870428567Z stderr F I0309 02:03:00.870266       1 schedule_one.go:337] "Successfully bound pod to node" pod="frp-plpm8/test-job-dqw79" node="kind-worker" evaluatedNodes=3 feasibleNodes=2
>2026-03-09T02:03:03.940913149Z stderr F I0309 02:03:03.940307       1 eventhandlers.go:461] "Delete event for scheduled pod" pod="frp-plpm8/test-job-dqw79"
>```
>So the Pod "frp-plpm8/test-job-dqw79" was deleted very quickly after scheduling, no wonder the Job wasn't running.
>
>So, I went to kube-controller-manager logs to see why the Pod was deleted, and we see:
>```
>2026-03-09T02:03:01.871427141Z stderr F I0309 02:03:01.871253       1 taint_eviction.go:111] "Deleting pod" controller="taint-eviction-controller" pod="frp-plpm8/test-job-dqw79"
>2026-03-09T02:03:01.871592422Z stderr F I0309 02:03:01.871461       1 event.go:389] "Event occurred" logger="taint-eviction-controller" object="frp-plpm8/test-job-dqw79" fieldPath="" kind="Pod" apiVersion="v1" type="Normal" reason="TaintManagerEviction" message="Marking for deletion Pod frp-plpm8/test-job-dqw79"
>```
>So it is pretty clear because the node was tainted.
>
>This got me thinking this is before https://github.com/kubernetes-sigs/kueue/pull/10120, and indeed the failed test was running on commit De6ffb9993eb58303b4a9f99bcb1636508a254bb which is from Match 6th, way before the fix for waiting for the Node to be ready and fully operational.
>
>So, I think the issue is already fixed by https://github.com/kubernetes-sigs/kueue/pull/10120
>
>/close
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
