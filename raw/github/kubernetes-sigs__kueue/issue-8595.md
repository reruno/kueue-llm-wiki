# Issue #8595: [Flaky] Kuberay [It] Should run a rayjob with InTreeAutoscaling

**Summary**: [Flaky] Kuberay [It] Should run a rayjob with InTreeAutoscaling

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8595

**Last updated**: 2026-01-16T11:48:50Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@IrvingMg](https://github.com/IrvingMg)
- **Created**: 2026-01-14T19:16:21Z
- **Updated**: 2026-01-16T11:48:50Z
- **Closed**: 2026-01-16T11:48:50Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 4

## Description

<!--
Please use this template for reporting flaky tests.
Links to specific failures in Prow are appreciated.
-->

**Which test is flaking?**:
Kuberay [It] Should run a rayjob with InTreeAutoscaling [area:singlecluster, feature:kuberay]

**First observed in** (PR or commit, if known):
https://github.com/kubernetes-sigs/kueue/pull/8592

**Link to failed CI job or steps to reproduce locally**:
https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/8592/pull-kueue-test-e2e-main-1-35/2011506332217118720

**Failure message or logs**:
```
[FAILED] Timed out after 45.001s.
  The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/kuberay_test.go:329 with:
  Expected exactly 3 workloads
  Expected
      <[]v1beta2.Workload | len:4, cap:4>: [
          {
              TypeMeta: {
                  Kind: "Workload",
                  APIVersion: "kueue.x-k8s.io/v1beta2",
              },
              ObjectMeta: {
                  Name: "job-rayjob-autoscaling-b6ab2",
                  GenerateName: "",
                  Namespace: "kuberay-e2e-vvh48",
                  SelfLink: "",
                  UID: "a38ab687-2448-4203-bac2-23d48c804274",
                  ResourceVersion: "3837",
                  Generation: 1,
                  CreationTimestamp: {
                      Time: 2026-01-14T18:45:44Z,
                  },
                  DeletionTimestamp: nil,
                  DeletionGracePeriodSeconds: nil,
                  Labels: {
                      "kueue.x-k8s.io/job-uid": "21a93aad-9465-4a0f-a3cb-184634360c1c",
                  },
                  Annotations: {
                      "kueue.x-k8s.io/elastic-job": "true",
                  },
                  OwnerReferences: [
                      {
                          APIVersion: "batch/v1",
                          Kind: "Job",
                          Name: "rayjob-autoscaling",
                          UID: "21a93aad-9465-4a0f-a3cb-184634360c1c",
                          Controller: true,
                          BlockOwnerDeletion: true,
                      },
                  ],
                  Finalizers: [
                      "kueue.x-k8s.io/resource-in-use",
                  ],
                  ManagedFields: [
                      {
                          Manager: "kueue-admission",
                          Operation: "Apply",
                          APIVersion: "kueue.x-k8s.io/v1beta2",
                          Time: {
                              Time: 2026-01-14T18:45:44Z,
                          },
                          FieldsType: "FieldsV1",
                          FieldsV1: {
                              Raw: "{\"f:metadata\":{\"f:annotations\":{\"f:kueue.x-k8s.io/elastic-job\":{}},\"f:labels\":{\"f:kueue.x-k8s.io/job-uid\":{}}},\"f:status\":{\"f:admission\":{\"f:clusterQueue\":{},\"f:podSetAssignments\":{\"k:{\\\"name\\\":\\\"main\\\"}\":{\".\":{},\"f:count\":{},\"f:flavors\":{\"f:cpu\":{}},\"f:name\":{},\"f:resourceUsage\":{\"f:cpu\":{}}}}},\"f:conditions\":{\"k:{\\\"type\\\":\\\"Admitted\\\"}\":{\".\":{},\"f:lastTransitionTime\":{},\"f:message\":{},\"f:observedGeneration\":{},\"f:reason\":{},\"f:status\":{},\"f:type\":{}},\"k:{\\\"type\\\":\\\"QuotaReserved\\\"}\":{\".\":{},\"f:lastTransitionTime\":{},\"f:message\":{},\"f:observedGeneration\":{},\"f:reason\":{},\"f:status\":{},\"f:type\":{}}}}}",
                          },
                          Subresource: "status",
                      },
...
                  Admission: nil,
                  RequeueState: nil,
                  ReclaimablePods: nil,
                  AdmissionChecks: nil,
                  ResourceRequests: nil,
                  AccumulatedPastExecutionTimeSeconds: 5,
                  SchedulingStats: nil,
                  NominatedClusterNames: nil,
                  ClusterName: nil,
                  UnhealthyNodes: nil,
              },
          },
      ]
  to have length 3
  In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/kuberay_test.go:330 @ 01/14/26 18:48:13.698
```

**Anything else we need to know?**:
The failure message/log was truncated here because it exceeded the length limit.

## Discussion

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-01-14T22:24:12Z

I think https://github.com/kubernetes-sigs/kueue/pull/8487 did help. I can see the logs clearly. 

This is expected behavior. The test assumption of exactly 3 workloads doesn't hold when the autoscaler makes multiple intermediate scaling decisions. The https://github.com/kubernetes-sigs/kueue/blob/main/keps/77-dynamically-sized-jobs/README.md#garbage-collection-of-preempted-workload-slices explicitly states:
`Under the current design proposal, all finished workload slices are retained indefinitely and are not garbage collected.`

I think we can either modify the test to count only non-finished workloads, or assert >= 3 instead of == 3, since finished slices are internal implementation details or implement the `PreemptedWorkloadSliceHistory` mechanism mentioned in the KEP to automatically delete old replaced slices beyond a configured limit. 

In the long term, we could immediately delete workloads marked with `WorkloadSliceReplaced`, because they are no longer needed. 
@mimowo Thoughts?

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-15T07:27:42Z

I see, thank you for the analysis. I think for now the test should be adjusted. 

From users perspective I think we need a better solution. Currently, the best we have is the time-based clearing of the finished Workloads using the ObjectRetentionPolicy. However, I think it would be indeed better to only keep preserve the last N finished workloads. We could make N configurable by API, but maybe it is sensible to set some default, say 3, and only make it configurable when proven to be needed. wdyt?

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-01-15T21:52:32Z

I agree with the long-term solution is the right approach here. The test fix is just a band-aid. We should implement proper garbage collection for finished workload slices.

  For the implementation, I think:
  1. Keeping the last N finished workloads is similar to `successfulJobsHistoryLimit`/`failedJobsHistoryLimit` on CronJobs - retaining recent history for debugging/observability before cleanup. Unlike Deployment's `revisionHistoryLimit`, there's no rollback use case here since finished slices are purely historical.
  2. This could be exposed via the `ObjectRetentionPolicy` API or as a dedicated field as mentioned in the KEP's `PreemptedWorkloadSliceHistory` proposal
  3. For workloads marked with `WorkloadSliceReplaced`, we could consider more aggressive cleanup since they're purely internal state with no user-facing value

For immediate unblocking, I'll submit a PR to fix the test by counting only non-finished workloads.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-16T10:25:05Z

Some users may prefer not to enable `ObjectRetentionPolicy`, still the ElasticWorkloads feature should behave "sensibly". While the ElasticWorkloads is in alpha we can change easily the default behavior. I'm thinking it makes sense to GC by default the finished workloads, if we have >2 of then. So we keep the 1 previous replacement (finished potentially long time ago), the current replacement (just finished), and the current active.

This should be enough for debuggability, yet we will prevent accumulating the finished workloads even if `ObjectRetentionPolicy` is disabled. 

Sure, it may not be enough for some rare cases, but then we can introduce API such as `replacementWorkloadHistoryLimit`, but I would defer that until user request to avoid over-complicating the API to unknown benefit.
