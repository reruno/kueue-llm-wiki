# Issue #2470: Race condition when setting MaxRetries on provisioning controller

**Summary**: Race condition when setting MaxRetries on provisioning controller

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2470

**Last updated**: 2024-06-25T21:32:39Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2024-06-21T20:17:19Z
- **Updated**: 2024-06-25T21:32:39Z
- **Closed**: 2024-06-25T21:32:39Z
- **Labels**: `kind/bug`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 2

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->

**What happened**:
A race condition occurs when setting MaxRetries on provisioning controller.

**What you expected to happen**:
No race condition

**How to reproduce it (as minimally and precisely as possible)**:
GINKGO_ARGS=--race make test-integration

**Anything else we need to know?**:
```
WARNING: DATA RACE
  Write at 0x000003df1458 by goroutine 2233:
    sigs.k8s.io/kueue/test/integration/controller/admissionchecks/provisioning.init.func1.4.2()
        /home/prow/go/src/sigs.k8s.io/kueue/test/integration/controller/admissionchecks/provisioning/provisioning_test.go:1003 +0x70
    github.com/onsi/ginkgo/v2/internal.extractBodyFunction.func3()
        /home/prow/go/pkg/mod/github.com/onsi/ginkgo/v2@v2.19.0/internal/node.go:472 +0x2e
    github.com/onsi/ginkgo/v2/internal.(*Suite).runNode.func3()
        /home/prow/go/pkg/mod/github.com/onsi/ginkgo/v2@v2.19.0/internal/suite.go:894 +0x12b
  Previous read at 0x000003df1458 by goroutine 535:
    sigs.k8s.io/kueue/pkg/controller/admissionchecks/provisioning.(*Controller).syncOwnedProvisionRequest()
        /home/prow/go/src/sigs.k8s.io/kueue/pkg/controller/admissionchecks/provisioning/controller.go:218 +0x7f6
    sigs.k8s.io/kueue/pkg/controller/admissionchecks/provisioning.(*Controller).Reconcile()
        /home/prow/go/src/sigs.k8s.io/kueue/pkg/controller/admissionchecks/provisioning/controller.go:143 +0x8ed
    sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).Reconcile()
        /home/prow/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.17.3/pkg/internal/controller/controller.go:119 +0x1a1
    sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).reconcileHandler()
        /home/prow/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.17.3/pkg/internal/controller/controller.go:316 +0x59a
    sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).processNextWorkItem()
        /home/prow/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.17.3/pkg/internal/controller/controller.go:266 +0x338
    sigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).Start.func2.2()
        /home/prow/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.17.3/pkg/internal/controller/controller.go:227 +0xb2
```

https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/2468/pull-kueue-test-integration-main/1804230951551635456

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-06-21T20:17:26Z

/cc @alculquicondor

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-06-24T05:11:03Z

/assign
