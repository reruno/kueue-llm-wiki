# Issue #6018: [flaky test] "Shouldn't admit deactivated Workload after manager restart"

**Summary**: [flaky test] "Shouldn't admit deactivated Workload after manager restart"

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6018

**Last updated**: 2025-07-18T12:34:26Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-07-18T11:29:35Z
- **Updated**: 2025-07-18T12:34:26Z
- **Closed**: 2025-07-18T12:34:26Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 2

## Description

/kind flake

**What happened**:

The test flaked on unrelated branch https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/5510/pull-kueue-test-integration-baseline-main/1946075894124646400

**What you expected to happen**:
no failures
**How to reproduce it (as minimally and precisely as possible)**:
ci
**Anything else we need to know?**:
```
{Failed after 0.015s.
The function passed to Consistently failed at /home/prow/go/src/sigs.k8s.io/kueue/test/integration/singlecluster/controller/jobs/job/job_controller_test.go:2132 with:
Expected
    <bool>: true
to be false failed [FAILED] Failed after 0.015s.
The function passed to Consistently failed at /home/prow/go/src/sigs.k8s.io/kueue/test/integration/singlecluster/controller/jobs/job/job_controller_test.go:2132 with:
Expected
    <bool>: true
to be false
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/integration/singlecluster/controller/jobs/job/job_controller_test.go:2135 @ 07/18/25 05:21:53.633
}
```

I suspect I know why it fails, check the test code

```golang
		ginkgo.By("Checking that the Workload is admitted", func() {
			gomega.Eventually(func(g gomega.Gomega) {
				g.Expect(k8sClient.Get(ctx, wlKey, wl)).To(gomega.Succeed())
				g.Expect(workload.IsAdmitted(wl)).To(gomega.BeTrue())
			}, util.Timeout, util.Interval).Should(gomega.Succeed())
			util.ExpectAdmittedWorkloadsTotalMetric(prodClusterQ, 1)
		})

		ginkgo.By("Deactivate the Workload", func() {
			gomega.Eventually(func(g gomega.Gomega) {
				g.Expect(k8sClient.Get(ctx, wlKey, wl)).To(gomega.Succeed())
				wl.Spec.Active = ptr.To(false)
				g.Expect(k8sClient.Update(ctx, wl)).To(gomega.Succeed())
			}, util.Timeout, util.Interval).Should(gomega.Succeed())
		})

		ginkgo.By("Checking that the Workload is deactivated and evicted", func() {
			gomega.Eventually(func(g gomega.Gomega) {
				g.Expect(k8sClient.Get(ctx, wlKey, wl)).To(gomega.Succeed())
				g.Expect(workload.IsActive(wl)).To(gomega.BeFalse())
				g.Expect(workload.IsEvicted(wl)).To(gomega.BeTrue()) 
			}, util.Timeout, util.Interval).Should(gomega.Succeed())
		})

		ginkgo.By("Restarting the manager", func() {
			restartManager()
		})

		ginkgo.By("Checking that the Workload is not admitted after restart the manager", func() {
			gomega.Consistently(func(g gomega.Gomega) {
				g.Expect(k8sClient.Get(ctx, wlKey, wl)).To(gomega.Succeed())
				g.Expect(workload.IsAdmitted(wl)).To(gomega.BeFalse())   # <------- line which failed
				g.Expect(workload.IsEvicted(wl)).To(gomega.BeTrue())
				// Using short intervals to make it likely to fail if the conditions flip
			}, util.ConsistentDuration, util.ShortInterval).Should(gomega.Succeed())
			// NOTE: controller restart in integration tests does not reset the metrics
			util.ExpectAdmittedWorkloadsTotalMetric(prodClusterQ, 1)
		})
```
I think it fails at "# <------- line which failed" because the process of Eviction is two-step: first the Evicted condition is added, then the Admitted and QuotaReserved conditions are set to False.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-18T11:30:43Z

seems like checking if the second step of eviction concludes before the restart is the way to go.
cc @mbobrovskyi

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-07-18T11:58:58Z

/assign
