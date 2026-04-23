# Issue #2454: Flaky integration test: Should print cluster queues list with paging

**Summary**: Flaky integration test: Should print cluster queues list with paging

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2454

**Last updated**: 2024-06-21T09:32:55Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2024-06-20T05:20:19Z
- **Updated**: 2024-06-21T09:32:55Z
- **Closed**: 2024-06-21T09:32:55Z
- **Labels**: `kind/bug`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 1

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
Integration test failed: https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/2452/pull-kueue-test-integration-main/1803655079367020544.

**What you expected to happen**:
No flake

**How to reproduce it (as minimally and precisely as possible)**:
Repeat the build.

**Anything else we need to know?**:

```
{Expected
    <string>: "...AGE
    cluster..."
to equal               |
    <string>: "...AGE
    cq1    ..." failed [FAILED] Expected
    <string>: "...AGE
    cluster..."
to equal               |
    <string>: "...AGE
    cq1    ..."
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/integration/kueuectl/list_test.go:178 @ 06/20/24 05:11:36.562
}
```

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-06-20T05:29:15Z

/assign
