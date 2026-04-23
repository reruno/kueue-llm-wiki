# Issue #5558: [Deflake] Stop checking  TAS NodeToReplaceAnnotation directly in test code

**Summary**: [Deflake] Stop checking  TAS NodeToReplaceAnnotation directly in test code

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5558

**Last updated**: 2025-06-10T07:46:25Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-06-09T07:51:12Z
- **Updated**: 2025-06-10T07:46:25Z
- **Closed**: 2025-06-10T07:46:25Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@pajakd](https://github.com/pajakd)
- **Comments**: 5

## Description

/kind flake

**What happened**:

The tests are flaky and time sensitive. 

The issue with the asserts on NodeToReplaceAnnotation  is that when the node is replaced then the annotation is removed. 

**What you expected to happen**:

No failures when 1s sleep is injected . Ideally we don't have any integration and e2e tests which check NodeToReplaceAnnotation directly. Instead, we should observe the behavior that the node is changed.

**How to reproduce it (as minimally and precisely as possible)**:

To show that just inject time.Sleep(1s) from [here](https://github.com/kubernetes-sigs/kueue/blob/main/test/integration/singlecluster/tas/tas_test.go#L945) 

```
ginkgo.By("deleting the node", func() {
	nodeToUpdate := &corev1.Node{}
	gomega.Expect(k8sClient.Get(ctx, client.ObjectKey{Name: nodeName}, nodeToUpdate)).Should(gomega.Succeed())
	gomega.Expect(k8sClient.Delete(ctx, nodeToUpdate)).Should(gomega.Succeed())
})
  
time.Sleep(time.Second)

ginkgo.By("verify the workload has the NodeToReplaceAnnotation", func() {
	gomega.Eventually(func(g gomega.Gomega) {
		g.Expect(k8sClient.Get(ctx, client.ObjectKeyFromObject(wl1), wl1)).To(gomega.Succeed())
		g.Expect(wl1.Annotations).Should(gomega.HaveKeyWithValue(kueuealpha.NodeToReplaceAnnotation, nodeName))
	}, util.LongTimeout, util.Interval).Should(gomega.Succeed())
})
```

**Anything else we need to know?**:

I think the asserts where added as a temporary measures before setting the annotation was done as the first PR, and only then we added the node replacing. However, it is now important to cleanup the technical debt.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-09T07:51:43Z

cc @PBundyra @pajakd @mbobrovskyi @mszadkow

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-09T08:04:58Z

The additional flakiness in the test makes it really hard to debug https://github.com/kubernetes-sigs/kueue/issues/5511, similarly as https://github.com/kubernetes-sigs/kueue/issues/5559.

### Comment by [@pajakd](https://github.com/pajakd) — 2025-06-09T08:46:29Z

/assign

### Comment by [@pajakd](https://github.com/pajakd) — 2025-06-09T12:48:15Z

Not sure how to deal with e2e tests. The sole purpose of the tests "Should update nodesToReplace at the workload when a node fails" and "Should update nodesToReplace at the workload when a node is deleted" is to validate that the annotation behaves correctly upon node failure. We do have integration tests that cover this so perhaps the e2e tests are redundant. Instead, we should perhaps have e2e tests that checks the full functionality, wdyt?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-09T13:16:38Z

Yes, so currently the integration tests provide more coverage than e2e. 

I think ultimately we will want to have an e2e test for the feature which is true e2e, without checking the presence of the annotation as interim step.

I'm ok to drop the existing tests even for a time being until we have a proper test, given that in the current form the e2e cause non-obvious flakes in other tests, see: https://github.com/kubernetes-sigs/kueue/issues/5555#issuecomment-2954781126.
