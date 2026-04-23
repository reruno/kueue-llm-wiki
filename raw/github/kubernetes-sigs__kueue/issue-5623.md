# Issue #5623: Workloads deactivated by Kueue are not deleted after Kueue restart (ObjectRetentionPolicies)

**Summary**: Workloads deactivated by Kueue are not deleted after Kueue restart (ObjectRetentionPolicies)

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5623

**Last updated**: 2025-06-12T07:44:57Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-06-11T12:52:43Z
- **Updated**: 2025-06-12T07:44:57Z
- **Closed**: 2025-06-12T07:44:57Z
- **Labels**: `kind/bug`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 2

## Description

**What happened**:

Jobs which were deactivated before Kueue upgrade to 0.12.2, are not garbage-collected (deleted) even when ObjectRetentionPolicies are enabled, as described here: https://kueue.sigs.k8s.io/docs/tasks/manage/setup_object_retention_policy/

Same would happen if Kueue is rebooted in the meanhwile.

**What you expected to happen**:

Kueue deletes deactivated workloads even if they were deactivated before upgrade or restart.

**How to reproduce it (as minimally and precisely as possible)**:

1. Install Kueue 0.12.2 and disable ObjectRetentionPolicies by setting false, and configure waitForPodsReady and object retention policies as described in https://kueue.sigs.k8s.io/docs/tasks/manage/setup_object_retention_policy/
2. Create a Job which has node selector which does not allow to run it, it will get deactivated after 2min
3. Enable ObjectRetentionPolicies by setting true, and restart kueue
*Issue*: the workload is not deleted

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-11T12:53:03Z

cc @mbobrovskyi @mykysha @mwysokin ptal

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-06-11T13:41:02Z

/assign
