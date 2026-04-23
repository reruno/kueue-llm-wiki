# Issue #7637: [Flaky] End To End Custom Configs: conversion webhook for kueue.x-k8s.io/v1beta1 failed

**Summary**: [Flaky] End To End Custom Configs: conversion webhook for kueue.x-k8s.io/v1beta1 failed

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7637

**Last updated**: 2025-11-14T18:23:39Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2025-11-13T12:06:41Z
- **Updated**: 2025-11-14T18:23:39Z
- **Closed**: 2025-11-14T18:23:39Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 1

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

```
{Expected success, but got an error:
    <*errors.StatusError | 0xc0001770e0>: 
    conversion webhook for kueue.x-k8s.io/v1beta1, Kind=LocalQueue failed: Post "https://kueue-webhook-service.kueue-system.svc:443/convert?timeout=30s": EOF
    {
        ErrStatus: {
            TypeMeta: {Kind: "", APIVersion: ""},
            ListMeta: {
                SelfLink: "",
                ResourceVersion: "",
                Continue: "",
                RemainingItemCount: nil,
            },
            Status: "Failure",
            Message: "conversion webhook for kueue.x-k8s.io/v1beta1, Kind=LocalQueue failed: Post \"https://kueue-webhook-service.kueue-system.svc:443/convert?timeout=30s\": EOF",
            Reason: "",
            Details: nil,
            Code: 500,
        },
    } failed [FAILED] Expected success, but got an error:
    <*errors.StatusError | 0xc0001770e0>: 
    conversion webhook for kueue.x-k8s.io/v1beta1, Kind=LocalQueue failed: Post "https://kueue-webhook-service.kueue-system.svc:443/convert?timeout=30s": EOF
    {
        ErrStatus: {
            TypeMeta: {Kind: "", APIVersion: ""},
            ListMeta: {
                SelfLink: "",
                ResourceVersion: "",
                Continue: "",
                RemainingItemCount: nil,
            },
            Status: "Failure",
            Message: "conversion webhook for kueue.x-k8s.io/v1beta1, Kind=LocalQueue failed: Post \"https://kueue-webhook-service.kueue-system.svc:443/convert?timeout=30s\": EOF",
            Reason: "",
            Details: nil,
            Code: 500,
        },
    }
In [AfterEach] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/customconfigs/managejobswithoutqueuename_test.go:85 @ 11/13/25 11:45:43.614
}
```

**What you expected to happen**:
No issue

**How to reproduce it (as minimally and precisely as possible)**:
https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/7636/pull-kueue-test-e2e-customconfigs-main/1988932518660804608

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

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-11-13T12:06:48Z

/kind flake
