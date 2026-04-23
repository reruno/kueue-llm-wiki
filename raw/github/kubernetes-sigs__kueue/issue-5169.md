# Issue #5169: [release-0.11] Flaky Integration Test: MultiKueue [It] Should run a job on worker if admitted

**Summary**: [release-0.11] Flaky Integration Test: MultiKueue [It] Should run a job on worker if admitted

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5169

**Last updated**: 2025-05-08T09:11:48Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-05-06T07:58:11Z
- **Updated**: 2025-05-08T09:11:48Z
- **Closed**: 2025-05-08T09:11:46Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 13

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

The `MultiKueue [It] Should run a job on worker if admitted` case failed on periodic CI job, unexpectedly:

```shell

  [FAILED] Timed out after 10.001s.
  The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/integration/multikueue/jobs_test.go:223 with:
  Expected success, but got an error:
      <*errors.StatusError | 0xc003562780>: 
      workloads.kueue.x-k8s.io "job-job-0ffed" not found
      {
          ErrStatus: {
              TypeMeta: {Kind: "", APIVersion: ""},
              ListMeta: {
                  SelfLink: "",
                  ResourceVersion: "",
                  Continue: "",
                  RemainingItemCount: nil,
              },
              Status: "Failure",
              Message: "workloads.kueue.x-k8s.io \"job-job-0ffed\" not found",
              Reason: "NotFound",
              Details: {
                  Name: "job-job-0ffed",
                  Group: "kueue.x-k8s.io",
                  Kind: "workloads",
                  UID: "",
                  Causes: nil,
                  RetryAfterSeconds: 0,
              },
              Code: 404,
          },
      }
  In [It] at: /home/prow/go/src/kubernetes-sigs/kueue/test/integration/multikueue/jobs_test.go:227 @ 05/05/25 08:30:23.295
```

https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-integration-multikueue-release-0-11/1919307278368903168

**What you expected to happen**:

no errors

**How to reproduce it (as minimally and precisely as possible)**:

<img width="715" alt="Image" src="https://github.com/user-attachments/assets/a65d74b8-ba58-4925-909d-b1570dd076a8" />

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-06T07:58:18Z

/kind flake

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-05-06T08:03:10Z

I think this is integration test.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-05-06T08:03:53Z

cc @mszadkow

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-06T08:09:20Z

> I think this is integration test.

Oh, you are right. I'm updating the issue title.

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-05-06T08:21:01Z

/assign

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-05-07T09:10:56Z

For one of the worker clusters (I assume worker1, as this workload was missing) the ClusterQueue creation event got lost for a while and the CQ itself was created in `checking the workload creation in the worker clusters` step.
This should be already done in BeforeEach.
In result the workload couldn't be created in that cluster: 
`Workload is inadmissible because of missing ClusterQueue` 
and 
`ClusterQueue for workload didn't exist; ignored for now`.
As we do not repeat the workload event when queue is finally created, here is the problem.

@mbobrovskyi @tenzen-y wdyt?
I think it's expected if CQ is missing at the time.
Maybe we could enhance the test by checking if CQs exist before proceed

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-07T14:29:40Z

> @mbobrovskyi @tenzen-y wdyt?
I think it's expected if CQ is missing at the time.
Maybe we could enhance the test by checking if CQs exist before proceed

That sounds reasonable. Thanks

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-07T14:43:21Z

> the ClusterQueue creation event got lost for a while and the CQ itself was created in checking the workload creation in the worker clusters step.

"the CQ itself was created in checking the " - I don't understand that. The step is only using "get", how it can create anything?

```golang 
		ginkgo.By("checking the workload creation in the worker clusters", func() {
			managerWl := &kueue.Workload{}
			gomega.Expect(managerTestCluster.client.Get(managerTestCluster.ctx, wlLookupKey, managerWl)).To(gomega.Succeed())
			gomega.Eventually(func(g gomega.Gomega) {
				g.Expect(worker1TestCluster.client.Get(worker1TestCluster.ctx, wlLookupKey, createdWorkload)).To(gomega.Succeed())
				g.Expect(createdWorkload.Spec).To(gomega.BeComparableTo(managerWl.Spec))
				g.Expect(worker2TestCluster.client.Get(worker2TestCluster.ctx, wlLookupKey, createdWorkload)).To(gomega.Succeed())
				g.Expect(createdWorkload.Spec).To(gomega.BeComparableTo(managerWl.Spec))
			}, util.Timeout, util.Interval).Should(gomega.Succeed())
		})
```
Or you mean the event about the CQ was delivered only then? In that case, maybe waiting in the BeforeEach for ExpectClusterQueuesToBeActive would help? To await for the cache to notice the event?

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-05-08T06:51:54Z

> > the ClusterQueue creation event got lost for a while and the CQ itself was created in checking the workload creation in the worker clusters step.
> 
> "the CQ itself was created in checking the " - I don't understand that. The step is only using "get", how it can create anything?
> 
> 		ginkgo.By("checking the workload creation in the worker clusters", func() {
> 			managerWl := &kueue.Workload{}
> 			gomega.Expect(managerTestCluster.client.Get(managerTestCluster.ctx, wlLookupKey, managerWl)).To(gomega.Succeed())
> 			gomega.Eventually(func(g gomega.Gomega) {
> 				g.Expect(worker1TestCluster.client.Get(worker1TestCluster.ctx, wlLookupKey, createdWorkload)).To(gomega.Succeed())
> 				g.Expect(createdWorkload.Spec).To(gomega.BeComparableTo(managerWl.Spec))
> 				g.Expect(worker2TestCluster.client.Get(worker2TestCluster.ctx, wlLookupKey, createdWorkload)).To(gomega.Succeed())
> 				g.Expect(createdWorkload.Spec).To(gomega.BeComparableTo(managerWl.Spec))
> 			}, util.Timeout, util.Interval).Should(gomega.Succeed())
> 		})
> Or you mean the event about the CQ was delivered only then? In that case, maybe waiting in the BeforeEach for ExpectClusterQueuesToBeActive would help? To await for the cache to notice the event?

Yes, exactly the latter.
The CQ creation event should be handled (thus CQ for worker1 created) before attempt to create workload on that worker.
`ExpectClusterQueuesToBeActive` will do the trick imho

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-08T08:05:08Z

/reopen
for the pending remarks https://github.com/kubernetes-sigs/kueue/pull/5195

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-05-08T08:05:13Z

@mimowo: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/5169#issuecomment-2862147404):

>/reopen
>for the pending remarks https://github.com/kubernetes-sigs/kueue/pull/5195


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-08T09:11:42Z

/close 
as we have https://github.com/kubernetes-sigs/kueue/pull/5196 follow up

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-05-08T09:11:46Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/5169#issuecomment-2862330351):

>/close 
>as we have https://github.com/kubernetes-sigs/kueue/pull/5196 follow up


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
