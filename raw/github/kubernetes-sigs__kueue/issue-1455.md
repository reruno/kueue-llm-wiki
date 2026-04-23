# Issue #1455: The scheduler unit test "only one workload can borrow one resources from the same flavor..." flakes

**Summary**: The scheduler unit test "only one workload can borrow one resources from the same flavor..." flakes

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1455

**Last updated**: 2023-12-14T17:17:51Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2023-12-14T10:27:25Z
- **Updated**: 2023-12-14T17:17:51Z
- **Closed**: 2023-12-14T17:17:51Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@alculquicondor](https://github.com/alculquicondor)
- **Comments**: 4

## Description

/kind bug
/kind flake

**What happened**:

Failed unit test: `sigs.k8s.io/kueue/pkg/scheduler: TestSchedule/only_one_workload_can_borrow_one_resources_from_the_same_flavor_in_the_same_cycle_if_cohort_quota_cannot_fit ` with output:

```
  scheduler_test.go:1120: Unexpected scheduled workloads (-want,+got):
          map[string]v1beta1.Admission{
        - 	"sales/wl1": {
        - 		ClusterQueue: "cq1",
        - 		PodSetAssignments: []v1beta1.PodSetAssignment{
        - 			{
        - 				Name:          "main",
        - 				Flavors:       map[v1.ResourceName]v1beta1.ResourceFlavorReference{...},
        - 				ResourceUsage: v1.ResourceList{...},
        - 				Count:         &1,
        - 			},
        - 		},
        - 	},
        + 	"sales/wl2": {
        + 		ClusterQueue: "cq2",
        + 		PodSetAssignments: []v1beta1.PodSetAssignment{
        + 			{
        + 				Name:          "main",
        + 				Flavors:       map[v1.ResourceName]v1beta1.ResourceFlavorReference{...},
        + 				ResourceUsage: v1.ResourceList{...},
        + 				Count:         &1,
        + 			},
        + 		},
        + 	},
          }
    scheduler_test.go:1145: Unexpected assigned clusterQueues in cache (-want,+got):
          map[string]v1beta1.Admission{
        - 	"sales/wl1": {
        - 		ClusterQueue: "cq1",
        - 		PodSetAssignments: []v1beta1.PodSetAssignment{
        - 			{
        - 				Name:          "main",
        - 				Flavors:       map[v1.ResourceName]v1beta1.ResourceFlavorReference{...},
        - 				ResourceUsage: v1.ResourceList{...},
        - 				Count:         &1,
        - 			},
        - 		},
        - 	},
        + 	"sales/wl2": {
        + 		ClusterQueue: "cq2",
        + 		PodSetAssignments: []v1beta1.PodSetAssignment{
        + 			{
        + 				Name:          "main",
        + 				Flavors:       map[v1.ResourceName]v1beta1.ResourceFlavorReference{...},
        + 				ResourceUsage: v1.ResourceList{...},
        + 				Count:         &1,
        + 			},
        + 		},
        + 	},
          }
    scheduler_test.go:1150: Unexpected elements left in the queue (-want,+got):
          map[string]sets.Set[string]{
        + 	"cq1": {"sales/wl1": {}},
        - 	"cq2": {"sales/wl2": {}},
          }
--- FAIL: TestSchedule/only_one_workload_can_borrow_one_resources_from_the_same_flavor_in_the_same_cycle_if_cohort_quota_cannot_fit (0.07s)
```

**What you expected to happen**:

No failure

**How to reproduce it (as minimally and precisely as possible)**:

https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/1405/pull-kueue-test-unit-main/1735227794121560064

**Anything else we need to know?**:

I think this is the second time I see it

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2023-12-14T10:27:53Z

cc @alculquicondor @tenzen-y @trasc

### Comment by [@mimowo](https://github.com/mimowo) — 2023-12-14T11:58:09Z

Seems to be failing rather often, other occurrences from various branches 
https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/1453/pull-kueue-test-unit-main/1735103635500568576
https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/1385/pull-kueue-test-unit-main/1735205083513098240
https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/1405/pull-kueue-test-unit-main/1734612685380653056
https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/1358/pull-kueue-test-unit-main/1734584641630769152

Looking at the job history the first failure for this reason was here Dec 12: https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/1428/pull-kueue-test-unit-main/1734553555177574400

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-12-14T14:14:24Z

/assign @trasc

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-12-14T15:01:36Z

The dates point to #1406 as the culprit. We just need to enable the feature.

/assign
/unassign trasc
