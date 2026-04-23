# Issue #3890: [Flaky test]  Topology Aware Scheduling when Single TAS Resource Flavor when Nodes are created before test with rack ...

**Summary**: [Flaky test]  Topology Aware Scheduling when Single TAS Resource Flavor when Nodes are created before test with rack ...

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3890

**Last updated**: 2025-01-15T13:30:41Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-12-19T10:26:17Z
- **Updated**: 2025-01-15T13:30:41Z
- **Closed**: 2025-01-15T13:30:41Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mykysha](https://github.com/mykysha)
- **Comments**: 7

## Description

/kind flake
/kind bug

**What happened**:

test flaked: TopologyAwareScheduling Suite.[It] Topology Aware Scheduling when Single TAS Resource Flavor when Nodes are created before test with rack being the lowest level should not admit the workload after the topology is deleted but should admit it after the topology is created

Failure on the 0.10 branch: https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-integration-release-0-10/1869374748694155264

Dashboard: https://testgrid.k8s.io/sig-scheduling#periodic-kueue-test-integration-release-0-10

![image](https://github.com/user-attachments/assets/fb172b7a-54d4-4443-bf83-a4ca35656dba)


**What you expected to happen**:

No random failures

**How to reproduce it (as minimally and precisely as possible)**:

CI 

**Anything else we need to know?**:

```
{Timed out after 5.000s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/util/util.go:94 with:
Error matcher expects an error.  Got:
    <nil>: nil failed [FAILED] Timed out after 5.000s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/util/util.go:94 with:
Error matcher expects an error.  Got:
    <nil>: nil
In [It] at: /home/prow/go/src/kubernetes-sigs/kueue/test/integration/tas/tas_test.go:585 @ 12/18/24 13:47:48.162
}
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-19T10:26:33Z

cc @PBundyra @mbobrovskyi PTAL

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-12-19T10:32:34Z

/assign

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-12-23T05:38:38Z

/reopen

It happens again https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/3870/pull-kueue-test-integration-main/1871059509439369216.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-12-23T05:38:43Z

@mbobrovskyi: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3890#issuecomment-2558945672):

>/reopen
>
>It happens again https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/3870/pull-kueue-test-integration-main/1871059509439369216.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-12-23T08:44:38Z

/unassign

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-12-23T09:25:50Z

/assign @mykysha

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-12-23T10:54:32Z

https://github.com/kubernetes-sigs/kueue/pull/3907
https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/3907/pull-kueue-test-integration-main/1871140236172464128
