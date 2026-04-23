# Issue #8447: [flaky test] Kuberay Should run a rayjob with InTreeAutoscaling

**Summary**: [flaky test] Kuberay Should run a rayjob with InTreeAutoscaling

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8447

**Last updated**: 2026-01-12T17:19:33Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-01-07T10:01:42Z
- **Updated**: 2026-01-12T17:19:33Z
- **Closed**: 2026-01-12T15:44:12Z
- **Labels**: `kind/bug`, `priority/important-soon`, `kind/flake`
- **Assignees**: [@sohankunkerkar](https://github.com/sohankunkerkar)
- **Comments**: 6

## Description

**Which test is flaking?**:
Kuberay Should run a rayjob with InTreeAutoscaling


**First observed in** (PR or commit, if known):

**Link to failed CI job or steps to reproduce locally**:

https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-main-1-34/2008631135017373696

**Failure message or logs**:
```
{Timed out after 45.001s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/singlecluster/kuberay_test.go:328 with:
Expected exactly 3 workloads
Expected
    <[]v1beta2.Workload | len:4, cap:4>: [
        {
            TypeMeta: {
                Kind: "Workload",
                APIVersion: "kueue.x-k8s.io/v1beta2",
            },
            ObjectMeta: {
                Name: "job-rayjob-autoscaling-bede5",
                GenerateName: "",
                Namespace: "kuberay-e2e-25656",
                SelfLink: "",
                UID: "7a4f8d77-79da-4025-90e2-0782d4c6aba0",
                ResourceVersion: "10794",
                Generation: 1,
                CreationTimestamp: {
                    Time: 2026-01-06T20:27:00Z,
                },
                DeletionTimestamp: nil,
                DeletionGracePeriodSeconds: nil,
                Labels: {
                    "kueue.x-k8s.io/job-uid": "46283874-5cd2-41af-9ea6-6b4a210a52fc",
                },
                Annotations: {
                    "kueue.x-k8s.io/elastic-job": "true",
                },
                OwnerReferences: [
                    {
                        APIVersion: "batch/v1",
                        Kind: "Job",
                        Name: "rayjob-autoscaling",
                        UID: "46283874-5cd2-41af-9ea6-6b4a210a52fc",
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
                            Time: 2026-01-06T20:27:00Z,
                        },
                        FieldsType: "FieldsV1",
                        FieldsV1: {
                            Raw: "{\"f:metadata\":{\"f:annotations\":{\"f:kueue.x-k8s.io/elastic-job\":{}},\"f:labels\":{\"f:kueue.x-k8s.io/job-uid\":{}}},\"f:status\":{\"f:admission\":{\"f:clusterQueue\":{},\"f:podSetAssignments\":{\"k:{\\\"name\\\":\\\"main\\\"}\":{\".\":{},\"f:count\":{},\"f:flavors\":{\"f:cpu\":{}},\"f:name\":{},\"f:resourceUsage\":{\"f:cpu\":{}}}}},\"f:conditions\":{\"k:{\\\"type\\\":\\\"Admitted\\\"}\":{\".\":{},\"f:lastTransitionTime\":{},\"f:message\":{},\"f:observedGeneration\":{},\"f:reason\":{},\"f:status\":{},\"f:type\":{}},\"k:{\\\"type\\\":\\\"QuotaReserved\\\"}\":{\".\":{},\"f:lastTransitionTime\":{},\"f:message\":{},\"f:observedGeneration\":{},\"f:reason\":{},\"f:status\":{},\"f:type\":{}}}}}",
                        },
                        Subresource: "status",
                    },
                    {
                        Manager: "kueue",
                        Operation: "Update",
                        APIVersion: "kueue.x-k8s.io/v1beta2",
                        Time: {
                            Time: 2026-01-06T20:27:00Z,
                        },
                        FieldsType: "FieldsV1",
                        FieldsV1: {
                            Raw: "{\"f:metadata\":{\"f:annotations\":{\".\":{},\"f:kueue.x-k8s.io/elastic-job\":{}},\"f:finalizers\":{\".\":{},\"v:\\\"kueue.x-k8s.io/resource-in-use\\\"\":{}},\"f:labels\":{\".\":{},\"f:kueue.x-k8s.io/job-uid\":{}},\"f:ownerReferences\":{\".\":{},\"k:{\\\"uid\\\":\\\"46283874-5cd2-41af-9ea6-6b4a210a52fc\\\"}\":{}}},\"f:spec\":{\".\":{},\"f:active\":{},\"f:podSets\":{\".\":{},\"k:{\\\"name\\\":\\\"main\\\"}\":{\".\":{},\"f:count\":{},\"f:name\":{},\"f:template\":{\".\":{},\"f:metadata\":{\".\":{},\"f:labels\":{\".\":{},\"f:batch.kubernetes.io/job-name\":{}}},\"f:spec\":{\".\":{},\"f:containers\":{\".\":{},\"k:{\\\"name\\\":\\\"rayjob-submitter\\\"}\":{\".\":{},\"f:args\":{},\"f:command\":{},\"f:env\":{\".\":{},\"k:{\\\"name\\\":\\\"PYTHONUNBUFFERED\\\"}\":{\".\":{},\"f:name\":{},\"f:value\":{}},\"k:{\\\"name\\\":\\\"RAY_DASHBOARD_ADDRESS\\\"}\":{\".\":{},\"f:name\":{},\"f:value\":{}},\"k:{\\\"name\\\":\\\"RAY_JOB_SUBMISSION_ID\\\"}\":{\".\":...

Gomega truncated this representation as it exceeds 'format.MaxLength'.
Consider having the object provide a custom 'GomegaStringer' representation
or adjust the parameters in Gomega's 'format' package.

Learn more here: https://onsi.github.io/gomega/#adjusting-output

to have length 3 failed [FAILED] Timed out after 45.001s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/singlecluster/kuberay_test.go:328 with:
Expected exactly 3 workloads
Expected
    <[]v1beta2.Workload | len:4, cap:4>: [
        {
            TypeMeta: {
                Kind: "Workload",
                APIVersion: "kueue.x-k8s.io/v1beta2",
            },
            ObjectMeta: {
                Name: "job-rayjob-autoscaling-bede5",
                GenerateName: "",
                Namespace: "kuberay-e2e-25656",
                SelfLink: "",
                UID: "7a4f8d77-79da-4025-90e2-0782d4c6aba0",
                ResourceVersion: "10794",
                Generation: 1,
                CreationTimestamp: {
                    Time: 2026-01-06T20:27:00Z,
                },
                DeletionTimestamp: nil,
                DeletionGracePeriodSeconds: nil,
                Labels: {
                    "kueue.x-k8s.io/job-uid": "46283874-5cd2-41af-9ea6-6b4a210a52fc",
                },
                Annotations: {
                    "kueue.x-k8s.io/elastic-job": "true",
                },
                OwnerReferences: [
                    {
                        APIVersion: "batch/v1",
                        Kind: "Job",
                        Name: "rayjob-autoscaling",
                        UID: "46283874-5cd2-41af-9ea6-6b4a210a52fc",
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
                            Time: 2026-01-06T20:27:00Z,
                        },
                        FieldsType: "FieldsV1",
                        FieldsV1: {
                            Raw: "{\"f:metadata\":{\"f:annotations\":{\"f:kueue.x-k8s.io/elastic-job\":{}},\"f:labels\":{\"f:kueue.x-k8s.io/job-uid\":{}}},\"f:status\":{\"f:admission\":{\"f:clusterQueue\":{},\"f:podSetAssignments\":{\"k:{\\\"name\\\":\\\"main\\\"}\":{\".\":{},\"f:count\":{},\"f:flavors\":{\"f:cpu\":{}},\"f:name\":{},\"f:resourceUsage\":{\"f:cpu\":{}}}}},\"f:conditions\":{\"k:{\\\"type\\\":\\\"Admitted\\\"}\":{\".\":{},\"f:lastTransitionTime\":{},\"f:message\":{},\"f:observedGeneration\":{},\"f:reason\":{},\"f:status\":{},\"f:type\":{}},\"k:{\\\"type\\\":\\\"QuotaReserved\\\"}\":{\".\":{},\"f:lastTransitionTime\":{},\"f:message\":{},\"f:observedGeneration\":{},\"f:reason\":{},\"f:status\":{},\"f:type\":{}}}}}",
                        },
                        Subresource: "status",
                    },
                    {
                        Manager: "kueue",
                        Operation: "Update",
                        APIVersion: "kueue.x-k8s.io/v1beta2",
                        Time: {
                            Time: 2026-01-06T20:27:00Z,
                        },
                        FieldsType: "FieldsV1",
                        FieldsV1: {
                            Raw: "{\"f:metadata\":{\"f:annotations\":{\".\":{},\"f:kueue.x-k8s.io/elastic-job\":{}},\"f:finalizers\":{\".\":{},\"v:\\\"kueue.x-k8s.io/resource-in-use\\\"\":{}},\"f:labels\":{\".\":{},\"f:kueue.x-k8s.io/job-uid\":{}},\"f:ownerReferences\":{\".\":{},\"k:{\\\"uid\\\":\\\"46283874-5cd2-41af-9ea6-6b4a210a52fc\\\"}\":{}}},\"f:spec\":{\".\":{},\"f:active\":{},\"f:podSets\":{\".\":{},\"k:{\\\"name\\\":\\\"main\\\"}\":{\".\":{},\"f:count\":{},\"f:name\":{},\"f:template\":{\".\":{},\"f:metadata\":{\".\":{},\"f:labels\":{\".\":{},\"f:batch.kubernetes.io/job-name\":{}}},\"f:spec\":{\".\":{},\"f:containers\":{\".\":{},\"k:{\\\"name\\\":\\\"rayjob-submitter\\\"}\":{\".\":{},\"f:args\":{},\"f:command\":{},\"f:env\":{\".\":{},\"k:{\\\"name\\\":\\\"PYTHONUNBUFFERED\\\"}\":{\".\":{},\"f:name\":{},\"f:value\":{}},\"k:{\\\"name\\\":\\\"RAY_DASHBOARD_ADDRESS\\\"}\":{\".\":{},\"f:name\":{},\"f:value\":{}},\"k:{\\\"name\\\":\\\"RAY_JOB_SUBMISSION_ID\\\"}\":{\".\":...

Gomega truncated this representation as it exceeds 'format.MaxLength'.
Consider having the object provide a custom 'GomegaStringer' representation
or adjust the parameters in Gomega's 'format' package.

Learn more here: https://onsi.github.io/gomega/#adjusting-output

to have length 3
In [It] at: /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/singlecluster/kuberay_test.go:329 @ 01/06/26 20:29:11.224
}
```

**Anything else we need to know?**:

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-07T10:33:42Z

/priority important-soon

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-01-07T20:51:55Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-08T16:39:33Z

@sohankunkerkar could you please provide some analysis / summary for why this is the issue.

I'm a bit surprised because we have this code in the scheduler which should make the replaced Workload as finished before sending the request to admit the new workload: https://github.com/kubernetes-sigs/kueue/blob/e355ea8d26bb8e597e7304b626df96e147760a64/pkg/scheduler/scheduler.go#L353-L364

So IIUC we should never admit before finishing the previous one.

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-01-08T20:57:24Z

You're right that the scheduler calls `replaceWorkloadSlice` before admit. However, there's a race between the scheduler and the job controller.

  The scenario:
  1. Scheduler issues `PATCH` to finish old workload via `replaceWorkloadSlice`
  2. Scheduler issues `PATCH/Apply` to admit new workload
  3. Job controller reconciles and calls `EnsureWorkloadSlices`

Even though the scheduler issues these patches sequentially, the job controller may observe an intermediate state where the new workload's admission has been committed but the old workload's Finished condition hasn't been observed yet (due to informer cache lag or API timing).

Additionally, if the scheduler can't find the old slice target, `oldWorkloadSlice` will be nil, so the scheduler skips `replaceWorkloadSlice` entirely and proceeds to admit. This can also lead to both slices being admitted. The controller must enforce the invariant when it observes both slices admitted and linked by `WorkloadSliceReplacementFor`.

When `EnsureWorkloadSlices` sees both workloads with quota reservation, it currently hits the error path. The [fix](https://github.com/kubernetes-sigs/kueue/pull/8456) adds a recovery mechanism: if the new workload has the `WorkloadSliceReplacementFor` annotation pointing to the old workload, we know this is the expected cleanup path rather than an anomaly, so we finish the old workload and proceed normally. This code path is narrowly gated by the replacement annotation check, so it doesn't alter behavior for other scenarios.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-09T09:04:23Z

Thank you for explaining, I know fully understand the circumstances for the race to occur (basically event propagation allows that we first observe the newWorkload Admitted before the old one Finished). So, this is worth fixing.

However, to get the full picture I still have some questions about the downstream effect of the bug (maybe you know answers):
1. Why would we get 4 workloads in the process?
2. Would this result in a user-facing issue, or just one extra workload which is finished?|

FYI: I have also opened https://github.com/kubernetes-sigs/kueue/pull/8487 which could reveal the state of the workloads for future occurrences.

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-01-12T17:19:33Z

>FYI: I have also opened https://github.com/kubernetes-sigs/kueue/pull/8487 which could reveal the state of the workloads for future occurrences.

Thanks for fixing that. Yeah, the logs were truncated for [this](https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-main-1-34/2008631135017373696) job. This will definitely help.

>Why would we get 4 workloads in the process?

Based on code analysis (the CI logs were truncated), I suspect the issue is a race condition between the scheduler and job controller. When a scale-up happens, the scheduler admits the new workload and tries to finish the old one. If finishing the old one fails for any reason, the scheduler moves on but the new workload is already admitted. The controller then sees both workloads with quota reserved, a state the old code didn't handle. I think what could have happened here is instead of cleaning up, it returned an error and retried. During these retries, Ray's autoscaler kept generating scale events. When things eventually resolved, each queued event could trigger creation of another workload. This accumulation might explain the extra workload.


>Would this result in a user-facing issue, or just one extra workload which is finished?

I believe so, though not severely. Users would likely see delays during autoscaling and possibly confusing error messages in logs. That said, from what I can tell, the system should eventually recover on its own, so no resources would be permanently leaked and extra workloads should get cleaned up. The fix just makes this recovery immediate rather than waiting for things to sync up naturally.
