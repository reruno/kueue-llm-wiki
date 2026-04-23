# Issue #5588: [release-0.12] Flaky Integration Test: Scheduler when Scheduling workloads on clusterQueues Should admit workloads with admission checks

**Summary**: [release-0.12] Flaky Integration Test: Scheduler when Scheduling workloads on clusterQueues Should admit workloads with admission checks

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5588

**Last updated**: 2025-06-17T11:49:01Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2025-06-09T14:30:36Z
- **Updated**: 2025-06-17T11:49:01Z
- **Closed**: 2025-06-17T11:49:01Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 2

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
```
Scheduler Suite: [It] Scheduler when Scheduling workloads on clusterQueues Should admit workloads with admission checks 

{Timed out after 10.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/util/util.go:478 with:
Expected object to be comparable, diff:   (*v1beta1.Admission)(
- 	&{
- 		ClusterQueue: "admission-check-cq",
- 		PodSetAssignments: []v1beta1.PodSetAssignment{
- 			{
- 				Name:          "main",
- 				Flavors:       map[v1.ResourceName]v1beta1.ResourceFlavorReference{...},
- 				ResourceUsage: v1.ResourceList{...},
- 				Count:         &1,
- 			},
- 		},
- 	},
+ 	nil,
  )
 failed [FAILED] Timed out after 10.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/util/util.go:478 with:
Expected object to be comparable, diff:   (*v1beta1.Admission)(
- 	&{
- 		ClusterQueue: "admission-check-cq",
- 		PodSetAssignments: []v1beta1.PodSetAssignment{
- 			{
- 				Name:          "main",
- 				Flavors:       map[v1.ResourceName]v1beta1.ResourceFlavorReference{...},
- 				ResourceUsage: v1.ResourceList{...},
- 				Count:         &1,
- 			},
- 		},
- 	},
+ 	nil,
  )
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/integration/singlecluster/scheduler/scheduler_test.go:477 @ 06/09/25 14:20:13.105
}
```

**What you expected to happen**:
No errors

**How to reproduce it (as minimally and precisely as possible)**:
https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/5586/pull-kueue-test-integration-baseline-release-0-12/1932077407703928832

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-06-09T14:30:43Z

/kind flake

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-06-17T11:23:40Z

/assign
