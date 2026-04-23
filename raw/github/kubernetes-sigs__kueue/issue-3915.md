# Issue #3915: Flaky Test: Pod groups when Single CQ should allow to preempt the lower priority group

**Summary**: Flaky Test: Pod groups when Single CQ should allow to preempt the lower priority group

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3915

**Last updated**: 2025-01-06T20:38:32Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-01-01T00:22:52Z
- **Updated**: 2025-01-06T20:38:32Z
- **Closed**: 2025-01-06T20:38:32Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 1

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
Flaky on "End To End Suite: kindest/node:v1.31.0: [It] Pod groups when Single CQ should allow to preempt the lower priority group"

```shell
{Timed out after 5.000s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/singlecluster/pod_test.go:505 with:
Error matcher expects an error.  Got:
    <nil>: nil failed [FAILED] Timed out after 5.000s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/singlecluster/pod_test.go:505 with:
Error matcher expects an error.  Got:
    <nil>: nil
In [It] at: /home/prow/go/src/kubernetes-sigs/kueue/test/e2e/singlecluster/pod_test.go:507 @ 12/30/24 19:35:24.733
}
```

**What you expected to happen**:
No errors.

**How to reproduce it (as minimally and precisely as possible)**:

https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-main-1-31/1873812786023239680

<img width="970" alt="Screenshot 2025-01-01 at 9 22 07" src="https://github.com/user-attachments/assets/efb11a58-f541-4393-ad75-2e59fdfb184e" />

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-01-01T00:22:59Z

/kind flake
