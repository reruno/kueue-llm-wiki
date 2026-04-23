# Issue #8752: [Flaky E2E] LeaderWorkerSet integration when LeaderWorkerSet created should allow to scale up, scale down fast LeaderReadyStartupPolicy

**Summary**: [Flaky E2E] LeaderWorkerSet integration when LeaderWorkerSet created should allow to scale up, scale down fast LeaderReadyStartupPolicy

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8752

**Last updated**: 2026-01-30T08:25:07Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2026-01-23T07:22:20Z
- **Updated**: 2026-01-30T08:25:07Z
- **Closed**: 2026-01-30T08:25:06Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mykysha](https://github.com/mykysha)
- **Comments**: 6

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->

/kind flake

**What happened**:

End To End Suite: kindest/node:v1.35.0: [It] LeaderWorkerSet integration when LeaderWorkerSet created should allow to scale up, scale down fast LeaderReadyStartupPolicy 

```
{Timed out after 45.001s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/util/util.go:120 with:
Error matcher expects an error.  Got:
    <nil>: nil failed [FAILED] Timed out after 45.001s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/util/util.go:120 with:
Error matcher expects an error.  Got:
    <nil>: nil
In [It] at: /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/singlecluster/leaderworkerset_test.go:481 @ 01/23/26 04:53:54.402
}
```

**What you expected to happen**:

No issue

**How to reproduce it (as minimally and precisely as possible)**:

https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-release-0-15-1-35/2014557337439703040

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

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-23T08:12:36Z

/assign @mykysha
Tentatively as this looks close to https://github.com/kubernetes-sigs/kueue/issues/8733 (same test, different line)

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-23T09:02:01Z

https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/8755/pull-kueue-test-e2e-main-1-35/2014610903948857344

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-01-26T11:23:01Z

One more https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/8724/pull-kueue-test-e2e-main-1-32/2015740598748712960.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-26T14:51:18Z

Interesting so the deletion of the leader Pod `lws-e2e-kxs58/lws-1` (UID: `2e00ca28-c0a8-4163-b2eb-401eb3e28ada`) is stuck due to the finalizer: `foregroundDeletion` - this is the core finalizer indicating the k8s GC is waiting for the children to be deleted fist. 


In this case the child is StatefulSet for leaders, and it matches the LWS code propagation policy, see [here](https://github.com/kubernetes-sigs/lws/blob/d450679bd16bab7156ae2b9962068776964ea971/pkg/controllers/pod_controller.go#L2454-L250). We can confirm that request in [LWS logs](https://storage.googleapis.com/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/8732/pull-kueue-test-e2e-main-1-33/2014193502698606592/artifacts/run-test-e2e-singlecluster-1.33.7/kind-worker2/pods/lws-system_lws-controller-manager-8cf8bfb5d-4zln6_b223c871-5af1-42be-9eaf-a4e390f10284/manager/0.log), see:
```
2026-01-22T04:44:14.399736918Z stderr F 2026-01-22T04:44:14Z	DEBUG	events	Worker pod lws-1-2 failed, deleted leader pod lws-1 to recreate group 1	{"type": "Normal", "object": {"kind":"LeaderWorkerSet","namespace":"lws-e2e-kxs58","name":"lws","uid":"940d0e08-7f9a-4a61-8eb6-c20b265bb984","apiVersion":"leaderworkerset.x-k8s.io/v1","resourceVersion":"7299"}, "reason": "RecreateGroupOnPodRestart"}
```
so now the question is why the StatefulSet couldn't get deleted.

I will continue looking, but one thing which stands out is this in the [`kube-controller-manager` logs](https://storage.googleapis.com/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/8732/pull-kueue-test-e2e-main-1-33/2014193502698606592/artifacts/run-test-e2e-singlecluster-1.33.7/kind-control-plane/pods/kube-system_kube-controller-manager-kind-control-plane_8a1398db1ff4f808bf4f65fdd17efddf/kube-controller-manager/0.log):

```
2026-01-22T04:44:17.167420935Z stderr F E0122 04:44:17.167234       1 garbagecollector.go:360] "Unhandled Error" err="error syncing item &garbagecollector.node{identity:garbagecollector.objectReference{OwnerReference:v1.OwnerReference{APIVersion:\"apps/v1\", Kind:\"StatefulSet\", Name:\"lws-1\", UID:\"299406b0-694d-4f0d-bb42-f4af834b3f69\", Controller:(*bool)(nil), BlockOwnerDeletion:(*bool)(nil)}, Namespace:\"lws-e2e-kxs58\"}, dependentsLock:sync.RWMutex{w:sync.Mutex{_:sync.noCopy{}, mu:sync.Mutex{state:0, sema:0x0}}, writerSem:0x0, readerSem:0x0, readerCount:atomic.Int32{_:atomic.noCopy{}, v:1}, readerWait:atomic.Int32{_:atomic.noCopy{}, v:0}}, dependents:map[*garbagecollector.node]struct {}{}, deletingDependents:true, deletingDependentsLock:sync.RWMutex{w:sync.Mutex{_:sync.noCopy{}, mu:sync.Mutex{state:0, sema:0x0}}, writerSem:0x0, readerSem:0x0, readerCount:atomic.Int32{_:atomic.noCopy{}, v:0}, readerWait:atomic.Int32{_:atomic.noCopy{}, v:0}}, beingDeleted:true, beingDeletedLock:sync.RWMutex{w:sync.Mutex{_:sync.noCopy{}, mu:sync.Mutex{state:0, sema:0x0}}, writerSem:0x0, readerSem:0x0, readerCount:atomic.Int32{_:atomic.noCopy{}, v:0}, readerWait:atomic.Int32{_:atomic.noCopy{}, v:0}}, virtual:false, virtualLock:sync.RWMutex{w:sync.Mutex{_:sync.noCopy{}, mu:sync.Mutex{state:0, sema:0x0}}, writerSem:0x0, readerSem:0x0, readerCount:atomic.Int32{_:atomic.noCopy{}, v:0}, readerWait:atomic.Int32{_:atomic.noCopy{}, v:0}}, owners:[]v1.OwnerReference{v1.OwnerReference{APIVersion:\"v1\", Kind:\"Pod\", Name:\"lws-1\", UID:\"2e00ca28-c0a8-4163-b2eb-401eb3e28ada\", Controller:(*bool)(0xc003a50efa), BlockOwnerDeletion:(*bool)(0xc003a50efb)}}}: admission webhook \"mstatefulset.kb.io\" denied the request: StatefulSet.apps \"lws\" not found" logger="UnhandledError"
2026-01-22T04:44:17.174660267Z stderr F I0122 04:44:17.174522       1 garbagecollector.go:501] "Processing item" logger="garbage-collector-controller" item="[apps/v1/StatefulSet, namespace: lws-e2e-kxs58, name: lws-1, uid: 299406b0-694d-4f0d-bb42-f4af834b3f69]" virtual=false
```
It looks like kube-controller-manager is trying to remove the owner reference from the StatefulSet, but it cannot perform the operation because `StatefulSet.apps \"lws\" not found`. I'm wondering the bug might be in our statefulset_webhook which calls [WorkloadShouldBeSuspended](https://github.com/kubernetes-sigs/kueue/blob/9d894011a29f0cd33c08eb7c9c4c875ddf58dc60/pkg/controller/jobs/statefulset/statefulset_webhook.go#L73-L77), but that might fail if the parent is "not found". I think we should only call `WorkloadShouldBeSuspended` only  on the first pass - and skip if `SuspendedByParentAnnotation` is already set. 

Still, I don't have a full understanding yet. cc @mbobrovskyi @sohankunkerkar who may have some good ideas here.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-01-30T08:25:01Z

/close

Due to fixed by https://github.com/kubernetes-sigs/kueue/pull/8862

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-01-30T08:25:07Z

@mbobrovskyi: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/8752#issuecomment-3822481527):

>/close
>
>Due to fixed by https://github.com/kubernetes-sigs/kueue/pull/8862


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
