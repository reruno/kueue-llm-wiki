# Issue #5164: The CustomConfig e2e test is cleaning up logs in AfterSuite.

**Summary**: The CustomConfig e2e test is cleaning up logs in AfterSuite.

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5164

**Last updated**: 2025-05-06T06:15:16Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2025-05-05T13:18:47Z
- **Updated**: 2025-05-06T06:15:16Z
- **Closed**: 2025-05-06T06:15:16Z
- **Labels**: `kind/bug`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 1

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
The CustomConfig e2e test restarting Kueue and cleans up logs in AfterSuite

https://github.com/kubernetes-sigs/kueue/blob/3d4725b8553082570b86ad7b81120570c26ea5fa/test/e2e/customconfigs/suite_test.go#L75

and in updateKueueConfiguration()

https://github.com/kubernetes-sigs/kueue/blob/3d4725b8553082570b86ad7b81120570c26ea5fa/test/e2e/customconfigs/suite_test.go#L84

, even when errors occur. 

For example, in #5106 and #5144 we only retain the logs from the last restart.

**What you expected to happen**:
Logs should be preserved in the artifacts.

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

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-05-05T14:50:40Z

/assign
