# Issue #7909: [flaky test] Kueue visibility server when There are pending workloads due to capacity maxed by the admitted job Should allow fetching information about pending workloads in ClusterQueue (v1beta1)

**Summary**: [flaky test] Kueue visibility server when There are pending workloads due to capacity maxed by the admitted job Should allow fetching information about pending workloads in ClusterQueue (v1beta1)

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7909

**Last updated**: 2025-11-26T18:30:40Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-11-26T11:55:46Z
- **Updated**: 2025-11-26T18:30:40Z
- **Closed**: 2025-11-26T18:30:40Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@IrvingMg](https://github.com/IrvingMg)
- **Comments**: 2

## Description

/kind flake

**What happened**:

failure on unrelated branch: https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/7895/pull-kueue-test-e2e-main-1-32/1993589081858117632

**What you expected to happen**:
no failure
**How to reproduce it (as minimally and precisely as possible)**:
ci
**Anything else we need to know?**:
```
Kueue visibility server when There are pending workloads due to capacity maxed by the admitted job Should allow fetching information about pending workloads in ClusterQueue (v1beta1)
/home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/visibility_test.go:137
  "level"=0 "msg"="Created namespace" "namespace"="e2e-jqbt4"
  "level"=0 "msg"="Created namespace" "namespace"="e2e-r72dn"
  STEP: Schedule a job that when admitted workload blocks the queue @ 11/26/25 08:07:32.498
  STEP: Ensure the workload is admitted, by awaiting until the job is unsuspended @ 11/26/25 08:07:32.516
  STEP: Verify there are zero pending workloads @ 11/26/25 08:07:39.613
  [FAILED] in [It] - /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/visibility_test.go:140 @ 11/26/25 08:07:39.619
• [FAILED] [9.052 seconds]
Kueue visibility server when There are pending workloads due to capacity maxed by the admitted job [It] Should allow fetching information about pending workloads in ClusterQueue (v1beta1)
/home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/visibility_test.go:137
  [FAILED] Unexpected error:
      <*errors.StatusError | 0xc000834f00>: 
      clusterqueue.visibility.kueue.x-k8s.io "cluster-queue" not found
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
              Message: "clusterqueue.visibility.kueue.x-k8s.io \"cluster-queue\" not found",
              Reason: "NotFound",
              Details: {
                  Name: "cluster-queue",
                  Group: "visibility.kueue.x-k8s.io",
                  Kind: "clusterqueue",
                  UID: "",
                  Causes: nil,
                  RetryAfterSeconds: 0,
              },
              Code: 404,
          },
      }
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-26T11:57:06Z

cc @mbobrovskyi @IrvingMg 
I think the issue is that we never check that the CQ has already been created (events got propagated). So, I think it would be better to check if the CQ is already Active, as we do also in other tests.

Alternatively, use eventually around the call.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-11-26T13:04:31Z

/assign @IrvingMg
