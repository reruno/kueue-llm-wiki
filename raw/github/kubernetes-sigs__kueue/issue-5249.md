# Issue #5249: Flaky integration test for object retention policy

**Summary**: Flaky integration test for object retention policy

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5249

**Last updated**: 2025-05-15T14:57:16Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-05-14T13:43:20Z
- **Updated**: 2025-05-15T14:57:16Z
- **Closed**: 2025-05-15T14:57:15Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mykysha](https://github.com/mykysha)
- **Comments**: 1

## Description



**What happened**:

The test failed on unrelated branch  ObjectRetentionPolicies with TinyTimeout when workload has finished should delete the Workload

https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/5248/pull-kueue-test-e2e-customconfigs-main/1922642913863405568

**What you expected to happen**:

no failures

**How to reproduce it (as minimally and precisely as possible)**:

**Anything else we need to know?**:

```
{Timed out after 10.000s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/customconfigs/objectretentionpolicies_test.go:104 with:
Error matcher expects an error.  Got:
    <nil>: nil failed [FAILED] Timed out after 10.000s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/customconfigs/objectretentionpolicies_test.go:104 with:
Error matcher expects an error.  Got:
    <nil>: nil
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/customconfigs/objectretentionpolicies_test.go:105 @ 05/14/25 13:33:38.051
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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-14T13:44:12Z

/kind flake
/assign @mykysha
tentatively, as one of the main contributors working on the object retention policy
ptal
