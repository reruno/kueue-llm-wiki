# Issue #4861: Crash in the kueue-controller-manager with TAS enabled

**Summary**: Crash in the kueue-controller-manager with TAS enabled

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4861

**Last updated**: 2025-04-08T05:38:51Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@GonzaloSaez](https://github.com/GonzaloSaez)
- **Created**: 2025-04-03T06:36:03Z
- **Updated**: 2025-04-08T05:38:51Z
- **Closed**: 2025-04-08T05:38:49Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 12

## Description

Hi all,

I'm using kueue 0.11.1 with TAS enabled and I got several crashes today when I added a new node pool (GKE) to my cluster. I attach the stacktrace at the end of the bug report. My configuration is very simple. A topology defined as

```
apiVersion: kueue.x-k8s.io/v1beta1
kind: Topology
metadata:
  name: "topology-only-hostname"
name: "topology-only-hostname"
levels: ["kubernetes.io/hostname"]
```

and multiple RF using this topology. Any help is welcome here since I had to deactivate TAS to stop the crashes but that has consequences on the scheduling of my workloads. Thanks!


```
	panic: runtime error: index out of range [-1]

goroutine 1352 [running]:
k8s.io/apimachinery/pkg/util/runtime.handleCrash({0x32a99a0, 0x4de3320}, {0x2c1e080, 0xc00183a0f0}, {0x4de3320, 0x0, 0x100000000440f18?})
	/workspace/vendor/k8s.io/apimachinery/pkg/util/runtime/runtime.go:89 +0xe7
k8s.io/apimachinery/pkg/util/runtime.HandleCrash({0x0, 0x0, 0xc0015c9dc0?})
	/workspace/vendor/k8s.io/apimachinery/pkg/util/runtime/runtime.go:59 +0x105
panic({0x2c1e080?, 0xc00183a0f0?})
	/usr/local/go/src/runtime/panic.go:787 +0x132
sigs.k8s.io/kueue/pkg/cache.(*TASFlavorSnapshot).lowestLevel(...)
	/workspace/pkg/cache/tas_flavor_snapshot.go:166
sigs.k8s.io/kueue/pkg/cache.(*TASFlavorSnapshot).isLowestLevelNode(...)
	/workspace/pkg/cache/tas_flavor_snapshot.go:162
sigs.k8s.io/kueue/pkg/cache.(*TASFlavorSnapshot).addNode(_, {{{0x25aa53f, 0x4}, {0x2e2d19a, 0x2}}, {{0xc0004a43c0, 0x20}, {0x0, 0x0}, {0x0, ...}, ...}, ...})
	/workspace/pkg/cache/tas_flavor_snapshot.go:141 +0x7bf
sigs.k8s.io/kueue/pkg/cache.(*TASFlavorCache).snapshotForNodes(0xc0016a7f00, {{0x32b4dd0?, 0xc0021e7d40?}, 0x0?}, {0xc0003cc008, 0x4, 0x4?}, {0xc001dac000, 0xf1, 0xf1})
	/workspace/pkg/cache/tas_flavor.go:127 +0x785
sigs.k8s.io/kueue/pkg/cache.(*TASFlavorCache).snapshot(0xc0016a7f00, {0x32a98c0, 0xc0021e7ad0})
	/workspace/pkg/cache/tas_flavor.go:115 +0x68e
sigs.k8s.io/kueue/pkg/cache.(*Cache).Snapshot(0xc0002544b0, {0x32a98c0, 0xc0021e7ad0})
	/workspace/pkg/cache/snapshot.go:127 +0x505
sigs.k8s.io/kueue/pkg/scheduler.(*Scheduler).schedule(0xc00025ae60, {0x32a98c0, 0xc0021e7a10})
	/workspace/pkg/scheduler/scheduler.go:191 +0x21b
sigs.k8s.io/kueue/pkg/util/wait.untilWithBackoff.func1()
	/workspace/pkg/util/wait/backoff.go:43 +0x2b
k8s.io/apimachinery/pkg/util/wait.BackoffUntil.func1(0xc00147b380?)
	/workspace/vendor/k8s.io/apimachinery/pkg/util/wait/backoff.go:226 +0x33
k8s.io/apimachinery/pkg/util/wait.BackoffUntil(0xc001b8ff30, {0x3274620, 0xc00147b380}, 0x0, 0xc00183e4d0)
	/workspace/vendor/k8s.io/apimachinery/pkg/util/wait/backoff.go:227 +0xaf
sigs.k8s.io/kueue/pkg/util/wait.untilWithBackoff({0x32a98c0, 0xc0021e7a10}, 0xc000a94a50, {0x329e7f0, 0xc000080a48})
	/workspace/pkg/util/wait/backoff.go:42 +0xd3
sigs.k8s.io/kueue/pkg/util/wait.UntilWithBackoff({0x32a98c0, 0xc0021e7a10}, 0xc000a94a50)
	/workspace/pkg/util/wait/backoff.go:34 +0x8c
created by sigs.k8s.io/kueue/pkg/scheduler.(*Scheduler).Start in goroutine 1348
	/workspace/pkg/scheduler/scheduler.go:146 +0x131
```

## Discussion

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-04-03T07:51:22Z

Hey @GonzaloSaez, please make sure your topology is defined like [this in the example](https://github.com/kubernetes-sigs/kueue/blob/8b63e005815d8dd48d4d38de0ffe9472d29507c5/site/static/examples/tas/sample-queues.yaml#L6)

I think levels should be defined in "spec.Levels" and more like this:
```
apiVersion: kueue.x-k8s.io/v1alpha1
kind: Topology
metadata:
  name: "topology-only-hostname"
spec:
  levels:
  - nodeLabel: "kubernetes.io/hostname"
```

### Comment by [@GonzaloSaez](https://github.com/GonzaloSaez) — 2025-04-03T08:06:10Z

Hi @mszadkow thanks for the quick answer the problem is that it's not possible to use v1alpha1 in kueue 0.11.1 due to https://github.com/kubernetes-sigs/kueue/issues/4850

### Comment by [@GonzaloSaez](https://github.com/GonzaloSaez) — 2025-04-03T08:10:46Z

Also it seems that the v1beta1 API was released with v0.11 so I'm wondering why can't we rely on it to create the topology CRDs?

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-04-03T08:28:24Z

Ok, I see, so there is another issue that needs to be resolved - like you have mentioned.
Because there is no different `kueue.x-k8s.io/v1beta1` version of `Topology`.
The one you can find in `kueue.x-k8s.io/v1beta1` is for `LocalQueue` internals.

### Comment by [@GonzaloSaez](https://github.com/GonzaloSaez) — 2025-04-03T08:50:37Z

If I don't use the helm chart I seem to be able to create v1alpha1 topologies, however they get upgraded to v1beta1 upon creation and then I no longer see the levels in the CRD with kubectl. Is this expected? I'm a bit confused by these two API versions sorry!

### Comment by [@GonzaloSaez](https://github.com/GonzaloSaez) — 2025-04-03T09:05:58Z

See the following

```
apiVersion: kueue.x-k8s.io/v1beta1
kind: Topology
metadata:
  annotations:
    kubectl.kubernetes.io/last-applied-configuration: |
      {"apiVersion":"kueue.x-k8s.io/v1alpha1","kind":"Topology","metadata":{"annotations":{},"name":"try-topology-v1"},"spec":{"levels":[{"nodeLabel":"cloud.provider.com/topology-rack"},{"nodeLabel":"kubernetes.io/hostname"}]}}
  creationTimestamp: "2025-04-03T09:04:29Z"
  generation: 1
  name: try-topology-v1
  resourceVersion: "275389195"
  uid: dddaea05-df08-4caa-ab85-07289bd1e659
```

After applying

```
apiVersion: kueue.x-k8s.io/v1alpha1
kind: Topology
metadata:
  name: "try-topology-v1"
spec:
  levels:
  - nodeLabel: "cloud.provider.com/topology-rack"
  - nodeLabel: "kubernetes.io/hostname"
```

### Comment by [@mimowo](https://github.com/mimowo) — 2025-04-03T09:29:41Z

Yeah, this is weird. Topology is alpha API still. It looks like you have some conversion webhook in your cluster which mutates it to v1beta1, but I think this will not work well. We are considering graduation to beta for 0.12, maybe 0.13.

### Comment by [@GonzaloSaez](https://github.com/GonzaloSaez) — 2025-04-03T09:42:06Z

Thanks for the investigation! I cannot find the mutating webhook that could be causing this. The following is empty and the conversion field in the topology CRD is set to None

```
kubectl describe mutatingwebhookconfigurations kueue-mutating-webhook-configuration | grep topolog
```

### Comment by [@GonzaloSaez](https://github.com/GonzaloSaez) — 2025-04-03T09:55:45Z

Okay this seems to be happening as well because we serve the v1beta1 CRD but we store the alpha1 it seems

```
    served: true
    storage: false
```

### Comment by [@GonzaloSaez](https://github.com/GonzaloSaez) — 2025-04-03T10:21:14Z

I fixed this by disabling the TAS feature gate and then manually changing the CRD to conform to the v1alpha1 schema. I tried using v1beta1 due to https://github.com/kubernetes-sigs/kueue/issues/4850 and that's what caused all these issues. I wonder if we should keep the discussion in https://github.com/kubernetes-sigs/kueue/issues/4850 or if we should discuss further whether the v1beta1 API should be hidden or disallowed?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-04-08T05:38:45Z

/close
Assuming the root cause is fixed by https://github.com/kubernetes-sigs/kueue/pull/4866 which is already cherry picked to 0.11.3. Feel free to reopen if more work is needed.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-04-08T05:38:50Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4861#issuecomment-2785278430):

>/close
>Assuming the root cause is fixed by https://github.com/kubernetes-sigs/kueue/pull/4866 which is already cherry picked to 0.11.3. Feel free to reopen if more work is needed.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
