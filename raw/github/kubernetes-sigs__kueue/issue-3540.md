# Issue #3540: Add option to disable strict pod spec validation

**Summary**: Add option to disable strict pod spec validation

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3540

**Last updated**: 2025-11-18T11:41:24Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@LucasZanellaMBTI](https://github.com/LucasZanellaMBTI)
- **Created**: 2024-11-15T08:34:20Z
- **Updated**: 2025-11-18T11:41:24Z
- **Closed**: 2025-10-30T07:58:03Z
- **Labels**: `kind/bug`, `kind/feature`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 41

## Description

<!-- Please only use this template for submitting enhancement requests -->
**What would you like to be added**:

We would need to influence strictness level of Pod spec validation.

**Why is this needed**:

It turned out Kueue validates Pod spec differently compared to plain K8s.
In our case workloads have been blocked due to env vars being duplicated in Pod spec.
Because there are many components involved regarding pod spec creation and manipulation
we cannot guarantee env var keys to be unique.

Plain K8s wouldn't complain about duplicated env vars. This is why we think it would be helpful
to offer more control on Kueue's validation mechanism.

This could also be relevant to resource types other than Pods.

Log of kueue controller `v0.8.1`:
``` json
 {
    "level": "error",
    "ts": "2024-11-14T17:56:56.563529963Z",
    "caller": "controller/controller.go:329",
    "msg": "Reconcilererror",
    "controller": "v1_pod",
    "namespace": "",
    "name": "",
    "reconcileID": "",
    "error": "Workload.kueue.x-k8s.io\"pod-reproduce-env-bug-o5ymx1-n0-0-24899\"isinvalid:spec.podSets[0].template.spec.containers[0].env[2]:Duplicatevalue:map[string]interface{},{\"name\":\"DUPLICATE_ENV\"},",
    "stacktrace": "sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).reconcileHandler\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:329\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).processNextWorkItem\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:266\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).Start.func2.2\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:227"
  }
```

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [x] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.


<sub>Lucas Zanella [lucas.zanella@mercedes-benz.com](mailto:lucas.zanella@mercedes-benz.com), Mercedes-Benz Tech Innovation GmbH, [imprint](https://github.com/mercedes-benz/foss/blob/master/PROVIDER_INFORMATION.md)</sub>

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-15T09:50:01Z

I believe this is not about Kueue validation but the underlying bug in SSA which prevents updates when fields are duplicated. For reference: https://github.com/kubernetes/kubernetes/issues/113482.

Given the bug for SSA exists for 2 years now I think it is unlikely this will be resolved soon, so I would suggest to consider withdrawing from SSA in Kueue. This is what we did for PodFailurePolicy in the core k8s: https://github.com/kubernetes/kubernetes/pull/121103.

I guess we could maintain two modes in Kueue behind a feature gate like `UseSSAForWorkload`, in case someone needs it. WDYT @tenzen-y ?

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-11-18T06:28:05Z

> I believe this is not about Kueue validation but the underlying bug in SSA which prevents updates when fields are duplicated. For reference: [kubernetes/kubernetes#113482](https://github.com/kubernetes/kubernetes/issues/113482).
> 
> Given the bug for SSA exists for 2 years now I think it is unlikely this will be resolved soon, so I would suggest to consider withdrawing from SSA in Kueue. This is what we did for PodFailurePolicy in the core k8s: [kubernetes/kubernetes#121103](https://github.com/kubernetes/kubernetes/pull/121103).
> 
> I guess we could maintain two modes in Kueue behind a feature gate like `UseSSAForWorkload`, in case someone needs it. WDYT @tenzen-y ?

The problem occurs when creating the workload, but not when patching it.

https://github.com/kubernetes-sigs/kueue/blob/30da29361a6fc95ade0a4350b97494394d30b0b9/pkg/controller/jobframework/reconciler.go#L1050-L1052

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-18T06:47:23Z

@mbobrovskyi can you check which layer rejects the creation? Is this validation in Kueue? If validation if Kueue I suppose it might have been added to prevent later failures due to SSA for patches.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-11-18T06:49:21Z

> @mbobrovskyi can you check which layer rejects the creation? Is this validation in Kueue?

No, it looks like k8s validation.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-18T06:55:45Z

Interesting, the error message in the description is from `controller/controller.go:329`, and the message contains `Workload.kueue.x-k8s.io\"pod-reproduce-env-bug-o5ymx1-n0-0-24899`, which suggests that the object already exists.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-11-18T06:57:31Z

I tried with creation. But I believe we have the same issue with update.

```
{"level":"Level(-2)","ts":"2024-11-18T05:35:30.888806634Z","caller":"jobframework/reconciler.go:332","msg":"Reconciling Job","controller":"v1_pod","namespace":"default","name":"kueue-sleep-bswbh","reconcileID":"541c2f22-019a-4285-a710-5a7f28c0c0ba","job":"default/kueue-sleep-bswbh","gvk":"/v1, Kind=Pod"}
{"level":"error","ts":"2024-11-18T05:35:30.902655051Z","caller":"jobframework/reconciler.go:410","msg":"Handling job with no workload","controller":"v1_pod","namespace":"default","name":"kueue-sleep-bswbh","reconcileID":"541c2f22-019a-4285-a710-5a7f28c0c0ba","job":"default/kueue-sleep-bswbh","gvk":"/v1, Kind=Pod","error":"Workload.kueue.x-k8s.io \"pod-kueue-sleep-bswbh-cb334\" is invalid: spec.podSets[0].template.spec.containers[0].env[1]: Duplicate value: map[string]interface {}{\"name\":\"DUPLICATE\"}","stacktrace":"sigs.k8s.io/kueue/pkg/controller/jobframework.(*JobReconciler).ReconcileGenericJob\n\t/workspace/pkg/controller/jobframework/reconciler.go:410\nsigs.k8s.io/kueue/pkg/controller/jobs/pod.(*Reconciler).Reconcile\n\t/workspace/pkg/controller/jobs/pod/pod_controller.go:123\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).Reconcile\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:116\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).reconcileHandler\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:303\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).processNextWorkItem\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:263\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).Start.func2.2\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:224"}
{"level":"error","ts":"2024-11-18T05:35:30.902756843Z","caller":"controller/controller.go:316","msg":"Reconciler error","controller":"v1_pod","namespace":"default","name":"kueue-sleep-bswbh","reconcileID":"541c2f22-019a-4285-a710-5a7f28c0c0ba","error":"Workload.kueue.x-k8s.io \"pod-kueue-sleep-bswbh-cb334\" is invalid: spec.podSets[0].template.spec.containers[0].env[1]: Duplicate value: map[string]interface {}{\"name\":\"DUPLICATE\"}","stacktrace":"sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).reconcileHandler\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:316\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).processNextWorkItem\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:263\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).Start.func2.2\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:224"}
```

### Comment by [@hy00nc](https://github.com/hy00nc) — 2025-02-07T23:59:48Z

Hi @mimowo , do we have any updates on this? I'm facing the same issue on pod creation and this is blocking Kueue from creating a Workload from a pod making it stuck in scheduling gated without any related events.

It is hard to notice why the pod is not scheduled unless users are familiar with Kueue and look into controller logs. I'd really appreciate if we can get some enhancement on this part.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-08T14:59:21Z

> I believe this is not about Kueue validation but the underlying bug in SSA which prevents updates when fields are duplicated. For reference: [kubernetes/kubernetes#113482](https://github.com/kubernetes/kubernetes/issues/113482).
> 
> Given the bug for SSA exists for 2 years now I think it is unlikely this will be resolved soon, so I would suggest to consider withdrawing from SSA in Kueue. This is what we did for PodFailurePolicy in the core k8s: [kubernetes/kubernetes#121103](https://github.com/kubernetes/kubernetes/pull/121103).
> 
> I guess we could maintain two modes in Kueue behind a feature gate like `UseSSAForWorkload`, in case someone needs it. WDYT [@tenzen-y](https://github.com/tenzen-y) ?

As I confirmed the duplicated map keys (ports, envs, and so on), I still face the same issue in v1.32 cluster as well.
But, as we can see https://github.com/kubernetes/kubernetes/issues/113482, this issue seems not to be resolved.

So, I agree with introducing `UseSSAForWorkload` feature gate. After the root cause is fixed in core kube, we can delete the `UseSSAForWorkload`. I honestly think we should not use the duplicated keys in those fields.

But, I think `UseSSAForWorkoad` could be helpful to mitigate this issue immediately, then provide the improvement period in their production cluster. @mimowo Any thoughts?

Note that `UseSSAForWorkload` should always be enabled by default.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-05-09T15:50:20Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle stale`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-06-08T16:38:12Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle rotten

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-11T12:38:12Z

/remove-lifecycle rotten

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-21T09:25:03Z

/kind bug
I think this can be considered a bug in Kueue. Users can create workloads which execute of without Kueue, but fail to execute when using Kueue. Yes, these are corner cases, but we've seen such workloads in practice.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-24T08:30:55Z

> But, I think UseSSAForWorkoad could be helpful to mitigate this issue immediately, then provide the improvement period in their production cluster. @mimowo Any thoughts?

I'm ok with the feature gate, but given the amount of issues SSA creates, I would just drop it altogether from Kueue, see https://github.com/kubernetes-sigs/kueue/issues/6158.

I'm not clear what are the benefits of using SSA in Kueue, especially as the upstream bug is not fixed for 3 years it does not seem as fixed any time soon. Now we have in Kueue a weird mixture of Patches and SSA which makes reasoning about code hard.

> Note that UseSSAForWorkload should always be enabled by default.

TBH, I would propose to have feature gate `UsaPatchForWorkload` and graduate it (see above).

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-24T09:19:41Z

@tenzen-y do you see any reason to continue using SSA in Kueue?

### Comment by [@mwysokin](https://github.com/mwysokin) — 2025-08-28T17:41:18Z

@LucasZanellaMBTI I just noticed that the progress on the issue is not clearly visible here. We've decided to implement an alternative strategy to SSA using PATCH and the work is in-flight. We're planning to release it in September. The issue where you can track the work is here: https://github.com/kubernetes-sigs/kueue/issues/6158

### Comment by [@LucasZanellaMBTI](https://github.com/LucasZanellaMBTI) — 2025-08-28T19:47:42Z

@mwysokin we are glad to read this. Thanks for the update here.

### Comment by [@bd-hhause](https://github.com/bd-hhause) — 2025-09-04T15:24:17Z

Just ran into this today with Buildkite adding a duplicate key to `spec.podSets[0].template.spec.containers[0].env`. Also happy to see that a fix is actively being worked on.

### Comment by [@mwysokin](https://github.com/mwysokin) — 2025-10-08T19:47:25Z

@LucasZanellaMBTI @bd-hhause FYI The feature was implemented and is available in releases 0.14.0 and 0.14.1
The docs: https://kueue.sigs.k8s.io/docs/concepts/workload/#workload-updates-by-kueue

### Comment by [@bd-hhause](https://github.com/bd-hhause) — 2025-10-08T20:04:17Z

Awesome, we'll try out the `WorkloadRequestUseMergePatch` soon. Where is this mentioned in the release notes?

### Comment by [@mwysokin](https://github.com/mwysokin) — 2025-10-08T21:42:32Z

I think the contributor and the reviewers might've missed adding the proper release notes block because the feature was scattered across multiple PRs or only adding a switch was worthy of a release notes item because I think I see it as the last item in the features section for release 0.14.0


If you're interested in how it was solved here's the umbrella issue (https://github.com/kubernetes-sigs/kueue/issues/6158). 

CC @mimowo @mszadkow

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-09T07:07:45Z

> Awesome, we'll try out the WorkloadRequestUseMergePatch soon. Where is this mentioned in the release notes?

Great, I can see it is listed under [0.14.0](https://github.com/kubernetes-sigs/kueue/releases/tag/v0.14.0), the notes for patch releases are only incremental. So, when you look for notes for "features" they are all under 0.x.0 release.

> I think the contributor and the reviewers might've missed adding the proper release notes block because the feature was scattered across multiple PRs or only adding a switch was worthy of a release notes

Indeed, when a feature is backed by multiple PRs we only report once. This is not unique to that feature by any means.

While this is implemented, note that the feature remains Alpha. One "known issue" is that on rare occasions the conditions set by a Kueue internal controller might be overitten by a patch sent by Kueue scheduler. This should be safe in all cases I know about - the controller will be re-triggered and will re-add the condition. However, I'm still considering this as an area for improvement before graduation to Beta: https://github.com/kubernetes-sigs/kueue/issues/7035

/close
Let's use  https://github.com/kubernetes-sigs/kueue/issues/7035 to track the remaining work.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-10-09T07:07:51Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3540#issuecomment-3384426804):

>> Awesome, we'll try out the WorkloadRequestUseMergePatch soon. Where is this mentioned in the release notes?
>
>Great, I can see it is listed under 0.14.0, the notes for patch releases are only incremental. So, when you look for notes for "features" they are all under 0.x.0 release.
>
>> I think the contributor and the reviewers might've missed adding the proper release notes block because the feature was scattered across multiple PRs or only adding a switch was worthy of a release notes
>
>Indeed, when a feature is backed by multiple PRs we only report once. This is not unique to that feature by any means.
>
>While this is implemented, note that the feature remains Alpha. One "known issue" is that on rare occasions the conditions set by a Kueue internal controller might be overitten by a patch sent by Kueue scheduler. This should be safe in all cases I know about - the controller will be re-triggered and will re-add the condition. However, I'm still considering this as an area for improvement before graduation to Beta: https://github.com/kubernetes-sigs/kueue/issues/7035
>
>/close
>Let's use  https://github.com/kubernetes-sigs/kueue/issues/7035 to track the remaining work.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@LucasZanellaMBTI](https://github.com/LucasZanellaMBTI) — 2025-10-15T11:28:59Z

@mimowo @mwysokin thank you so much for implementing this. We we'll give it a try asap.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-23T12:25:10Z

@LucasZanellaMBTI we just released 0.14.2 which contains a small fix for the mechanism. 

It would be great if you can share results of your testing

### Comment by [@bd-hhause](https://github.com/bd-hhause) — 2025-10-23T13:33:13Z

@mimowo I tried enabling the feature flag a couple of days ago and am still experiencing the following error in the Kueue controller: 

```
"error":"Workload.kueue.x-k8s.io \"job-buildkite-0199151e-0f3b-4dd8-b28b-8790dbf06e9e-08da5\" is invalid: spec.podSets[0].template.spec.containers[0].env[14]: Duplicate value: map[string]interface {}{\"name\":\"BUILDKITE_HOOKS_PATH\"}"
```

This error occurs when the workload first is created at `handleJobWithNoWorkload` in the jobFramework reconciler. I am also exploring options to remove the duplicate ENV VAR from the other controller, since it doesn't seem like it should be Kueue's responsibility to handle this case.

Does this case fall outside of the scope of changes in this PR?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-23T13:39:15Z

> @mimowo I tried enabling the feature flag a couple of days ago and am still experiencing the following error in the Kueue controller:

This is quite surprising, because this error is SSA specific, whilst with this feature gate SSA should not be used.

There might be an omission though, we should test this more end-to-end. I will update the thread.

### Comment by [@bd-hhause](https://github.com/bd-hhause) — 2025-10-23T13:42:10Z

Thanks, let me know if you'd like me to share a minimal example to reproduce.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-23T13:54:07Z

Do you maybe the logs to include the specific log line which might be sending the problematic patch?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-23T14:22:06Z

/reopen
I reproduced the issue quite easily (on 0.14.2), the log line :
```
{"level":"error","ts":"2025-10-23T14:19:18.259276575Z","caller":"jobframework/reconciler.go:481","msg":"Handling job with no workload","controller":"job","controllerGroup":"batch","controllerKind":"Job","Job":{"name":"sample-jobcfcfp","namespace":"default"},"namespace":"default","name":"sample-jobcfcfp","reconcileID":"0d7f5d12-403b-4f75-be17-15b842e563e7","job":"default/sample-jobcfcfp","gvk":"batch/v1, Kind=Job","error":"Workload.kueue.x-k8s.io \"job-sample-jobcfcfp-b9d77\" is invalid: spec.podSets[0].template.spec.containers[0].env[1]: Duplicate value: {\"name\":\"DEMO\"}","stacktrace":"sigs.k8s.io/kueue/pkg/controller/jobframework.(*JobReconciler).ReconcileGenericJob\n\t/workspace/pkg/controller/jobframework/reconciler.go:481\nsigs.k8s.io/kueue/pkg/controller/jobframework.(*genericReconciler).Reconcile\n\t/workspace/pkg/controller/jobframework/reconciler.go:1485\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).Reconcile\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:216\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).reconcileHandler\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:461\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).processNextWorkItem\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:421\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).Start.func1.1\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:296"}
{"level":"error","ts":"2025-10-23T14:19:18.259355125Z","caller":"controller/controller.go:474","msg":"Reconciler error","controller":"job","controllerGroup":"batch","controllerKind":"Job","Job":{"name":"sample-jobcfcfp","namespace":"default"},"namespace":"default","name":"sample-jobcfcfp","reconcileID":"0d7f5d12-403b-4f75-be17-15b842e563e7","error":"Workload.kueue.x-k8s.io \"job-sample-jobcfcfp-b9d77\" is invalid: spec.podSets[0].template.spec.containers[0].env[1]: Duplicate value: {\"name\":\"DEMO\"}","stacktrace":"sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).reconcileHandler\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:474\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).processNextWorkItem\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:421\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).Start.func1.1\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:296"}
```
with the Job:
```yaml
apiVersion: batch/v1
kind: Job
metadata:
  generateName: sample-job
  namespace: default
  labels:
    kueue.x-k8s.io/queue-name: user-queue
spec:
  parallelism: 3
  completions: 3
  completionMode: Indexed
  suspend: true
  template:
    spec:
      containers:
      - name: dummy-job
        image: gcr.io/k8s-staging-perf-tests/sleep:v0.0.3
        args: ["300s"]
        env:
        - name: DEMO
          value: "Hello from the environment"
        - name: DEMO
          value: "Such a sweet sorrow"
        resources:
          requests:
            cpu: "1"
            memory: "1Mi"
      restartPolicy: Never
```

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-10-23T14:22:13Z

@mimowo: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3540#issuecomment-3437305129):

>/reopen
>I reproduced the issue quite easily, the log line :
>```
>{"level":"error","ts":"2025-10-23T14:19:18.259276575Z","caller":"jobframework/reconciler.go:481","msg":"Handling job with no workload","controller":"job","controllerGroup":"batch","controllerKind":"Job","Job":{"name":"sample-jobcfcfp","namespace":"default"},"namespace":"default","name":"sample-jobcfcfp","reconcileID":"0d7f5d12-403b-4f75-be17-15b842e563e7","job":"default/sample-jobcfcfp","gvk":"batch/v1, Kind=Job","error":"Workload.kueue.x-k8s.io \"job-sample-jobcfcfp-b9d77\" is invalid: spec.podSets[0].template.spec.containers[0].env[1]: Duplicate value: {\"name\":\"DEMO\"}","stacktrace":"sigs.k8s.io/kueue/pkg/controller/jobframework.(*JobReconciler).ReconcileGenericJob\n\t/workspace/pkg/controller/jobframework/reconciler.go:481\nsigs.k8s.io/kueue/pkg/controller/jobframework.(*genericReconciler).Reconcile\n\t/workspace/pkg/controller/jobframework/reconciler.go:1485\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).Reconcile\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:216\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).reconcileHandler\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:461\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).processNextWorkItem\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:421\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).Start.func1.1\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:296"}
>{"level":"error","ts":"2025-10-23T14:19:18.259355125Z","caller":"controller/controller.go:474","msg":"Reconciler error","controller":"job","controllerGroup":"batch","controllerKind":"Job","Job":{"name":"sample-jobcfcfp","namespace":"default"},"namespace":"default","name":"sample-jobcfcfp","reconcileID":"0d7f5d12-403b-4f75-be17-15b842e563e7","error":"Workload.kueue.x-k8s.io \"job-sample-jobcfcfp-b9d77\" is invalid: spec.podSets[0].template.spec.containers[0].env[1]: Duplicate value: {\"name\":\"DEMO\"}","stacktrace":"sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).reconcileHandler\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:474\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).processNextWorkItem\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:421\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).Start.func1.1\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:296"}
>```
>with the Job:
>```yaml
>apiVersion: batch/v1
>kind: Job
>metadata:
>  generateName: sample-job
>  namespace: default
>  labels:
>    kueue.x-k8s.io/queue-name: user-queue
>spec:
>  parallelism: 3
>  completions: 3
>  completionMode: Indexed
>  suspend: true
>  template:
>    spec:
>      containers:
>      - name: dummy-job
>        image: gcr.io/k8s-staging-perf-tests/sleep:v0.0.3
>        args: ["300s"]
>        env:
>        - name: DEMO
>          value: "Hello from the environment"
>        - name: DEMO
>          value: "Such a sweet sorrow"
>        resources:
>          requests:
>            cpu: "1"
>            memory: "1Mi"
>      restartPolicy: Never
>```


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-23T14:22:46Z

cc @mszadkow @mbobrovskyi could you check if maybe we still are using SSA in some places?

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-10-23T14:25:40Z

/assign

### Comment by [@bd-hhause](https://github.com/bd-hhause) — 2025-10-23T14:38:31Z

@mimowo Sure, here's a quick example: 

```
apiVersion: batch/v1
kind: Job
metadata:
  name: test-duplicate-env
spec:
  template:
    spec:
      restartPolicy: Never
      containers:
      - name: busybox
        image: busybox:1.35
        command: ["sh", "-c", "env | grep TEST_VAR; sleep 30"]
        env:
        - name: TEST_VAR
          value: "first_value"
        - name: TEST_VAR
          value: "second_value"
        - name: OTHER_VAR
          value: "normal_var"
```

`k apply -f test_job.yaml`

View error: 
`k logs -n kueue-system kueue-controller-manager-7499d78568-jb7rv | grep test-duplicate-env`

```
{
  "level": "error",
  "ts": "2025-10-23T14:28:08.106613615Z",
  "caller": "controller/controller.go:474",
  "msg": "Reconciler error",
  "controller": "job",
  "controllerGroup": "batch",
  "controllerKind": "Job",
  "Job": {
    "name": "test-duplicate-env",
  },
  "namespace": "default",
  "name": "test-duplicate-env",
  "reconcileID": "c2f78148-ad97-4f69-a75e-f775eb91bc8d",
  "error": "Workload.kueue.x-k8s.io \"job-test-duplicate-env-0ee7d\" is invalid: spec.podSets[0].template.spec.containers[0].env[1]: Duplicate value: map[string]interface {}{\"name\":\"TEST_VAR\"}",
  "stacktrace": "sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).reconcileHandler\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:474\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).processNextWorkItem\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:421\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).Start.func1.1\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:296"
}
```

Thanks for the quick response. Happy to provide further details if necessary!

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-10-23T15:11:25Z

I found easier solution how to catch it:

```yaml
apiVersion: kueue.x-k8s.io/v1beta1
kind: Workload
metadata:
  name: sample-job
spec:
  active: true
  queueName: team-a-queue
  podSets:
    - count: 3
      name: main
      template:
        spec:
          containers:
            - name: container
              image: registry.k8s.io/e2e-test-images/agnhost:latest
              args: ["pause"]
              imagePullPolicy: Always
              resources:
                requests:
                  cpu: "1"
                  memory: 200Mi
              env:
                - name: DEMO
                  value: "Hello from the environment"
                - name: DEMO
                  value: "Such a sweet sorrow"
          restartPolicy: Never
```

```
The Workload "sample-job" is invalid: spec.podSets[0].template.spec.containers[0].env[1]: Duplicate value: {"name":"DEMO"}
```

The problem is caused by a duplicated environment variable. We can’t create the workload because of it, and an error occurs in the job framework reconciler. 

https://github.com/kubernetes-sigs/kueue/blob/178155c7eadd36393cecb5da349995c946918b78/pkg/controller/jobframework/reconciler.go#L1378-L1380

```
{"level":"error","ts":"2025-10-23T14:42:57.846072599Z","caller":"jobframework/reconciler.go:481","msg":"Handling job with no workload","controller":"job","controllerGroup":"batch","controllerKind":"Job","Job":{"name":"sample-job","namespace":"default"},"namespace":"default","name":"sample-job","reconcileID":"511efb60-60bc-44ac-8780-d371117e320c","job":"default/sample-job","gvk":"batch/v1, Kind=Job","error":"Workload.kueue.x-k8s.io \"job-sample-job-ef531\" is invalid: spec.podSets[0].template.spec.containers[0].env[1]: Duplicate value: {\"name\":\"DEMO\"}","stacktrace":"sigs.k8s.io/kueue/pkg/controller/jobframework.(*JobReconciler).ReconcileGenericJob\n\t/workspace/pkg/controller/jobframework/reconciler.go:481\nsigs.k8s.io/kueue/pkg/controller/jobframework.(*genericReconciler).Reconcile\n\t/workspace/pkg/controller/jobframework/reconciler.go:1485\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).Reconcile\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:216\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).reconcileHandler\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:461\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).processNextWorkItem\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:421\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).Start.func1.1\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:296"}
{"level":"error","ts":"2025-10-23T14:42:57.846366808Z","caller":"controller/controller.go:474","msg":"Reconciler error","controller":"job","controllerGroup":"batch","controllerKind":"Job","Job":{"name":"sample-job","namespace":"default"},"namespace":"default","name":"sample-job","reconcileID":"511efb60-60bc-44ac-8780-d371117e320c","error":"Workload.kueue.x-k8s.io \"job-sample-job-ef531\" is invalid: spec.podSets[0].template.spec.containers[0].env[1]: Duplicate value: {\"name\":\"DEMO\"}","stacktrace":"sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).reconcileHandler\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:474\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).processNextWorkItem\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:421\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).Start.func1.1\n\t/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:296"}
```

It might not be the best solution, but it could work if we remove duplicated environment variables in the mutation webhook and keep only the last one.

### Comment by [@bd-hhause](https://github.com/bd-hhause) — 2025-10-23T15:20:27Z

@mbobrovskyi I'm also looking at removing the duplicate env var from the controller creating the spec. My question is: is it even Kueue's responsibility to handle this? Is the duplicate key something that should be handled by all controllers? I couldn't find any good answer on this.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-10-23T15:23:57Z

Yeah, this should also work, but I think it’s better to add it here:

https://github.com/kubernetes-sigs/kueue/blob/178155c7eadd36393cecb5da349995c946918b78/pkg/webhooks/workload_webhook.go#L60-L73

### Comment by [@LucasZanellaMBTI](https://github.com/LucasZanellaMBTI) — 2025-10-27T07:45:37Z

@mimowo I was off and therefore couldn't participate recent discussion, sorry for that. Does it make sense to postpone our evaluation until open points got fixed/implmented?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-27T09:09:30Z

> Yeah, this should also work, but I think it’s better to add it here:

Workload webhook is one possible place, but probably even better in the code which prepares the workload to be created.

The good thing about this change is also that it should work fine both with patch and SSA.

This should work I think. We may also investigate the "Restore" code to try not overriding the original Job created by the user.

>  Does it make sense to postpone our evaluation until open points got fixed/implmented?

Yes, I think this is not going to fly currently, because the Workload creation is rejected early due to the CRD validation generated for the embedded PodTemplateSpec.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-30T08:11:26Z

The fix is already merged but not released yet, it will be part of 0.14.3 and 0.13.8 (tentatively planned today):
- https://github.com/kubernetes-sigs/kueue/issues/7435
- https://github.com/kubernetes-sigs/kueue/issues/7436

### Comment by [@mwysokin](https://github.com/mwysokin) — 2025-11-04T13:36:58Z

@LucasZanellaMBTI @bd-hhause I tested it today E2E with Kueue 0.14.3 and it worked correctly. I used the following yaml:

```yaml
apiVersion: batch/v1
kind: Job 
metadata:
  generateName: sleep-job-
  labels:
    kueue.x-k8s.io/queue-name: lq
spec:
  parallelism: 1
  completions: 1
  completionMode: Indexed
  template:
    spec:
      containers:
      - name: dummy-job
        image: ubuntu
        command: ["sleep"]
        args: ["600s"]
        env:
        - name: "A"
          value: "1"
        - name: "B"
          value: "1"
        - name: "A"
          value: "2"
        resources:
          requests:
            cpu: "0.1" 
          limits:
            cpu: "0.1"
      restartPolicy: Never
```

Result:

```bash
$ kubectl exec sleep-job-5qwcw-0-kglvt -- env | grep "A="
A=2
```

### Comment by [@vladmirtxrx](https://github.com/vladmirtxrx) — 2025-11-18T11:41:05Z

Issue still affects pods with duplicate port numbers (kueue 0.14.4):
```
 ports:                                                                                                                                                                                                                                                                             
        - containerPort: 8000                                                                                                                                                                                                                                                              
          name: http                                                                                                                                                                                                                                                                       
          protocol: TCP                                                                                                                                                                                                                                                                    
        - containerPort: 8000                                                                                                                                                                                                                                                              
          name: metrics                                                                                                                                                                                                                                                                    
          protocol: TCP                                                                                                                                                                                                                                                                    
        - containerPort: 5001                                                                                                                                                                                                                                                              
          name: grpc                                                                                                                                                                                                                                                                       
          protocol: TCP          
```
```
{"level":"error","ts":"2025-11-18T11:38:24.97681862Z","caller":"jobframework/reconciler.go:481","msg":"Handling job with no workload","controller":"v1_pod","namespace":"app-cvtryout","name":"modelwgpu-dogsftriton-0-modelwgpu-5768674df6-pd56m","reconcileID":"432ca6dc-ee63-441a-92c2-efab7f2d4775","job":"app-cvtryout/modelwgpu-dogsftriton-0-modelwgpu-5768674df6-pd56m","gvk":"/v1, Kind=Pod","error":"Workload.kueue.x-k8s.io "pod-modelwgpu-dogsftriton-0-modelwgpu-5768674df6-pd56m-27c03" is invalid: spec.podSets[0].template.spec.containers[1].ports[1]: Duplicate value: map[string]interface {}{"containerPort":8000, "protocol":"TCP"}","stacktrace":"sigs.k8s.io/kueue/pkg/controller/jobframework.(*JobReconciler).ReconcileGenericJob
	/workspace/pkg/controller/jobframework/reconciler.go:481
sigs.k8s.io/kueue/pkg/controller/jobs/pod.(*Reconciler).Reconcile
	/workspace/pkg/controller/jobs/pod/pod_controller.go:117
sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).Reconcile
	/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:216
sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).reconcileHandler
	/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:461
sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).processNextWorkItem
	/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:421
sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller[...]).Start.func1.1
	/workspace/vendor/sigs.k8s.io/controller-runtime/pkg/internal/controller/controller.go:296"}      
```
