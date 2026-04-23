# Issue #6950: [flaky test] should update workload TopologyAssignment after a node recovers

**Summary**: [flaky test] should update workload TopologyAssignment after a node recovers

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6950

**Last updated**: 2025-09-23T14:00:30Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-09-23T07:40:51Z
- **Updated**: 2025-09-23T14:00:30Z
- **Closed**: 2025-09-23T14:00:30Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@pajakd](https://github.com/pajakd)
- **Comments**: 3

## Description

**What happened**:

https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-integration-main/1970379300045590528

**What you expected to happen**:
no failure
**How to reproduce it (as minimally and precisely as possible)**:
ci
**Anything else we need to know?**:

```
TopologyAwareScheduling Suite: [It] Topology Aware Scheduling when Single TAS Resource Flavor when Nodes are created before test with the hostname being the lowest level should update workload TopologyAssignment after a node recovers expand_less	14s
{Timed out after 10.000s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/integration/singlecluster/tas/tas_test.go:1224 with:
Expected object to be comparable, diff:   &v1beta1.TopologyAssignment{
  	Levels: {"kubernetes.io/hostname"},
  	Domains: []v1beta1.TopologyDomainAssignment{
  		{
- 			Values: []string{"x2"},
+ 			Values: []string{"x1"},
  			Count:  1,
  		},
  		{
- 			Values: []string{"x3"},
+ 			Values: []string{"x2"},
  			Count:  1,
  		},
  	},
  }
 failed [FAILED] Timed out after 10.000s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/integration/singlecluster/tas/tas_test.go:1224 with:
Expected object to be comparable, diff:   &v1beta1.TopologyAssignment{
  	Levels: {"kubernetes.io/hostname"},
  	Domains: []v1beta1.TopologyDomainAssignment{
  		{
- 			Values: []string{"x2"},
+ 			Values: []string{"x1"},
  			Count:  1,
  		},
  		{
- 			Values: []string{"x3"},
+ 			Values: []string{"x2"},
  			Count:  1,
  		},
  	},
  }
In [It] at: /home/prow/go/src/kubernetes-sigs/kueue/test/integration/singlecluster/tas/tas_test.go:1234 @ 09/23/25 07:07:07.751
}
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-23T07:41:11Z

cc @PBundyra @pajakd seems like Node Hot Swap related flake?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-23T07:41:18Z

/kind flake

### Comment by [@pajakd](https://github.com/pajakd) — 2025-09-23T08:25:37Z

/assign
