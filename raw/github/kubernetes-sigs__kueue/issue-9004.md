# Issue #9004: [Flaky] Topology Aware Scheduling when Single TAS Resource Flavor when Nodes are created before test with rack being the lowest level [It] should respect TAS usage by admitted workloads after reboot; second workload created before reboot

**Summary**: [Flaky] Topology Aware Scheduling when Single TAS Resource Flavor when Nodes are created before test with rack being the lowest level [It] should respect TAS usage by admitted workloads after reboot; second workload created before reboot

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9004

**Last updated**: 2026-02-09T11:35:26Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@IrvingMg](https://github.com/IrvingMg)
- **Created**: 2026-02-05T12:06:45Z
- **Updated**: 2026-02-09T11:35:26Z
- **Closed**: 2026-02-09T11:35:25Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@sohankunkerkar](https://github.com/sohankunkerkar)
- **Comments**: 3

## Description

<!--
Please use this template for reporting flaky tests.
Links to specific failures in Prow are appreciated.
-->

**Which test is flaking?**:

Topology Aware Scheduling when Single TAS Resource Flavor when Nodes are created before test with rack being the lowest level [It] should respect TAS usage by admitted workloads after reboot; second workload created before reboot

**First observed in** (PR or commit, if known):

https://github.com/kubernetes-sigs/kueue/pull/9002

**Link to failed CI job or steps to reproduce locally**:

https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/9002/pull-kueue-test-integration-extended-main/2019375797827014656

**Failure message or logs**:
```
 [FAILED] Timed out after 10.000s.
  The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/util/util.go:412 with:
  Unexpected workloads are admitted
  Expected
      <[]types.NamespacedName | len:0, cap:2>: []
  to equal
      <[]types.NamespacedName | len:2, cap:2>: [
          {
              Namespace: "tas-crjqh",
              Name: "wl2",
          },
          {
              Namespace: "tas-crjqh",
              Name: "wl3",
          },
      ]
  In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/integration/singlecluster/tas/tas_test.go:803 @ 02/05/26 12:00:19.175
```

**Anything else we need to know?**:

## Discussion

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-02-06T04:06:11Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-06T14:00:25Z

actually I was aware of the issue, this is why I put this hack
```golang
ginkgo.By("create wl3 to ensure ClusterQueue is reconciled", func() {
	wl3 = utiltestingapi.MakeWorkload("wl3", ns.Name).
		Queue(kueue.LocalQueueName(localQueue.Name)).Request(corev1.ResourceCPU, "1").Obj()
	wl3.Spec.PodSets[0].TopologyRequest = &kueue.PodSetTopologyRequest{
		Preferred: ptr.To(utiltesting.DefaultRackTopologyLevel),
	}
	util.MustCreate(ctx, k8sClient, wl3)
})
```
which is meant to make the failure less likely. 

So, I'm pretty sure that as you are working on the fix you can remove this block and it will allow you to expose the issue more often. This way you can confirm if the fix works by looping the test. I'm pretty sure 100 repeats will expose it if the block is removed.

Now, it is not a "big deal" issue, beacuse on a real producation system there will be many workloads, so some will trigger scheduling for sure. So we can as well just plumb the tests with the approach by calling QueueInadmissibleWorkloads  as done in "non-TAS pod terminates, releasing capacity".

Still, feel free to solve it properly, but then let's confirm the fix is working.

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-02-06T16:45:17Z

>Now, it is not a "big deal" issue, beacuse on a real producation system there will be many workloads, so some will trigger scheduling for sure. So we can as well just plumb the tests with the approach by calling QueueInadmissibleWorkloads as done in "non-TAS pod terminates, releasing capacity".

> Still, feel free to solve it properly, but then let's confirm the fix is working.

Ah, thanks for the background. Now it makes complete sense. I’d still lean toward fixing this the right way.
