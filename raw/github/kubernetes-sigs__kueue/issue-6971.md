# Issue #6971: Kueue 0.13.4 has OOM issue with 18Gi config in kueue controller

**Summary**: Kueue 0.13.4 has OOM issue with 18Gi config in kueue controller

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6971

**Last updated**: 2025-09-29T20:24:52Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@nuonuoli2009](https://github.com/nuonuoli2009)
- **Created**: 2025-09-23T20:22:50Z
- **Updated**: 2025-09-29T20:24:52Z
- **Closed**: 2025-09-29T20:24:51Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 21

## Description


**What happened**:
We upgrade Kueue from 0.12.8 to 0.13.4
and the after the upgrade deployed, the kueue controller pods CrashLoopBackOff with error OOM. We config the kueue controller version to 18Gi. After we change it to 36Gi, it works fine. 18Gi is pretty big memory and we wonder if there is memory leaking in the new version 

**What you expected to happen**:
the kueue control pod could run within 1 GB memory 

**How to reproduce it (as minimally and precisely as possible)**:

upgrade the kueue version from 0.12.8 to 0.13.4 

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`): 
Client Version: v1.32.2
Kustomize Version: v5.5.0
Server Version: v1.32.7-eks-b707fbb
- Kueue version (use `git describe --tags --dirty --always`): registry.k8s.io/kueue/kueue:v0.13.4
- Cloud provider or hardware configuration: EKS
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@amy](https://github.com/amy) — 2025-09-23T20:24:14Z

/cc

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-09-24T03:03:47Z

Thanks for reporting that.
@nuonuoli2009 Are you able to share the kueue-controller-manager logs when you hit the OOM issue?

### Comment by [@nuonuoli2009](https://github.com/nuonuoli2009) — 2025-09-24T05:27:37Z



> Thanks for reporting that. [@nuonuoli2009](https://github.com/nuonuoli2009) Are you able to share the kueue-controller-manager logs when you hit the OOM issue?

Thanks for checking. Unfortunately, there is no logs from the OOM controller pod

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-24T05:43:13Z

After you bumped memory to 36Gi what is your usage? Also is it increasing gradually or stable at high level.

### Comment by [@nuonuoli2009](https://github.com/nuonuoli2009) — 2025-09-24T05:48:16Z

> After you bumped memory to 36Gi what is your usage? Also is it increasing gradually or stable at high level.

first we config it as 18Gi and it crushed immediately right after the pod deployed without any logs and we config it to 36Gi to resolve the OOM issue. But it does not make sense to use 18 GI memory

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-24T06:00:16Z

Well depends on the size of your deployment, and features enabled. For example Pod integration or TAS I imagine are mem hungry, because for these features controller-runtime maintains a cache of all Pods.

Also what our users hit in the past is that finished workloads accumulated over time. This we now recommend to setup the ObjectRetentionapolicy.

It would be helpful to know
1. how much memory is actually used (not declared in requests)
2. did the memory requirements bump after upgrade? How much memory was enough before upgrade

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-24T06:00:33Z

cc @mwysokin

### Comment by [@mwysokin](https://github.com/mwysokin) — 2025-09-24T14:00:44Z

@nuonuoli2009 Thanks for letting us now about this! We'll be running our MegaCluster GKE scale tests with Kueue this week to compare the last 3 releases (.12, .13 and upcoming .14). We can probably share some report about the outcome. So far we're not aware of any memory leaks or issues related to increased memory consumption.

Could you maybe share some more data about memory consumption in 0.12 and now in 0.13? Has anything else changed in your infrastructure? Was the memory consumption trending up? Or was it stable and suddenly went up?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-09-24T14:02:21Z

@nuonuoli2009 Indeed, we enabled Hierarchical Cohort (Cohort API) by default in v0.13.
So, can you disable the `HierarchicalCohort` feature gate to follow https://kueue.sigs.k8s.io/docs/installation/#change-the-feature-gates-configuration so that we can confirm that the Cohort-associated features do not raise a memory leak?

### Comment by [@amy](https://github.com/amy) — 2025-09-24T15:55:49Z

At the time of this test these were the feature flags: `--feature-gates=PrioritySortingWithinCohort=false,VisibilityOnDemand=false,MultiplePreemptions=true,FlavorFungibilityImplicitPreferenceDefault=true`

We can try explicitly turning off `HierarchicalCohort` as a test.

### Comment by [@nuonuoli2009](https://github.com/nuonuoli2009) — 2025-09-24T18:57:53Z

@tenzen-y it looks HierarchicalCohort	true	Beta	0.11	 
enabled since 0.11. Is that true ? 

<img width="630" height="52" alt="Image" src="https://github.com/user-attachments/assets/6da22ae3-707d-42f0-aee4-3f32976163ec" />

### Comment by [@nuonuoli2009](https://github.com/nuonuoli2009) — 2025-09-25T16:55:48Z

The memory in version 0.12  is under 1Gi and in the version 0.13.4 it crushed immediately and It is hard to catch how much memory it is using.

### Comment by [@amy](https://github.com/amy) — 2025-09-25T20:40:50Z

We can't explicitly turn off HierarchicalCohort because its in GA now and is no longer recognized as a featuregate (ie the pod will crashloopbackoff with an error about the featuregate not being valid). We've turned on pprof. Also fixing some metrics so that we can see overall historical memory usage for the pod (ie whether memory usage plateaus at some point). Will update with findings.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-09-25T21:32:20Z

Is it a cold start, i.e., w/out preexisting workloads in queues?

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-09-25T21:37:51Z

> At the time of this test these were the feature flags: `--feature-gates=PrioritySortingWithinCohort=false,VisibilityOnDemand=false,MultiplePreemptions=true,FlavorFungibilityImplicitPreferenceDefault=true`

Something just caught my eye, is `MultiplePreemptions=true` a valid feature gate for `v0.13.4`?

### Comment by [@amy](https://github.com/amy) — 2025-09-26T17:36:50Z

> Is it a cold start, i.e., w/out preexisting workloads in queues?

No. This is running in a dev cluster. So whatever the dev cluster current state is, it is loading into the controller.

---
Comparison of 0.12.8 vs. 0.13.4 memory patterns:
- `0.13.4` spikes up to 23Gi on startup, falls down and stabilizes to about 4Gi
- `0.12.8` spikes up to about 5Gi on startup, falls down to and stabilizes to about 3Gi

⭐️ So something definitely changed.

---
Next, here's what I do for 0.13.4 and 0.12.8
1. pprof of stable state (after spike)
2. pprof of spiked state
3. take a trace of the top offender during spiked state

0.13.4 stable state, hovering around 5Gi
```
(pprof) top
Showing nodes accounting for 2GB, 83.02% of 2.40GB total
Dropped 295 nodes (cum <= 0.01GB)
Showing top 10 nodes out of 91
      flat  flat%   sum%        cum   cum%
    0.49GB 20.22% 20.22%     0.49GB 20.22%  k8s.io/apimachinery/pkg/apis/meta/v1.(*FieldsV1).Unmarshal
    0.46GB 19.31% 39.53%     1.02GB 42.54%  k8s.io/api/core/v1.(*PodSpec).Unmarshal
    0.27GB 11.07% 50.60%     0.80GB 33.46%  k8s.io/apimachinery/pkg/apis/meta/v1.(*ObjectMeta).Unmarshal
    0.21GB  8.62% 59.21%     0.25GB 10.36%  k8s.io/api/core/v1.(*PodStatus).Unmarshal
    0.18GB  7.58% 66.79%     0.18GB  7.58%  reflect.New
    0.14GB  5.99% 72.78%     0.32GB 13.36%  k8s.io/api/core/v1.(*Container).Unmarshal
    0.12GB  4.86% 77.64%     0.12GB  4.86%  k8s.io/api/core/v1.(*ResourceRequirements).Unmarshal
    0.07GB  2.80% 80.44%     0.07GB  2.80%  k8s.io/api/core/v1.(*Toleration).Unmarshal
    0.04GB  1.58% 82.02%     0.52GB 21.81%  k8s.io/apimachinery/pkg/apis/meta/v1.(*ManagedFieldsEntry).Unmarshal
    0.02GB  0.99% 83.02%     0.02GB  0.99%  k8s.io/api/core/v1.(*PodCondition).Unmarshal
```
0.13.4 spiked startup state, hovering around 23Gi
```
(pprof) top
Showing nodes accounting for 11.32GB, 99.66% of 11.36GB total
Dropped 172 nodes (cum <= 0.06GB)
Showing top 10 nodes out of 33
      flat  flat%   sum%        cum   cum%
    5.87GB 51.70% 51.70%     5.87GB 51.70%  go.uber.org/zap/buffer.(*Buffer).AppendString
    4.38GB 38.55% 90.25%     4.38GB 38.55%  strings.(*Builder).grow
    1.07GB  9.41% 99.66%     1.07GB  9.41%  io.ReadAll
         0     0% 99.66%     4.38GB 38.55%  encoding/hex.Dump
         0     0% 99.66%     5.87GB 51.70%  github.com/go-logr/logr.Logger.Info
         0     0% 99.66%     5.87GB 51.70%  github.com/go-logr/zapr.(*zapLogger).Info
         0     0% 99.66%     5.87GB 51.70%  go.uber.org/zap/zapcore.(*CheckedEntry).Write
         0     0% 99.66%     5.87GB 51.70%  go.uber.org/zap/zapcore.(*ioCore).Write
         0     0% 99.66%     5.87GB 51.70%  go.uber.org/zap/zapcore.(*jsonEncoder).AddString
         0     0% 99.66%     5.87GB 51.70%  go.uber.org/zap/zapcore.(*jsonEncoder).AppendString
```
sample trace starting with go.uber.org/zap/buffer.(*Buffer).AppendString
```
     bytes:  3.26GB
    3.26GB   go.uber.org/zap/buffer.(*Buffer).AppendString
             go.uber.org/zap/zapcore.safeAppendStringLike[go.shape.string]
             go.uber.org/zap/zapcore.(*jsonEncoder).safeAddString (inline)
             go.uber.org/zap/zapcore.(*jsonEncoder).AppendString
             go.uber.org/zap/zapcore.(*jsonEncoder).AddString
             go.uber.org/zap/zapcore.Field.AddTo
             go.uber.org/zap/zapcore.addFields (inline)
             go.uber.org/zap/zapcore.(*jsonEncoder).EncodeEntry
             sigs.k8s.io/controller-runtime/pkg/log/zap.(*KubeAwareEncoder).EncodeEntry
             go.uber.org/zap/zapcore.(*ioCore).Write
             go.uber.org/zap/zapcore.(*CheckedEntry).Write
             github.com/go-logr/zapr.(*zapLogger).Info
             sigs.k8s.io/controller-runtime/pkg/log.(*delegatingLogSink).Info
             github.com/go-logr/logr.Logger.Info
             k8s.io/client-go/rest.logBody
             k8s.io/client-go/rest.(*Request).transformResponse
             k8s.io/client-go/rest.(*Request).Do.func1
             k8s.io/client-go/rest.(*Request).request.func3.1 (inline)
             k8s.io/client-go/rest.(*Request).request.func3
             k8s.io/client-go/rest.(*Request).request
             k8s.io/client-go/rest.(*Request).Do
             sigs.k8s.io/controller-runtime/pkg/cache/internal.(*Informers).makeListWatcher.func5
             sigs.k8s.io/controller-runtime/pkg/cache/internal.(*Informers).addInformerToMap.func1
             k8s.io/client-go/tools/cache.(*ListWatch).ListWithContext
             k8s.io/client-go/tools/cache.(*Reflector).list.func1.2
             k8s.io/client-go/tools/cache.(*Reflector).list.func1.SimplePageFunc.3
             k8s.io/client-go/tools/pager.(*ListPager).list
             k8s.io/client-go/tools/pager.(*ListPager).ListWithAlloc (inline)
             k8s.io/client-go/tools/cache.(*Reflector).list.func1
```
0.12.8 stable state, hovering around 3Gi 
```
(pprof) top
Showing nodes accounting for 1947.88MB, 82.24% of 2368.56MB total
Dropped 251 nodes (cum <= 11.84MB)
Showing top 10 nodes out of 97
      flat  flat%   sum%        cum   cum%
  501.51MB 21.17% 21.17%   501.51MB 21.17%  k8s.io/apimachinery/pkg/apis/meta/v1.(*FieldsV1).Unmarshal
  421.39MB 17.79% 38.96%   974.50MB 41.14%  k8s.io/api/core/v1.(*PodSpec).Unmarshal
  257.54MB 10.87% 49.84%   823.55MB 34.77%  k8s.io/apimachinery/pkg/apis/meta/v1.(*ObjectMeta).Unmarshal
  193.65MB  8.18% 58.01%   232.66MB  9.82%  k8s.io/api/core/v1.(*PodStatus).Unmarshal
  170.18MB  7.19% 65.20%   170.18MB  7.19%  reflect.New
  140.03MB  5.91% 71.11%   317.10MB 13.39%  k8s.io/api/core/v1.(*Container).Unmarshal
  118.07MB  4.98% 76.10%   118.07MB  4.98%  k8s.io/api/core/v1.(*ResourceRequirements).Unmarshal
   63.50MB  2.68% 78.78%    63.50MB  2.68%  k8s.io/api/core/v1.(*Toleration).Unmarshal
      50MB  2.11% 80.89%   551.51MB 23.28%  k8s.io/apimachinery/pkg/apis/meta/v1.(*ManagedFieldsEntry).Unmarshal
      32MB  1.35% 82.24%   131.01MB  5.53%  k8s.io/api/core/v1.(*VolumeSource).Unmarshal
```
0.12.8 spiked startup state, hovering around 5Gi
```
(pprof) top
Showing nodes accounting for 2114.76MB, 78.80% of 2683.57MB total
Dropped 291 nodes (cum <= 13.42MB)
Showing top 10 nodes out of 121
      flat  flat%   sum%        cum   cum%
  483.47MB 18.02% 18.02%   483.47MB 18.02%  k8s.io/apimachinery/pkg/apis/meta/v1.(*FieldsV1).Unmarshal
  463.43MB 17.27% 35.29%  1011.04MB 37.68%  k8s.io/api/core/v1.(*PodSpec).Unmarshal
  286.05MB 10.66% 45.94%   829.03MB 30.89%  k8s.io/apimachinery/pkg/apis/meta/v1.(*ObjectMeta).Unmarshal
  196.15MB  7.31% 53.25%   228.65MB  8.52%  k8s.io/api/core/v1.(*PodStatus).Unmarshal
  171.19MB  6.38% 59.63%   171.19MB  6.38%  reflect.New
  148.87MB  5.55% 65.18%   149.38MB  5.57%  io.ReadAll
  142.03MB  5.29% 70.47%   322.10MB 12.00%  k8s.io/api/core/v1.(*Container).Unmarshal
  117.56MB  4.38% 74.85%   117.56MB  4.38%  k8s.io/api/core/v1.(*ResourceRequirements).Unmarshal
   56.50MB  2.11% 76.96%    56.50MB  2.11%  k8s.io/api/core/v1.(*Toleration).Unmarshal
   49.50MB  1.84% 78.80%   532.98MB 19.86%  k8s.io/apimachinery/pkg/apis/meta/v1.(*ManagedFieldsEntry).Unmarshal
```
sample trace for k8s.io/apimachinery/pkg/apis/meta/v1.(*FieldsV1).Unmarshal
```
     bytes:  8kB
    1.51MB   k8s.io/apimachinery/pkg/apis/meta/v1.(*FieldsV1).Unmarshal
             k8s.io/apimachinery/pkg/apis/meta/v1.(*ManagedFieldsEntry).Unmarshal
             k8s.io/apimachinery/pkg/apis/meta/v1.(*ObjectMeta).Unmarshal
             k8s.io/api/core/v1.(*Pod).Unmarshal
             k8s.io/api/core/v1.(*PodList).Unmarshal
             k8s.io/api/core/v1.(*PodList).XXX_Unmarshal
             github.com/gogo/protobuf/proto.Unmarshal
             k8s.io/apimachinery/pkg/runtime/serializer/protobuf.unmarshalToObject
             k8s.io/apimachinery/pkg/runtime/serializer/protobuf.(*Serializer).Decode
             k8s.io/apimachinery/pkg/runtime.WithoutVersionDecoder.Decode
             sigs.k8s.io/controller-runtime/pkg/client/apiutil.targetZeroingDecoder.Decode
             k8s.io/client-go/rest.Result.Into
             sigs.k8s.io/controller-runtime/pkg/cache/internal.(*Informers).makeListWatcher.func5
             sigs.k8s.io/controller-runtime/pkg/cache/internal.(*Informers).addInformerToMap.func1
             k8s.io/client-go/tools/cache.(*ListWatch).List
             k8s.io/client-go/tools/cache.(*Reflector).list.func1.2
             k8s.io/client-go/tools/cache.(*Reflector).list.func1.SimplePageFunc.3
             k8s.io/client-go/tools/pager.(*ListPager).list
             k8s.io/client-go/tools/pager.(*ListPager).ListWithAlloc (inline)
             k8s.io/client-go/tools/cache.(*Reflector).list.func1
```

### Comment by [@amy](https://github.com/amy) — 2025-09-27T01:36:48Z

Found it:
`logBody` gets used when zap logging is 8+, we have ours set to 10. When I change logging level down to 3, `0.13.4` gets spiked to only 5Gi. 

Looks like level 8 will log http request/responses. And you can follow the trace down to:  `k8s.io/client-go/tools/cache.(*ListWatch).ListWithContext` 

We can lower the log level to 7.

Curious about the significant difference between 0.13.4 and 0.12.8 in terms of cache informer list requests to api server. Because both `0.13.4` and `0.12.8` had logging verbosity set to `10`.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-29T09:12:15Z

@amy thank you for the analysis. Generally in Kueue we take the freedom to add verbose logs at V5+. Such high verbosity logs are not optimized for performance, and I would only focus during review making sure V2 and V3 are not verbose too much.

Still, there can be some bug / regression in the amount of logging in 0.13 and might be worth exploring. However, as you report there is a signifficant difference between V7 and V10. I couldn't find any logs produced by Kueue at this level, so I suppose it might be due to bumping dependencies such as controller-runtime or k8s itself.

### Comment by [@amy](https://github.com/amy) — 2025-09-29T16:35:29Z

Yeah not sure if its worth exploring or not. I'll create a followup issue just so we remember this happened in case something related in the future pops up. Maybe one concern is apiserver load on kueue controller restart.

### Comment by [@amy](https://github.com/amy) — 2025-09-29T20:24:46Z

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-09-29T20:24:52Z

@amy: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/6971#issuecomment-3348920037):

>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
