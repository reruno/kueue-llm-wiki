# Issue #3299: [Flaky e2e test]  Stateful set integration when Single CQ should admit group that fits

**Summary**: [Flaky e2e test]  Stateful set integration when Single CQ should admit group that fits

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3299

**Last updated**: 2024-10-24T11:54:54Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-10-24T07:50:09Z
- **Updated**: 2024-10-24T11:54:54Z
- **Closed**: 2024-10-24T11:54:53Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 2

## Description

/kind flake 

**What happened**:

The test flaked https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-main-1-31/1849350043572637696

**What you expected to happen**:

no flakes

**How to reproduce it (as minimally and precisely as possible)**:

run on CI

**Anything else we need to know?**:

```
End To End Suite: kindest/node:v1.31.0: [It] Stateful set integration when Single CQ should admit group that fits expand_less	18s
{Timed out after 5.001s.
The matcher passed to Eventually returned the following error:
    <*errors.errorString | 0xc000212480>: 
    NotFoundError expects an error
    {
        s: "NotFoundError expects an error",
    } failed [FAILED] Timed out after 5.001s.
The matcher passed to Eventually returned the following error:
    <*errors.errorString | 0xc000212480>: 
    NotFoundError expects an error
    {
        s: "NotFoundError expects an error",
    }
In [It] at: /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/singlecluster/statefulset_test.go:130 @ 10/24/24 07:28:30.802
}
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-24T07:50:49Z

cc @mbobrovskyi @vladikkuzn

### Comment by [@mszadkow](https://github.com/mszadkow) — 2024-10-24T11:04:54Z

Happens pretty consistently in PR runs: https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/3289/pull-kueue-test-e2e-main-1-30/1849395496418807808
