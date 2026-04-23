# Issue #4651: Flaky test:  JobSet when Creating a JobSet Should run a jobSet if admitted

**Summary**: Flaky test:  JobSet when Creating a JobSet Should run a jobSet if admitted

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4651

**Last updated**: 2025-03-19T08:11:06Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-03-17T12:32:21Z
- **Updated**: 2025-03-19T08:11:06Z
- **Closed**: 2025-03-19T08:11:04Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 4

## Description

**What happened**:

The test failed on unrelated branch: https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/4648/pull-kueue-test-e2e-main-1-32/1901605023159160832

**What you expected to happen**:

no failures

**How to reproduce it (as minimally and precisely as possible)**:

ci 

**Anything else we need to know?**:

```
End To End Suite: kindest/node:v1.32.0: [It] JobSet when Creating a JobSet Should run a jobSet if admitted expand_less	47s
{Timed out after 45.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/jobset_test.go:107 with:
Expected object to be comparable, diff:   (*v1.Condition)(
- 	nil,
+ 	s"&Condition{Type:Finished,Status:True,ObservedGeneration:0,LastTransitionTime:0001-01-01 00:00:00 +0000 UTC,Reason:Succeeded,Message:jobset completed successfully,}",
  )
 failed [FAILED] Timed out after 45.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/jobset_test.go:107 with:
Expected object to be comparable, diff:   (*v1.Condition)(
- 	nil,
+ 	s"&Condition{Type:Finished,Status:True,ObservedGeneration:0,LastTransitionTime:0001-01-01 00:00:00 +0000 UTC,Reason:Succeeded,Message:jobset completed successfully,}",
  )
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/jobset_test.go:113 @ 03/17/25 12:12:27.713
}

```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-17T12:32:36Z

/kind flake
cc @mbobrovskyi @tenzen-y

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-17T12:33:23Z

I discuss this test a bit here: https://github.com/kubernetes-sigs/kueue/issues/4626#issuecomment-2729317844.

I think we need to either increase the timeout somehow or relax the assert.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-19T08:11:00Z

/close
Doing reset of e2e-related flakes as agreed in https://github.com/kubernetes-sigs/kueue/issues/4674#issuecomment-2734095182.

The reason is that we recently bumped up the job resources, and it is expected to help for most of the flakes were attributed to long termination of a job. So, this way we can avoid people looking into an already solved problem.

For more details check the PR [kubernetes/test-infra#34529](https://github.com/kubernetes/test-infra/pull/34529) as discussed here: [#4669](https://github.com/kubernetes-sigs/kueue/issues/4669).

If the failure re-occurs feel free to re-open or open a new one.

Also, feel free to re-open if you have some evidence / hints that constrained resources is not the reason for the failure.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-03-19T08:11:05Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4651#issuecomment-2735670345):

>/close
>Doing reset of e2e-related flakes as agreed in https://github.com/kubernetes-sigs/kueue/issues/4674#issuecomment-2734095182.
>
>The reason is that we recently bumped up the job resources, and it is expected to help for most of the flakes were attributed to long termination of a job. So, this way we can avoid people looking into an already solved problem.
>
>For more details check the PR [kubernetes/test-infra#34529](https://github.com/kubernetes/test-infra/pull/34529) as discussed here: [#4669](https://github.com/kubernetes-sigs/kueue/issues/4669).
>
>If the failure re-occurs feel free to re-open or open a new one.
>
>Also, feel free to re-open if you have some evidence / hints that constrained resources is not the reason for the failure.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
