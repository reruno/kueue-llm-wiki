# Issue #9492: If Kueue fails to remove scheduling gate on pod, kueue still thinks the workload is admitted.

**Summary**: If Kueue fails to remove scheduling gate on pod, kueue still thinks the workload is admitted.

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9492

**Last updated**: 2026-03-09T09:21:50Z

---

## Metadata

- **State**: open
- **Author**: [@kannon92](https://github.com/kannon92)
- **Created**: 2026-02-25T20:15:22Z
- **Updated**: 2026-03-09T09:21:50Z
- **Closed**: —
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 8

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

If I use a simple pod integration on Openshift with some invalid security context settings:

```yaml
apiVersion: v1
kind: Pod
metadata:
  generateName: kueue-sleep-
  namespace: kueue-test
  labels:
    kueue.x-k8s.io/queue-name: user-queue-no-exclude-cpu
spec:
  securityContext:
    runAsUser: 1000
    runAsGroup: 3000
    fsGroup: 2000
    supplementalGroups: [4000]
  containers:
    - name: sleep
      image: busybox
      command:
        - sleep
      args:
        - 100s
      resources:
        requests:
          memory: 100Mi
  restartPolicy: OnFailure
```

This is invalid but the pod is created.

```
kehannon@kehannon-thinkpadp1gen4i:~/Work/kueue-release-testing/ai/rhbok$ oc get workloads -n kueue-test
NAME                          QUEUE                       RESERVED IN     ADMITTED   FINISHED   AGE
pod-kueue-sleep-ltm8v-8d654   user-queue-no-exclude-cpu   cluster-queue   True                  9m15s
```

```
kehannon@kehannon-thinkpadp1gen4i:~/Work/kueue-release-testing/ai/rhbok$ oc get pods -n kueue-test
NAME                READY   STATUS            RESTARTS   AGE
kueue-sleep-ltm8v   0/1     SchedulingGated   0          9m20s
```

Openshift rejects the pod update due to a separate admission process but Kueue doesn't not handle this error correctly.

In kueue-controller-manager you can see the patch fails

```bash
{"level":"error","ts":"2026-02-25T20:03:20.206487306Z","caller":"jobframework/reconciler.go:574","msg":"Unsuspending job","controller":"v1_pod","namespace":"kueue-test","name":"kueue-sleep-ltm8v","reconcileID":"e216f114-4b8a-48cf-82e0-4c2d7151b778","job":"kueue-test/kueue-sleep-ltm8v","gvk":"/v1, Kind=Pod","error":"pods \"kueue-sleep-ltm8v\" is forbidden: unable to validate against any security context constraint: [provider \"anyuid\": Forbidden: not usable by user or serviceaccount, provider restricted-v2: .spec.securityContext.fsGroup: Invalid value: [2000]: 2000 is not an allowed group, provider restricted-v2: .containers[0].runAsUser: Invalid value: 1000: must be in the ranges: [1000790000, 1000799999], provider restricted-v3: .spec.securityContext.hostUsers: Invalid value: null: Host Users must be set to false, provider \"restricted\": Forbidden: not usable by user or serviceaccount, provider \"nested-container\": Forbidden: not usable by user or serviceaccount, provider \"nonroot-v2\": Forbidden: not usable by user or serviceaccount, provider \"nonroot\": Forbidden: not usable by user or serviceaccount, provider \"hostmount-anyuid\": Forbidden: not usable by user or serviceaccount, provider \"hostmount-anyuid-v2\": Forbidden: not usable by user or serviceaccount, provider \"machine-api-termination-handler\": Forbidden: not usable by user or serviceaccount, provider \"hostnetwork-v2\": Forbidden: not usable by user or serviceaccount, provider \"hostnetwork\": Forbidden: not usable by user or serviceaccount, provider \"hostaccess\": Forbidden: not usable by user or serviceaccount, provider \"insights-runtime-extractor-scc\": Forbidden: not usable by user or serviceaccount, provider \"node-exporter\": Forbidden: not usable by user or serviceaccount, provider \"privileged\": Forbidden: not usable by user or serviceaccount]","stacktrace":"sigs.k8s.io/kueue/pkg/controller/jobframework.(*JobReconciler).ReconcileGenericJob\n\t/workspace/upstream/kueue/src/pkg/controller/jobframework/reconciler.go:574\nsigs.k8s.io/kueue/pkg/controller/jobs/pod.(*Reconciler).Reconcile\n\t/workspace/upstream/kueue/src/pkg/controller/jobs/pod/pod_controller.go:117\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).Reconcile\n\t/workspace/upstream/kueue/src/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:216\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).reconcileHandler\n\t/workspace/upstream/kueue/src/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:461\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).processNextWorkItem\n\t/workspace/upstream/kueue/src/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:421\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).Start.func1.1\n\t/workspace/upstream/kueue/src/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:296"}
{"level":"error","ts":"2026-02-25T20:03:20.20655596Z","caller":"controller/controller.go:474","msg":"Reconciler error","controller":"v1_pod","namespace":"kueue-test","name":"kueue-sleep-ltm8v","reconcileID":"e216f114-4b8a-48cf-82e0-4c2d7151b778","error":"pods \"kueue-sleep-ltm8v\" is forbidden: unable to validate against any security context constraint: [provider \"anyuid\": Forbidden: not usable by user or serviceaccount, provider restricted-v2: .spec.securityContext.fsGroup: Invalid value: [2000]: 2000 is not an allowed group, provider restricted-v2: .containers[0].runAsUser: Invalid value: 1000: must be in the ranges: [1000790000, 1000799999], provider restricted-v3: .spec.securityContext.hostUsers: Invalid value: null: Host Users must be set to false, provider \"restricted\": Forbidden: not usable by user or serviceaccount, provider \"nested-container\": Forbidden: not usable by user or serviceaccount, provider \"nonroot-v2\": Forbidden: not usable by user or serviceaccount, provider \"nonroot\": Forbidden: not usable by user or serviceaccount, provider \"hostmount-anyuid\": Forbidden: not usable by user or serviceaccount, provider \"hostmount-anyuid-v2\": Forbidden: not usable by user or serviceaccount, provider \"machine-api-termination-handler\": Forbidden: not usable by user or serviceaccount, provider \"hostnetwork-v2\": Forbidden: not usable by user or serviceaccount, provider \"hostnetwork\": Forbidden: not usable by user or serviceaccount, provider \"hostaccess\": Forbidden: not usable by user or serviceaccount, provider \"insights-runtime-extractor-scc\": Forbidden: not usable by user or serviceaccount, provider \"node-exporter\": Forbidden: not usable by user or serviceaccount, provider \"privileged\": Forbidden: not usable by user or serviceaccount]","stacktrace":"sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).reconcileHandler\n\t/workspace/upstream/kueue/src/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:474\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).processNextWorkItem\n\t/workspace/upstream/kueue/src/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:421\nsigs.k8s.io/controller-runtime/pk
```

**What you expected to happen**:

I would expect that Kueue catches the failed patch and doesn't say the workload is admitted.

**How to reproduce it (as minimally and precisely as possible)**:
On Openshift with Red Hat Build of Kueue (1.2) which is based on Kueue 0.14

**Anything else we need to know?**:

I can't figure out how to reproduce this with Pod Security Admission but this could be an issue if someone has a separate pod admission controller

**Environment**:
- Kubernetes version (use `kubectl version`): 1.34
- Kueue version (use `git describe --tags --dirty --always`): 0.14
- Cloud provider or hardware configuration: openshift
- OS (e.g: `cat /etc/os-release`): rhel
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2026-02-25T20:29:01Z

## Analysis (AI-generated via Claude Code)

The core problem is in the reconciliation loop at `pkg/controller/jobframework/reconciler.go:600-616`.

### Flow

1. **Pod is created** with an invalid security context (e.g., violating OpenShift SCC rules). The Kueue webhook adds a scheduling gate (`kueue.x-k8s.io/admission`) to the pod.

2. **Workload is created and admitted** by the scheduler. The workload gets `Admitted=True` condition and quota is reserved.

3. **Reconciler hits step 7** (`reconciler.go:600`):
   - `job.IsSuspended()` returns `true` — because the pod is still gated (`pod_controller.go:215-216`: `podSuspended` = `IsTerminated || isGated`)
   - `workload.IsAdmitted(wl)` returns `true` — because the scheduler already admitted it
   - So it enters the "unsuspend" path and calls `r.startJob()` (line 604)

4. **`startJob`** calls `cj.Run()` (`reconciler.go:1187`) since Pod implements `ComposableJob`.

5. **`Pod.Run()`** (`pod_controller.go:272-275`) calls `clientutil.Patch()` which calls `prepare()` to remove the scheduling gate and apply node affinity. **This patch is rejected** by OpenShift's SCC admission controller with a "forbidden" error.

6. **Error classification fails** — back in `ReconcileGenericJob` (line 607), `podset.IsPermanent(err)` is checked. This only returns `true` for `ErrInvalidPodsetInfo` or `ErrInvalidPodSetUpdate` (`podset/podset.go:212-213`). The SCC forbidden error is **neither** of these, so `IsPermanent` returns `false`.

7. **The error is returned** at line 616: `return ctrl.Result{}, err`. Controller-runtime requeues with exponential backoff.

### The Stuck State

On every subsequent reconciliation, the exact same thing happens:
- Pod is still gated → `IsSuspended() = true`
- Workload is still admitted → `IsAdmitted() = true`
- Patch fails again with the same SCC error
- Error is not classified as permanent → requeued again

This creates an **infinite retry loop** where:

- **The workload stays `Admitted=True`** — consuming cluster quota permanently
- **The pod stays `SchedulingGated`** — it can never actually run
- **Quota is leaked** — other workloads can't use the capacity held by this stuck workload
- **No clear signal to the user** — the workload looks admitted; only the controller logs show the error

### Root Cause

The `IsPermanent` check at `reconciler.go:607` is too narrow. It only covers Kueue-internal errors (`ErrInvalidPodsetInfo`, `ErrInvalidPodSetUpdate`) but doesn't account for Kubernetes API errors like `StatusReasonForbidden` that are equally permanent in nature — the SCC constraints won't change on retry.

### Potential Fix Directions

1. **Expanding `IsPermanent`** to also treat `apierrors.IsForbidden()` (and possibly other non-transient API errors) as permanent failures, causing the workload to be marked as finished with failure.
2. **Adding specific handling in `Pod.Run()`** to wrap the patch error in a way that signals permanence.
3. **Adding a retry limit or timeout** so that after N failures, the workload gets unadmitted and the quota is freed.

### Comment by [@kannon92](https://github.com/kannon92) — 2026-02-26T01:41:38Z

cc @mimowo @tenzen-y 

I'm looking into this to better understand the openshift side.

I don't really like any of suggestions from claude honestly.

### Comment by [@kannon92](https://github.com/kannon92) — 2026-02-26T16:00:03Z

This fix may be resolved by https://github.com/openshift/apiserver-library-go/pull/128 actually.

The change hasn't made it in a released version of OCP.

### Comment by [@kannon92](https://github.com/kannon92) — 2026-02-26T16:00:40Z

> The IsPermanent check at reconciler.go:607 is too narrow. It only covers Kueue-internal errors (ErrInvalidPodsetInfo, ErrInvalidPodSetUpdate) but doesn't account for Kubernetes API errors like StatusReasonForbidden that are equally permanent in nature — the SCC constraints won't change on retry.

I am curious about this function and what was the goal of it? I think checking API errors would make sense here in addition to Kueue internal errors. But I don't know the rationale for IsPermanent.

### Comment by [@falconlee236](https://github.com/falconlee236) — 2026-03-08T04:34:35Z

I'm interested in fixing this "quota zombie" issue. The infinite retry loop caused by the restricted IsPermanent check definitely needs to be addressed to prevent resource leakage.

Since I've been diving deep into the jobframework recently, I'm confident I can provide a fix that properly handles these permanent API errors.

/assign

### Comment by [@kannon92](https://github.com/kannon92) — 2026-03-08T18:32:09Z

@falconlee236 It may be best to see what @mimowo and @tenzen-y think first.

From my end this isn't too high of a priority honestly because we usually discourage pod based integration and I think the bug would be fixed once SCC does not run on updates to scheduling gates.

### Comment by [@falconlee236](https://github.com/falconlee236) — 2026-03-09T09:01:37Z

/unassign

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-09T09:21:32Z

I don't consider this a bug in Kueue, maybe a small improvement is possible, but I'm not sure about gain/effort ratio. 
Yes, there is an inifinite look in the reconciler, but:
1. gain is low, because controller-runtime can gracefully handle that problem by exponential backoff, growing the backoff to 15min or so
2. effort - i'm not sure, but generally we rarely test external scheduling gates, so adding custom handling may require extensive testing

Let me know if I'm missing something.
