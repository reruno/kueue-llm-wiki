# Issue #5559: [Deflake] TAS integration test "should evict workload when multiple assigned nodes are deleted"

**Summary**: [Deflake] TAS integration test "should evict workload when multiple assigned nodes are deleted"

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5559

**Last updated**: 2025-06-09T13:00:31Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-06-09T08:03:56Z
- **Updated**: 2025-06-09T13:00:31Z
- **Closed**: 2025-06-09T13:00:31Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@pajakd](https://github.com/pajakd)
- **Comments**: 4

## Description

**What happened**:

The test fails locally when injecting small sleeps, or repeating the test many times. 

This is similar to https://github.com/kubernetes-sigs/kueue/issues/5558

**What you expected to happen**:

no failures, even if small sleeps injected or running under stress

**How to reproduce it (as minimally and precisely as possible)**:

inject sleep 1s sleep [here](https://github.com/kubernetes-sigs/kueue/blob/main/test/integration/singlecluster/tas/tas_test.go#L1177-L1194)

```golang
ginkgo.By("deleting the first assigned node: "+node1Name, func() {
	nodeToDelete := &corev1.Node{ObjectMeta: metav1.ObjectMeta{Name: node1Name}}
	gomega.Expect(k8sClient.Delete(ctx, nodeToDelete)).Should(gomega.Succeed())
	util.ExpectObjectToBeDeleted(ctx, k8sClient, nodeToDelete, false)
})

ginkgo.By("verify the workload has the NodeToReplaceAnnotation", func() {
	gomega.Eventually(func(g gomega.Gomega) {
		g.Expect(k8sClient.Get(ctx, client.ObjectKeyFromObject(wl1), wl1)).To(gomega.Succeed())
		g.Expect(wl1.Annotations).Should(gomega.HaveKeyWithValue(kueuealpha.NodeToReplaceAnnotation, node1Name))
	}, util.LongTimeout, util.Interval).Should(gomega.Succeed())
})

time.Sleep(time.Second)

ginkgo.By("deleting the second assigned node: "+node2Name, func() {
	nodeToDelete := &corev1.Node{ObjectMeta: metav1.ObjectMeta{Name: node2Name}}
	gomega.Expect(k8sClient.Delete(ctx, nodeToDelete)).Should(gomega.Succeed())
	util.ExpectObjectToBeDeleted(ctx, k8sClient, nodeToDelete, false)
})

ginkgo.By("verify the workload is evicted due to multiple node failures", func() {
```

**Anything else we need to know?**:

Failures requiring 1s sleep can easily happen on CI under load or when repeating the test multiple times. 

The additional flakiness in the test makes it really hard to debug https://github.com/kubernetes-sigs/kueue/issues/5511

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-09T08:04:13Z

cc @PBundyra @pajakd @mbobrovskyi @mszadkow

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-09T08:04:19Z

/kind flake

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-09T08:26:46Z

I think we should make sure there is no replacement for the first node, so that the second node, when failed triggers eviciton. To make sure there is no replacement for the first node, we could (some ideas, maybe there are other): 
1. use nodeSelectors in the workload so that it restricts TAS to only x1 or x2; 
2. increase the workload size so that it would use all nodes anyway (probably simplest), 
3. reduce the number of nodes so that there is no replacement.

### Comment by [@pajakd](https://github.com/pajakd) — 2025-06-09T10:53:53Z

/assign
