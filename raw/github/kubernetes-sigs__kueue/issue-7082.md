# Issue #7082: [flaky workload slicing unit test] sigs.k8s.io/kueue/pkg/workloadslicing: TestFinish/AlreadyFinishedWorkload

**Summary**: [flaky workload slicing unit test] sigs.k8s.io/kueue/pkg/workloadslicing: TestFinish/AlreadyFinishedWorkload

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7082

**Last updated**: 2025-10-01T09:46:20Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-09-30T13:50:28Z
- **Updated**: 2025-10-01T09:46:20Z
- **Closed**: 2025-10-01T09:46:20Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 2

## Description

**What happened**:

failure on unrelated branch: https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/7075/pull-kueue-test-unit-main/1973017516351426560

**What you expected to happen**:
no failure
**How to reproduce it (as minimally and precisely as possible)**:
ci
**Anything else we need to know?**:
```
sigs.k8s.io/kueue/pkg/workloadslicing: TestFinish/AlreadyFinishedWorkload expand_less
Run #0: Failed expand_less	0s
{Failed  === RUN   TestFinish/AlreadyFinishedWorkload
    workloadslicing_test.go:377: Deactivated() (-want,+got):
          &v1beta1.Workload{
          	TypeMeta:   {},
          	ObjectMeta: {Name: "test", Namespace: "default", ResourceVersion: "1", CreationTimestamp: {Time: s"2025-09-30 13:48:12 +0000 UTC"}, ...},
          	Spec:       {PodSets: {{Name: "main", Template: {Spec: {Containers: {{Name: "c", Resources: {Requests: {s"cpu": {i: {...}, s: "100m", Format: "DecimalSI"}}}}}, RestartPolicy: "Never"}}, Count: 1}}},
          	Status: v1beta1.WorkloadStatus{
          		Conditions: []v1.Condition{
          			{
          				Type:               "Finished",
          				Status:             "True",
          				ObservedGeneration: 0,
        - 				LastTransitionTime: v1.Time{Time: s"2025-09-30 13:48:13.013682336 +0000 UTC m=+1.677315711"},
        + 				LastTransitionTime: v1.Time{Time: s"2025-09-30 13:48:12 +0000 UTC"},
          				Reason:             "ByTest",
          				Message:            "Finished by test",
          			},
          		},
          		Admission:    nil,
          		RequeueState: nil,
          		... // 8 identical fields
          	},
          }
--- FAIL: TestFinish/AlreadyFinishedWorkload (0.02s)
}
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-30T13:50:59Z

/kind flake 
looks very similar to https://github.com/kubernetes-sigs/kueue/pull/7076
cc @mszadkow @ichekrygin ptal

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-10-01T07:19:50Z

/assign
