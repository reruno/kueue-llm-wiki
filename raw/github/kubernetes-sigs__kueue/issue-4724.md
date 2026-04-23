# Issue #4724: LWS workloads get deleted on preemption

**Summary**: LWS workloads get deleted on preemption

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4724

**Last updated**: 2025-04-16T18:27:12Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-03-20T17:35:24Z
- **Updated**: 2025-04-16T18:27:12Z
- **Closed**: 2025-04-16T18:27:12Z
- **Labels**: `kind/bug`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 2

## Description

**What happened**:

When LWS workload for a group is preempted it is deleted and recreated. See discussion in https://github.com/kubernetes-sigs/kueue/pull/4711/files#diff-8be708e6a6046713666b607889f5a2fd5f69f817a0a2815c62b03f725f6ab34fR798

However, this is an issue because then the state of the workload is lost. There might be important state with waitForPodsReady information. It also means the "active" field does not work.

**What you expected to happen**:

The preempted workload should not be deleted and recreated.

**How to reproduce it (as minimally and precisely as possible)**:

Follow the steps in the e2e test in https://github.com/kubernetes-sigs/kueue/pull/4711/files#diff-8be708e6a6046713666b607889f5a2fd5f69f817a0a2815c62b03f725f6ab34fR670

**Anything else we need to know?**:

We have analogous issue for StatefulSet https://github.com/kubernetes-sigs/kueue/issues/4342

I think just adding owner reference for the workload to LWS would solve the problem.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-20T17:35:47Z

/cc @mbobrovskyi

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-03-21T13:07:49Z

/assign
