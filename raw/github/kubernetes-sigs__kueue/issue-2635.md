# Issue #2635: Flaky Unit Test: deleted_unschedulable_pods_are_finalized

**Summary**: Flaky Unit Test: deleted_unschedulable_pods_are_finalized

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2635

**Last updated**: 2024-07-19T10:58:06Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@gabesaba](https://github.com/gabesaba)
- **Created**: 2024-07-18T12:02:24Z
- **Updated**: 2024-07-19T10:58:06Z
- **Closed**: 2024-07-19T10:58:06Z
- **Labels**: `kind/bug`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 2

## Description

**What happened**:
unit test flaked as a timestamp didn't match
https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/2633/pull-kueue-test-unit-main/1813897188141436928 during CI run on #2633

```
=== FAIL: pkg/controller/jobs/pod TestReconciler/deleted_unschedulable_pods_are_finalized (0.08s)
    reconciler.go:313: "level"=2 "msg"="Reconciling Job" "job"="group/ns/test-group" "gvk"="/v1, Kind=Pod"
    reconciler.go:454: "level"=2 "msg"="Job admitted, unsuspending" "job"="group/ns/test-group" "gvk"="/v1, Kind=Pod"
    pod_controller_test.go:4735: Pods after reconcile (-want,+got):
          []v1.Pod{
          	{ObjectMeta: {Name: "pod1", Namespace: "ns", UID: "test-uid", CreationTimestamp: {Time: s"2024-07-18 10:29:26 +0000 UTC"}, ...}, Spec: {Containers: {{Name: "c", Resources: {Requests: {s"cpu": {i: {...}, s: "1", Format: "DecimalSI"}}}}}, RestartPolicy: "Never"}, Status: {Phase: "Running"}},
          	{
          		... // 1 ignored field
          		ObjectMeta: v1.ObjectMeta{
          			... // 1 ignored and 5 identical fields
          			Generation:        0,
        - 			CreationTimestamp: v1.Time{Time: s"2024-07-18 11:29:27 +0000 UTC"},
        + 			CreationTimestamp: v1.Time{Time: s"2024-07-18 11:29:26 +0000 UTC"},
          			... // 1 ignored and 6 identical fields
          		},
          		Spec:   {Containers: {{Name: "c", Resources: {Requests: {s"cpu": {i: {...}, s: "1", Format: "DecimalSI"}}}}}, RestartPolicy: "Never"},
          		Status: {},
          	},
          }
=== FAIL: pkg/controller/jobs/pod TestReconciler (3.21s)
```

When fixing this bug, we should fix other places where this error could occur in the suite (or perhaps more globally)

cc @mimowo

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-07-18T12:07:04Z

/cc @alculquicondor @mbobrovskyi

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-07-18T14:04:40Z

/assign
