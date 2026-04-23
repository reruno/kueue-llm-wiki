# Issue #7803: [flaky unit tests] TestReconciler/when_workload_is_admitted_and_PodSetUpdates_conflict_between_admission_checks_on_annotations,_the_workload_is_finished_with_failure_WorkloadRequestUseMergePatch_enabled:_false

**Summary**: [flaky unit tests] TestReconciler/when_workload_is_admitted_and_PodSetUpdates_conflict_between_admission_checks_on_annotations,_the_workload_is_finished_with_failure_WorkloadRequestUseMergePatch_enabled:_false

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7803

**Last updated**: 2025-11-21T09:58:35Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-11-21T08:17:09Z
- **Updated**: 2025-11-21T09:58:35Z
- **Closed**: 2025-11-21T09:58:35Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 3

## Description


**What happened**:

failure: https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/7312/pull-kueue-test-unit-main/1991776223881072640

**What you expected to happen**:
no fail
**How to reproduce it (as minimally and precisely as possible)**:
ci
**Anything else we need to know?**:
```
sigs.k8s.io/kueue/pkg/controller/jobs/job: TestReconciler/when_workload_is_admitted_and_PodSetUpdates_conflict_between_admission_checks_on_annotations,_the_workload_is_finished_with_failure_WorkloadRequestUseMergePatch_enabled:_false expand_more
sigs.k8s.io/kueue/pkg/controller/jobs/job: TestReconciler/when_workload_is_admitted_and_PodSetUpdates_conflict_between_admission_checks_on_annotations,_the_workload_is_finished_with_failure_WorkloadRequestUseMergePatch_enabled:_true expand_more
sigs.k8s.io/kueue/pkg/controller/jobs/job: TestReconciler/when_workload_is_admitted_and_PodSetUpdates_conflict_between_admission_check_nodeSelector_and_current_node_selector,_the_workload_is_finished_with_failure_WorkloadRequestUseMergePatch_enabled:_false expand_more
sigs.k8s.io/kueue/pkg/controller/jobs/job: TestReconciler/when_workload_is_admitted_and_PodSetUpdates_conflict_between_admission_check_nodeSelector_and_current_node_selector,_the_workload_is_finished_with_failure_WorkloadRequestUseMergePatch_enabled:_true expand_more
sigs.k8s.io/kueue/pkg/controller/jobs/job: TestReconciler/when_workload_is_admitted_and_PodSetUpdates_conflict_between_admission_checks_on_labels,_the_workload_is_finished_with_failure_WorkloadRequestUseMergePatch_enabled:_false expand_more
sigs.k8s.io/kueue/pkg/controller/jobs/job: TestReconciler/when_workload_is_admitted_and_PodSetUpdates_conflict_between_admission_checks_on_labels,_the_workload_is_finished_with_failure_WorkloadRequestUseMergePatch_enabled:_true expand_more
sigs.k8s.io/kueue/pkg/controller/jobs/job: TestReconciler/when_job_completes,_workload_is_marked_as_finished_WorkloadRequestUseMergePatch_enabled:_false expand_more
sigs.k8s.io/kueue/pkg/controller/jobs/job: TestReconciler/when_job_completes,_workload_is_marked_as_finished_WorkloadRequestUseMergePatch_enabled:_true expand_more
sigs.k8s.io/kueue/pkg/controller/jobs/job: TestReconciler/when_workload_is_admitted_and_PodSetUpdates_conflict_between_admission_checks_on_nodeSelector,_the_workload_is_finished_with_failure_WorkloadRequestUseMergePatch_enabled:_false expand_more
sigs.k8s.io/kueue/pkg/controller/jobs/job: TestReconciler/when_workload_is_admitted_and_PodSetUpdates_conflict_between_admission_checks_on_nodeSelector,_the_workload_is_finished_with_failure_WorkloadRequestUseMergePatch_enabled:_true expand_more
sigs.k8s.io/kueue/pkg/controller/jobs/job: TestReconciler expand_more
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-21T08:17:21Z

cc @mbobrovskyi any ideas?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-21T08:18:06Z

/kind flake

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-11-21T08:32:22Z

/assign
