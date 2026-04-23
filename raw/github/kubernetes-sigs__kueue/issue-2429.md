# Issue #2429: Flaky e2e test for Pod groups

**Summary**: Flaky e2e test for Pod groups

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2429

**Last updated**: 2024-07-08T07:48:44Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@PBundyra](https://github.com/PBundyra)
- **Created**: 2024-06-17T21:47:01Z
- **Updated**: 2024-07-08T07:48:44Z
- **Closed**: 2024-07-08T07:48:44Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 1

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->

/kind flake

**What happened**:
E2e test for Pod groups "Pod groups when Single CQ should allow to preempt the lower priority group" failed

**What you expected to happen**:
No failuer

**How to reproduce it (as minimally and precisely as possible)**:
https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/2408/pull-kueue-test-e2e-main-1-29/1802723422350872576

## Discussion

### Comment by [@mszadkow](https://github.com/mszadkow) — 2024-06-20T09:14:12Z

/assign
