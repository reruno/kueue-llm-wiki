# Issue #9954: Flaky test: MultiKueue with scheduler when MultiKueueOrchestratedPreemption is enabled [It] should not trigger concurrent preemptions [area:multikueue, feature:multikueue]

**Summary**: Flaky test: MultiKueue with scheduler when MultiKueueOrchestratedPreemption is enabled [It] should not trigger concurrent preemptions [area:multikueue, feature:multikueue]

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9954

**Last updated**: 2026-04-17T09:15:59Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2026-03-17T17:31:52Z
- **Updated**: 2026-04-17T09:15:59Z
- **Closed**: 2026-04-17T09:15:58Z
- **Labels**: `kind/bug`, `kind/flake`, `area/multikueue`
- **Assignees**: [@kshalot](https://github.com/kshalot)
- **Comments**: 12

## Description

<!--
Please use this template for reporting flaky tests.
Links to specific failures in Prow are appreciated.
-->

**Which test is flaking?**:

MultiKueue with scheduler when MultiKueueOrchestratedPreemption is enabled [It] should not trigger concurrent preemptions [area:multikueue, feature:multikueue]

**Link to failed CI job or steps to reproduce locally**:

https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/9953/pull-kueue-test-integration-multikueue-main/2033955179371433984

**Failure message or logs**:
```
  [FAILED] Failed after 0.574s.
  The function passed to Consistently failed at /home/prow/go/src/sigs.k8s.io/kueue/test/integration/multikueue/scheduler/scheduler_test.go:637 with:
  Expected success, but got an error:
      <*errors.StatusError | 0xc002e96b40>: 
      workloads.kueue.x-k8s.io "job-low-job2-bdddb" not found
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
              Message: "workloads.kueue.x-k8s.io \"job-low-job2-bdddb\" not found",
              Reason: "NotFound",
              Details: {
                  Name: "job-low-job2-bdddb",
                  Group: "kueue.x-k8s.io",
                  Kind: "workloads",
                  UID: "",
                  Causes: nil,
                  RetryAfterSeconds: 0,
              },
              Code: 404,
          },
      }
  In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/integration/multikueue/scheduler/scheduler_test.go:655 @ 03/17/26 17:25:35.413
```

**Anything else we need to know?**:

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-17T17:35:56Z

cc @kshalot ptal

### Comment by [@kshalot](https://github.com/kshalot) — 2026-03-17T18:16:56Z

/assign

I saw this once, made some changes and then re-ran the test locally in a loop and it did not flake. So I guess I got lucky then.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-27T13:06:38Z

https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/10081/pull-kueue-test-integration-multikueue-main/2037512650392342528

### Comment by [@kshalot](https://github.com/kshalot) — 2026-04-07T15:03:16Z

This was addressed in https://github.com/kubernetes-sigs/kueue/pull/9670. I'll monitor the flakiness.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-04-08T11:09:59Z

https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-integration-multikueue-main/2041810094642958336
This still fails on the same assert, pretty often actually

### Comment by [@mimowo](https://github.com/mimowo) — 2026-04-08T11:10:52Z

/retitle MultiKueue with scheduler when MultiKueueOrchestratedPreemption is enabled [It] should not trigger concurrent preemptions [area:multikueue, feature:multikueue]

Including the full title for easier search in the existing issues

### Comment by [@mimowo](https://github.com/mimowo) — 2026-04-08T11:11:42Z

Another occurrence: https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-integration-multikueue-main/2041628898977910784
/retitle Flaky test: MultiKueue with scheduler when MultiKueueOrchestratedPreemption is enabled [It] should not trigger concurrent preemptions [area:multikueue, feature:multikueue]

### Comment by [@kshalot](https://github.com/kshalot) — 2026-04-08T12:40:49Z

> Another occurrence: https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-integration-multikueue-main/2041628898977910784 /retitle Flaky test: MultiKueue with scheduler when MultiKueueOrchestratedPreemption is enabled [It] should not trigger concurrent preemptions [area:multikueue, feature:multikueue]

@mimowo this looks more like https://github.com/kubernetes-sigs/kueue/issues/10304

### Comment by [@kshalot](https://github.com/kshalot) — 2026-04-08T12:45:10Z

But it is indeed failing (https://testgrid.k8s.io/sig-scheduling#periodic-kueue-test-integration-multikueue-main). And I think I see why, only the e2e test was aligned in https://github.com/kubernetes-sigs/kueue/pull/9670 and not the integration test.

I'll make the change.

### Comment by [@olekzabl](https://github.com/olekzabl) — 2026-04-16T08:07:26Z

/area multikueue

### Comment by [@kshalot](https://github.com/kshalot) — 2026-04-17T09:15:52Z

/close

Looks like it's solved by https://github.com/kubernetes-sigs/kueue/pull/10367.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-04-17T09:15:59Z

@kshalot: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/9954#issuecomment-4266762142):

>/close
>
>Looks like it's solved by https://github.com/kubernetes-sigs/kueue/pull/10367.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
