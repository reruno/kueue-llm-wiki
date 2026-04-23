# Issue #1540: integration test for MultiKueue is flaky

**Summary**: integration test for MultiKueue is flaky

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1540

**Last updated**: 2024-01-11T15:49:59Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-01-03T14:18:49Z
- **Updated**: 2024-01-11T15:49:59Z
- **Closed**: 2024-01-11T15:49:59Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 4

## Description

**What happened**:

Integration test "Multikueue Suite: [It] Multikueue when Using multiple clusters Cluster kubeconfig propagation worker1" 
fails occasionally on unrelated branches.

**Anything else we need to know?**:

Example failure: 
https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/1397/pull-kueue-test-integration-main/1742541526778515456

Details below in case the link expires.

```
{  &v1beta1.Workload{
  	TypeMeta: {},
  	ObjectMeta: v1.ObjectMeta{
  		... // 3 identical fields
  		SelfLink:          "",
  		UID:               "91e52491-ea73-4180-8069-10d9cf949772",
- 		ResourceVersion:   "218",
+ 		ResourceVersion:   "219",
  		Generation:        1,
  		CreationTimestamp: {Time: s"2024-01-03 13:56:17 +0000 UTC"},
  		... // 4 identical fields
  		OwnerReferences: nil,
  		Finalizers:      nil,
  		ManagedFields: []v1.ManagedFieldsEntry{
+ 			{
+ 				Manager:     "kueue-admission",
+ 				Operation:   "Apply",
+ 				APIVersion:  "kueue.x-k8s.io/v1beta1",
+ 				Time:        s"2024-01-03 13:56:17 +0000 UTC",
+ 				FieldsType:  "FieldsV1",
+ 				FieldsV1:    s`{"f:status":{"f:conditions":{"k:{\"type\":\"QuotaReserved\"}":{".":{},"f:lastTransitionTime":{},"f:message":{},"f:reason":{},"f:`...,
+ 				Subresource: "status",
+ 			},
  			{Manager: "multikueue.test", Operation: "Update", APIVersion: "kueue.x-k8s.io/v1beta1", Time: s"2024-01-03 13:56:17 +0000 UTC", ...},
  		},
  	},
  	Spec: {PodSets: {{Name: "main", Template: {Spec: {Containers: {{Name: "c"}}, RestartPolicy: "Never"}}, Count: 1}}, Active: &true},
  	Status: v1beta1.WorkloadStatus{
  		Admission:  nil,
- 		Conditions: nil,
+ 		Conditions: []v1.Condition{
+ 			{
+ 				Type:               "QuotaReserved",
+ 				Status:             "False",
+ 				LastTransitionTime: s"2024-01-03 13:56:17 +0000 UTC",
+ 				Reason:             "Inadmissible",
+ 				Message:            "LocalQueue  doesn't exist",
+ 			},
+ 		},
  		ReclaimablePods: nil,
  		AdmissionChecks: nil,
  	},
  }
 failed [FAILED]   &v1beta1.Workload{
  	TypeMeta: {},
  	ObjectMeta: v1.ObjectMeta{
  		... // 3 identical fields
  		SelfLink:          "",
  		UID:               "91e52491-ea73-4180-8069-10d9cf949772",
- 		ResourceVersion:   "218",
+ 		ResourceVersion:   "219",
  		Generation:        1,
  		CreationTimestamp: {Time: s"2024-01-03 13:56:17 +0000 UTC"},
  		... // 4 identical fields
  		OwnerReferences: nil,
  		Finalizers:      nil,
  		ManagedFields: []v1.ManagedFieldsEntry{
+ 			{
+ 				Manager:     "kueue-admission",
+ 				Operation:   "Apply",
+ 				APIVersion:  "kueue.x-k8s.io/v1beta1",
+ 				Time:        s"2024-01-03 13:56:17 +0000 UTC",
+ 				FieldsType:  "FieldsV1",
+ 				FieldsV1:    s`{"f:status":{"f:conditions":{"k:{\"type\":\"QuotaReserved\"}":{".":{},"f:lastTransitionTime":{},"f:message":{},"f:reason":{},"f:`...,
+ 				Subresource: "status",
+ 			},
  			{Manager: "multikueue.test", Operation: "Update", APIVersion: "kueue.x-k8s.io/v1beta1", Time: s"2024-01-03 13:56:17 +0000 UTC", ...},
  		},
  	},
  	Spec: {PodSets: {{Name: "main", Template: {Spec: {Containers: {{Name: "c"}}, RestartPolicy: "Never"}}, Count: 1}}, Active: &true},
  	Status: v1beta1.WorkloadStatus{
  		Admission:  nil,
- 		Conditions: nil,
+ 		Conditions: []v1.Condition{
+ 			{
+ 				Type:               "QuotaReserved",
+ 				Status:             "False",
+ 				LastTransitionTime: s"2024-01-03 13:56:17 +0000 UTC",
+ 				Reason:             "Inadmissible",
+ 				Message:            "LocalQueue  doesn't exist",
+ 			},
+ 		},
  		ReclaimablePods: nil,
  		AdmissionChecks: nil,
  	},
  }
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/integration/multikueue/multikueue_test.go:108 @ 01/03/24 13:56:17.995
}
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-01-03T14:19:21Z

/kind flake

### Comment by [@mimowo](https://github.com/mimowo) — 2024-01-03T14:19:34Z

cc @trasc

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-01-05T04:16:14Z

I guess that this is similar to https://github.com/kubernetes-sigs/kueue/issues/1490.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-01-10T10:56:22Z

/assign @trasc
