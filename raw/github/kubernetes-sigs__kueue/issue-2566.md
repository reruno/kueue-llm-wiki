# Issue #2566: JobReconciler does not retry to reset start time and restore info after error on stop job.

**Summary**: JobReconciler does not retry to reset start time and restore info after error on stop job.

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2566

**Last updated**: 2024-07-10T19:11:24Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2024-07-09T16:43:40Z
- **Updated**: 2024-07-10T19:11:24Z
- **Closed**: 2024-07-10T19:11:24Z
- **Labels**: `kind/bug`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 2

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->

**What happened**:
`JobReconciler` does not retry to reset start time and restore info after error on stop job. This happening if the job was successfully suspended but on reset start time https://github.com/kubernetes-sigs/kueue/blob/dc73a33849ce6b76093eca1aade29cfe390d63a5/pkg/controller/jobs/job/job_controller.go#L179 or restore info https://github.com/kubernetes-sigs/kueue/blob/dc73a33849ce6b76093eca1aade29cfe390d63a5/pkg/controller/jobs/job/job_controller.go#L187 an error occurs. 

On this case re-try will not be attempted because `JobReconciler` skipping all not suspended jobs https://github.com/kubernetes-sigs/kueue/blob/dc73a33849ce6b76093eca1aade29cfe390d63a5/pkg/controller/jobframework/reconciler.go#L600.

**What you expected to happen**:
Retry to reset start time and restore info after error on stop job

**How to reproduce it (as minimally and precisely as possible)**:

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

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-07-09T16:44:23Z

/cc @alculquicondor @mimowo

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-07-09T16:45:29Z

/assign
