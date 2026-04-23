# Issue #2822: [Flaky test] E2e test for visibility fails occasionally

**Summary**: [Flaky test] E2e test for visibility fails occasionally

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2822

**Last updated**: 2024-08-13T11:31:05Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-08-12T11:37:28Z
- **Updated**: 2024-08-13T11:31:05Z
- **Closed**: 2024-08-13T11:31:05Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 2

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->

/kind flake

**What happened**:

This test failed on unrelated branch: "Kueue visibility server when There are pending workloads due to capacity maxed by the admitted job Should allow fetching information about pending workloads in LocalQueue"

https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/2815/pull-kueue-test-e2e-main-1-28/1822956531436490752

**What you expected to happen**:

No random failures

**How to reproduce it (as minimally and precisely as possible)**:

Repeat the build on CI

**Anything else we need to know?**:

```
{Timed out after 5.001s.
Expected
    <int>: 0
to equal
    <int>: 1 failed [FAILED] Timed out after 5.001s.
Expected
    <int>: 0
to equal
    <int>: 1
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/visibility_test.go:295 @ 08/12/24 11:29:52.171
}
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-08-12T11:38:21Z

/cc @mbobrovskyi @trasc

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-08-12T11:51:26Z

/assign
