# Issue #7903: [Flake E2E Test] Pod groups when Single CQ should admit group that fits

**Summary**: [Flake E2E Test] Pod groups when Single CQ should admit group that fits

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7903

**Last updated**: 2025-11-27T06:46:22Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2025-11-26T10:37:38Z
- **Updated**: 2025-11-27T06:46:22Z
- **Closed**: 2025-11-27T06:46:21Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@sohankunkerkar](https://github.com/sohankunkerkar)
- **Comments**: 1

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

End To End Suite: kindest/node:v1.34.0: [It] Pod groups when Single CQ should admit group that fits 

```
{Timed out after 10.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/pod_test.go:103 with:
Expected
    <[]v1.PodSchedulingGate | len:2, cap:2>: [
        {
            Name: "kueue.x-k8s.io/admission",
        },
        {
            Name: "kueue.x-k8s.io/topology",
        },
    ]
to be empty failed [FAILED] Timed out after 10.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/pod_test.go:103 with:
Expected
    <[]v1.PodSchedulingGate | len:2, cap:2>: [
        {
            Name: "kueue.x-k8s.io/admission",
        },
        {
            Name: "kueue.x-k8s.io/topology",
        },
    ]
to be empty
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/pod_test.go:108 @ 11/26/25 10:02:25.853
}
```

**What you expected to happen**:
No errors

**How to reproduce it (as minimally and precisely as possible)**:
https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/7900/pull-kueue-test-e2e-main-1-34/1993616322499448832

**Anything else we need to know?**:

/kind flake

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2025-11-26T14:05:35Z

/assign @sohankunkerkar
