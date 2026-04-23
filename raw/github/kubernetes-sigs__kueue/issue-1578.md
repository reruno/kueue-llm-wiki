# Issue #1578: Flaky UT: preemption_while_borrowing,_workload_waiting_for_preemption_should_not_block_a_borrowing_workload_in_another_CQ

**Summary**: Flaky UT: preemption_while_borrowing,_workload_waiting_for_preemption_should_not_block_a_borrowing_workload_in_another_CQ

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1578

**Last updated**: 2024-01-15T16:01:26Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2024-01-13T16:16:13Z
- **Updated**: 2024-01-15T16:01:26Z
- **Closed**: 2024-01-15T16:01:26Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mimowo](https://github.com/mimowo)
- **Comments**: 1

## Description

**What happened**:

/kind flake

```
    scheduler_test.go:1343: Unexpected elements left in the queue (-want,+got):
          map[string][]string(
        - 	nil,
        + 	{"cq_a": {"eng-alpha/a"}},
          )
    scheduler_test.go:1347: Unexpected elements left in inadmissible workloads (-want,+got):
          map[string][]string(
        - 	{"cq_a": {"eng-alpha/a"}},
        + 	nil,
          )
```

**What you expected to happen**:

**How to reproduce it (as minimally and precisely as possible)**:

https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/1577/pull-kueue-test-unit-main/1746201565619818496

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

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-01-13T16:16:22Z

/assign @mimowo
