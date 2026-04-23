# Issue #6726: [Failing tests] Release branches are failing

**Summary**: [Failing tests] Release branches are failing

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6726

**Last updated**: 2025-09-05T12:58:56Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-09-04T17:34:57Z
- **Updated**: 2025-09-05T12:58:56Z
- **Closed**: 2025-09-05T12:58:55Z
- **Labels**: `kind/bug`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 5

## Description

**What happened**:

The release branches are failing recently:

<img width="1926" height="426" alt="Image" src="https://github.com/user-attachments/assets/1347ae71-7156-4db6-bfbe-800917b100bd" />

https://testgrid.k8s.io/sig-scheduling#periodic-kueue-test-scheduling-perf-release-0-13
and https://testgrid.k8s.io/sig-scheduling#periodic-kueue-test-unit-release-0-13

**What you expected to happen**:

no failures

**How to reproduce it (as minimally and precisely as possible)**:

ci

**Anything else we need to know?**:

```
make[1]: Entering directory '/home/prow/go/src/kubernetes-sigs/kueue'
# golang.org/x/tools/internal/tokeninternal
../../../pkg/mod/golang.org/x/tools@v0.24.0/internal/tokeninternal/tokeninternal.go:64:9: invalid array length -delta * delta (constant -256 of type int64)
make[1]: *** [Makefile-deps.mk:87: gotestsum] Error 1
make[1]: Leaving directory '/home/prow/go/src/kubernetes-sigs/kueue'
make: *** [Makefile-test.mk:249: test-performance-scheduler] Error 2
```

This seems like addressed by https://github.com/kubernetes-sigs/kueue/pull/6722 on the main branch

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-04T17:35:24Z

cc @mbobrovskyi who fixed the issue on the main branch in https://github.com/kubernetes-sigs/kueue/pull/6722

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-09-04T20:15:09Z

/assign

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-09-04T20:16:28Z

Yeah, this happens because we need to cherry-pick https://github.com/kubernetes-sigs/kueue/pull/6722 to the release branches. Created PR for this https://github.com/kubernetes-sigs/kueue/pull/6727.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-05T12:58:51Z

/close 
as the PRs are merged

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-09-05T12:58:56Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/6726#issuecomment-3258262507):

>/close 
>as the PRs are merged


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
