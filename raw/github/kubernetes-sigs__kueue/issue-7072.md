# Issue #7072: [Flaky unit test] TestEnsureWorkloadSlices/OneWorkloadSlice_ReservedQuota_ScaleDown_MultiplePodSets

**Summary**: [Flaky unit test] TestEnsureWorkloadSlices/OneWorkloadSlice_ReservedQuota_ScaleDown_MultiplePodSets

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7072

**Last updated**: 2025-09-30T10:30:20Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-09-30T08:25:26Z
- **Updated**: 2025-09-30T10:30:20Z
- **Closed**: 2025-09-30T10:30:20Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 2

## Description

**What happened**:

failure on periodic build from main: https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-unit-main/1972731321574756352

**What you expected to happen**:

no failure

**How to reproduce it (as minimally and precisely as possible)**:
ci
**Anything else we need to know?**:

```
sigs.k8s.io/kueue/pkg/workloadslicing: TestEnsureWorkloadSlices/OneWorkloadSlice_ReservedQuota_ScaleDown_MultiplePodSets expand_less
Run #0: Failed expand_less	0s
{Failed  === RUN   TestEnsureWorkloadSlices/OneWorkloadSlice_ReservedQuota_ScaleDown_MultiplePodSets
    workloadslicing_test.go:993: EnsureWorkloadSlices() (-want,+got):
          &v1beta1.Workload{
          	TypeMeta:   {},
          	ObjectMeta: {Name: "test-1", ResourceVersion: "2", OwnerReferences: {{APIVersion: "batch/v1", Kind: "Job", Name: "test", UID: "67455e46-645d-48c3-b3e8-3bdac9edece2", ...}}},
          	Spec:       {PodSets: {{Name: "scale-down", Template: {Spec: {Containers: {{Name: "c", Resources: {Requests: {s"cpu": {i: {...}, s: "1", Format: "DecimalSI"}}}}}, RestartPolicy: "Never"}}, Count: 1}, {Name: "stay-the-same", Template: {Spec: {Containers: {{Name: "c", Resources: {Requests: {s"cpu": {i: {...}, s: "1", Format: "DecimalSI"}}}}}, RestartPolicy: "Never"}}, Count: 3}}},
          	Status: v1beta1.WorkloadStatus{
          		Conditions: []v1.Condition{
          			{
          				Type:               "QuotaReserved",
          				Status:             "True",
          				ObservedGeneration: 0,
        - 				LastTransitionTime: v1.Time{Time: s"2025-09-29 18:51:41.000067302 +0000 UTC m=+0.244136162"},
        + 				LastTransitionTime: v1.Time{Time: s"2025-09-29 18:51:40 +0000 UTC"},
          				Reason:             "AdmittedByTest",
          				Message:            "Admitted by ClusterQueue default",
          			},
          		},
          		Admission:    &{ClusterQueue: "default", PodSetAssignments: {{Name: "scale-down", Flavors: {s"cpu": "default"}, ResourceUsage: {s"cpu": {i: {...}, s: "1", Format: "DecimalSI"}}, Count: &3, ...}, {Name: "stay-the-same", Flavors: {s"cpu": "default"}, ResourceUsage: {s"cpu": {i: {...}, s: "1", Format: "DecimalSI"}}, Count: &3, ...}}},
          		RequeueState: nil,
          		... // 8 identical fields
          	},
          }
--- FAIL: TestEnsureWorkloadSlices/OneWorkloadSlice_ReservedQuota_ScaleDown_MultiplePodSets (0.01s)
}
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-30T08:25:51Z

/kind flake
seems like clock issue, cc @ichekrygin @mbobrovskyi ptal

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-09-30T08:38:50Z

/assign
