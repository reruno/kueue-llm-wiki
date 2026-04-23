# Issue #6698: ElasticJob integration test depends on ordering of Workload items

**Summary**: ElasticJob integration test depends on ordering of Workload items

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6698

**Last updated**: 2025-08-29T22:36:52Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@VassilisVassiliadis](https://github.com/VassilisVassiliadis)
- **Created**: 2025-08-29T14:40:10Z
- **Updated**: 2025-08-29T22:36:52Z
- **Closed**: 2025-08-29T22:36:52Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 3

## Description

**What happened**:

The integration test for Elastic Jobs has an implicit assumption on the ordering of Workload items. 

The test in question is https://github.com/kubernetes-sigs/kueue/blob/3658e05baed9fe424763c1c24ff2147b56019f0d/test/integration/singlecluster/controller/jobs/job/job_controller_test.go#L3213-L3227

It uses `testJobWorkload.name` as a means of identifying the workload item that's supposed to have finished. The problem is that the for loop also updates the reference `testJobWorkload`. This implicitly makes the code assume that the `workload.Items` are in the order [workload-before-scale, workload-after-scale].


Explanation:

If the 1st object in workload.Items is the "post-scale" workload then the condition in the if statement of line 3219 will evaluate to False. The code below the if statement will then point the `testJobWorkload` to the "post-scale" object. 

And this is what is causing the problem.

Changing `testJobWorkload` to point to workload.Items[0] now makes the next iteration to also not execute the body of the if statement in 3219. As a result the test will never run the the assertion on line 3220.

<details><summary>A trace of the code with the 2 different orderings of the objects</summary>


Now here's what I think happens when the order of the items is [postScale, preScale]:


- 3219: condition is False because testJobWorkload.name != postScale.name
- 3223: testJobWorkload is now postScale
- 3224: the assertion is fine because postScale is admitted
- 3219: condition is False because testJobWorkload.name != preScale.name
- 3223: testJobWorkload is now preScale
- 3224: the assertion is fine because preScale is admitted

With the order [postScale, preScale] we didn't get to check whether preScale is finished.

</details>

**What you expected to happen**:

The test should finish successfully regardless of the ordering of the Workload items.

**How to reproduce it (as minimally and precisely as possible)**:

Change the `old workload is finished and new workload is admitted` step into this:

```go
ginkgo.By("old workload is finished and new workload is admitted")
		gomega.Eventually(func(g gomega.Gomega) {
			workloads := &kueue.WorkloadList{}
			g.Expect(k8sClient.List(ctx, workloads, client.InNamespace(testJob.Namespace))).Should(gomega.Succeed())
			g.Expect(workloads.Items).Should(gomega.HaveLen(2))
			verifiedFinished := false    // <-- new line
			for i := range workloads.Items {
				if workloads.Items[i].Name == testJobWorkload.Name {
					g.Expect(workload.IsFinished(&workloads.Items[i])).Should(gomega.BeTrue())
					verifiedFinished = true    // <-- new line
					continue
				}
				testJobWorkload = &workloads.Items[i]
				util.ExpectWorkloadsToBeAdmitted(ctx, k8sClient, testJobWorkload)
			}
			g.Expect(verifiedFinished).Should(gomega.BeTrue())    // <-- new line
		}, util.Timeout, util.Interval).Should(gomega.Succeed())
```

Then to test, run from within the root directory of the Kueue code:

```
INTEGRATION_TARGET='test/integration/singlecluster/controller/jobs/job' GINKGO_ARGS="--focus='Job with elastic jobs via workload-slices support'" make test-integration
```

This test will randomly fail during the `old workload is finished and new workload is admitted` step on the assertion for `verifiedFinished == true`.

## Discussion

### Comment by [@VassilisVassiliadis](https://github.com/VassilisVassiliadis) — 2025-08-29T14:40:33Z

The PR for this is in https://github.com/kubernetes-sigs/kueue/pull/6692

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-29T22:36:47Z

@VassilisVassiliadis Thank you for reporting this issue!

Closing by #6692 
/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-08-29T22:36:52Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/6698#issuecomment-3238473736):

>@VassilisVassiliadis Thank you for reporting this issue!
>
>Closing by #6692 
>/close
>
>
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
