# Issue #2398: Flaky integration tests for jobset controller

**Summary**: Flaky integration tests for jobset controller

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2398

**Last updated**: 2024-06-13T12:12:11Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@PBundyra](https://github.com/PBundyra)
- **Created**: 2024-06-11T12:28:36Z
- **Updated**: 2024-06-13T12:12:11Z
- **Closed**: 2024-06-13T12:12:11Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 2

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
The integration test failed

**What you expected to happen**:
Not to fail

**How to reproduce it (as minimally and precisely as possible)**:
https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/2363/pull-kueue-test-integration-main/1800218473264058368

**Anything else we need to know?**:

**Environment**:

## Discussion

### Comment by [@PBundyra](https://github.com/PBundyra) — 2024-06-11T12:29:14Z

/kind flake

### Comment by [@mszadkow](https://github.com/mszadkow) — 2024-06-12T06:28:55Z

/assign
