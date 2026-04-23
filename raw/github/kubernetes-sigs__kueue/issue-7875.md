# Issue #7875: [flaky test] TopologyAwareScheduling when Creating a Job requesting TAS should admit a Job via TAS

**Summary**: [flaky test] TopologyAwareScheduling when Creating a Job requesting TAS should admit a Job via TAS

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7875

**Last updated**: 2025-11-25T13:22:39Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-11-25T10:20:26Z
- **Updated**: 2025-11-25T13:22:39Z
- **Closed**: 2025-11-25T13:22:39Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mimowo](https://github.com/mimowo)
- **Comments**: 2

## Description

/kind flake 

**What happened**:

https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/7859/pull-kueue-test-e2e-main-1-33/1993025952111661056

failure on unrelated branch

**What you expected to happen**:
no failure

**How to reproduce it (as minimally and precisely as possible)**:
ci
**Anything else we need to know?**:


```

End To End Suite: kindest/node:v1.33.4: [It] TopologyAwareScheduling when Creating a Job requesting TAS should admit a Job via TAS expand_less	12s
{Timed out after 10.000s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/util/util.go:1084 with:
Expected
    <*bool | 0xc000c0e36a>: true
to equal
    <*bool | 0xc000c0e570>: false failed [FAILED] Timed out after 10.000s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/util/util.go:1084 with:
Expected
    <*bool | 0xc000c0e36a>: true
to equal
    <*bool | 0xc000c0e570>: false
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/tas_test.go:111 @ 11/24/25 19:23:41.821
}

```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-25T10:28:40Z

I think this is likely because of a delay, seems like the order of checks is suboptimial: https://github.com/kubernetes-sigs/kueue/blob/main/test/e2e/singlecluster/tas_test.go#L109-L137, because the Workload is actually admitted first, then job is unsuspended. So I would try checking if workload admitted first.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-25T10:44:33Z

/assign
