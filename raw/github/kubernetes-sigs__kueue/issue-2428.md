# Issue #2428: Flaky e2e test for JobSet

**Summary**: Flaky e2e test for JobSet

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2428

**Last updated**: 2024-06-21T17:43:03Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@PBundyra](https://github.com/PBundyra)
- **Created**: 2024-06-17T21:45:53Z
- **Updated**: 2024-06-21T17:43:03Z
- **Closed**: 2024-06-21T17:43:03Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 1

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->
/kind flake

**What happened**:
Flaky test for JobSet "JobSet when Creating a JobSet Should run a jobSet if admitted"

**What you expected to happen**:
No failure

**How to reproduce it (as minimally and precisely as possible)**:
https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/2408/pull-kueue-test-e2e-main-1-28/1802723422271180800

## Discussion

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-06-20T07:19:02Z

/assign
