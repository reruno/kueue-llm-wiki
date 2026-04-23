# Issue #495: Flaky e2e: Failed calling webhook in k8s v1.23

**Summary**: Flaky e2e: Failed calling webhook in k8s v1.23

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/495

**Last updated**: 2022-12-22T18:59:27Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2022-12-22T18:43:39Z
- **Updated**: 2022-12-22T18:59:27Z
- **Closed**: 2022-12-22T18:59:27Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 0

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
The webhook call timed out in e2e for k8s v1.23.

**What you expected to happen**:
I expected to succeed in e2e.

**How to reproduce it (as minimally and precisely as possible)**:
https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/415/pull-kueue-test-e2e-main-1-23/1605990854189649920

**Anything else we need to know?**:
Maybe, we lift the timeout to 1 min or more.

originally posted by @alculquicondor :

```sh
Uhm.... it looks like kueue is particularly slow to start in 1.23. We have a timeout of 30s. We can easily lift this to 1 min or more.
```

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:
