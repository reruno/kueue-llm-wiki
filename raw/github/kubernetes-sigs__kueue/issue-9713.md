# Issue #9713: Pod groups when Single CQ Failed Pod can be replaced in group

**Summary**: Pod groups when Single CQ Failed Pod can be replaced in group

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9713

**Last updated**: 2026-03-12T07:05:40Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-03-06T12:46:16Z
- **Updated**: 2026-03-12T07:05:40Z
- **Closed**: 2026-03-12T07:05:40Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@sohankunkerkar](https://github.com/sohankunkerkar)
- **Comments**: 13

## Description

**Which test is flaking?**:

Pod groups when Single CQ Failed Pod can be replaced in group

**Link to failed CI job or steps to reproduce locally**:

https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-release-0-16-1-35/2029796010150072320

**Failure message or logs**:
```

End To End Suite: kindest/node:v1.35.0: [It] Pod groups when Single CQ Failed Pod can be replaced in group [area:singlecluster, feature:pod] expand_less	1m16s
{Timed out after 45.001s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/singlecluster/pod_test.go:230 with:
Expected
    <v1.PodPhase>: Running
to equal
    <v1.PodPhase>: Failed failed [FAILED] Timed out after 45.001s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/singlecluster/pod_test.go:230 with:
Expected
    <v1.PodPhase>: Running
to equal
    <v1.PodPhase>: Failed
In [It] at: /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/singlecluster/pod_test.go:231 @ 03/06/26 06:09:06.067
}
```

**Anything else we need to know?**:

Same build as https://github.com/kubernetes-sigs/kueue/issues/9714

## Discussion

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-03-06T20:53:51Z

/assign

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-03-09T06:15:30Z

I traced through the kubelet and containerd logs from the failed build. The container process exits within 20ms of receiving SIGTERM  (exitCode=2), but containerd gets stuck retrying task deletion with "context deadline exceeded" errors. The kubelet won't  transition the pod phase to Failed until containerd finishes cleanup, so the 45-second `LongTimeout` expires while the pod is still showing Running.                                                                                                                                        

This is the same root cause as #2729, #2885, and #4669 (containerd task cleanup latency in kind/DinD). Each previous fix bumped timeouts, but the problem keeps recurring because CI node pressure can push containerd delays beyond any reasonable timeout. I think we should remove the pod phase assertion entirely. The test's purpose is to verify Kueue's replacement logic, not containerd's  termination lifecycle. Instead of waiting for `pod.Status.Phase == Failed`, it should wait for Kueue's `WaitingForReplacementPods` condition. This decouples the test from containerd timing.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-09T06:44:18Z

@sohankunkerkar thank you for the analysis. Can we tell from the kubelet logs how long the termination took overall? 

This could give us ideas about alternatives:
1. bump timeout again, say by another 5-10s
2. increase CI job CPU, say bump another 10%

While you say those timeouts or Job CPU have already been bumped, I consider this a natural consequence of some changes we do. For example, since then we:
a) increased the number of operators (relatively recently added KubeRay or AppWrapper)
b) started to install the promethous operator
c) started to run e2e test in parallel

All of those could have justified another bump we didn't do.

Now, I'm not a fan of removing the assert for `pod.Status.Phase == Failed` and only relying on `WaitingForReplacementPods`, because: we are already checking `WaitingForReplacementPods` in the follow up assert with just 10s delay. Now we would need to increase the timeout here to say 1min. By decoupling the containerd assert and Kueue's logic assert we can currently have short assert on Kueue. Decoupling removes Kueue from suspects for failures like these. Assume we did that and the timeout was 1min. Now you need to analyze both containerd and Kueue logic which one is at fault.

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-03-09T12:08:50Z

Good point! From the kubelet logs, the container exited at 06:08:22 (20ms after SIGTERM) but the pod phase didn't reach Failed until 06:09:29 - a 67-seconds gap. The kubelet was logging `Delaying pod deletion as the phase is non-terminal` during that window, waiting for sandbox container cleanup.

How about bumping the timeout for the pod phase assertion to 90 seconds?

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-09T12:16:35Z

sgtm, the question how we name the new timeout. 
I'm thinking about:
- Timeout=10s, stays
- LongTimeout=45, stays
- VeryLongTimeout=3min -> reduced to 90min
- StartupTimeout stays
I think it is rare when we would need actually 3min, maybe never

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-03-09T14:41:01Z

I think the existing `VeryLongTimeout` callers are mostly KubeRay tests waiting for Ray image pulls (2GB+) and cluster startup. Dropping to 90s would likely break those. I'd suggest keeping VeryLongTimeout at 5min and adding a new constant instead like `PodLifecycleTimeout = 90 * time.Second`

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-09T15:00:14Z

Hm

> callers are mostly KubeRay tests waiting for Ray image pulls (2GB+) and cluster startup.

Oh, do we need that? I think this was the reason why we introduced the mini ray image, which is snappy - just 300mb or so. Maybe we just forgot to use it. 

>  I'd suggest keeping VeryLongTimeout at 5min and adding a new constant instead like PodLifecycleTimeout = 90 * time.Second

I'm not sure. Clearly we need something between LongTimeout and VeryLongTimeout, but I wouldn't couple to the test type. Similarly I don't like StartupTimout. 

I think ideally:
Timeout=10s
MidiumTimeout=45s
LongTimeout=2min
VeryLongTimeout=5min

would it be too many changes?

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-03-10T15:24:37Z

It's a big diff but zero risk since it's just constant renames.

Re: mini ray image - yes, most kuberay tests already use the mini image (ray:2.9.0-py310 ~300MB). The VeryLongTimeout usages there are for RayCluster startup (head + workers + Redis) rather than image pulls, which still takes time.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-10T15:28:07Z

> It's a big diff but zero risk since it's just constant renames.

That is my thinking. I'm ok with big renames totally. Let me also check this with @mbobrovskyi

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-03-10T16:03:23Z

Timeout = 10s (no changes)

Rename:
- LongTimeout → MediumTimeout (45s)
- VeryLongTimeout → LongTimeout (90s, is it sufficient?)
- StartupTimeout → VeryLongTimeout (5 min)

WDYT?

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-10T16:07:25Z

I think this is great, the 90s will be enough I think. this would also allow us to reduce some of the 5min timeouts currently (but as a follow up)

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-03-11T09:02:45Z

@sohankunkerkar do you want to create PR, or should I do it?

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-03-11T15:18:03Z

>@sohankunkerkar do you want to create PR, or should I do it?

working on it, will post the link here shortly.
