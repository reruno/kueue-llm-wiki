# Issue #6883: [flaky test] StatefulSet created should allow to change queue name if ReadyReplicas

**Summary**: [flaky test] StatefulSet created should allow to change queue name if ReadyReplicas

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6883

**Last updated**: 2025-12-05T17:28:59Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-09-17T08:36:31Z
- **Updated**: 2025-12-05T17:28:59Z
- **Closed**: 2025-12-05T17:28:59Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 3

## Description

**What happened**:

failure https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-main-1-34/1968220530033037312

**What you expected to happen**:
no failure
**How to reproduce it (as minimally and precisely as possible)**:
ci
**Anything else we need to know?**:

```
End To End Suite: kindest/node:v1.34.0: [It] StatefulSet integration when StatefulSet created should allow to change queue name if ReadyReplicas=0 expand_less	47s
{Timed out after 45.001s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/singlecluster/statefulset_test.go:377 with:
Expected
    <int32>: 0
to equal
    <int32>: 3 failed [FAILED] Timed out after 45.001s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/singlecluster/statefulset_test.go:377 with:
Expected
    <int32>: 0
to equal
    <int32>: 3
In [It] at: /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/singlecluster/statefulset_test.go:378 @ 09/17/25 08:12:43.533
}
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-17T08:36:54Z

/kind flake
cc @mbobrovskyi who worked on the StatefulSet integration so may have some ideas

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2025-09-23T17:49:37Z

It looks like the approach discussed in https://github.com/kubernetes-sigs/kueue/issues/5041 didn't help much. Are we open to increase the timeout to `VeryLongTimeout` and see if that helps?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-04T09:46:16Z

I think this is likely the same issue as solved in https://github.com/kubernetes-sigs/kueue/pull/7479

so we would add here https://github.com/kubernetes-sigs/kueue/pull/7479/files#diff-a223a8237dd26861e7b3bbfa6f4fd1bb35636045af13214b6a01f4b5f24b4116R143-R146 the analogous check.

cc @IrvingMg @mbobrovskyi 

EDIT: My comment is related to the new PR attempting to fix: https://github.com/kubernetes-sigs/kueue/pull/7512
