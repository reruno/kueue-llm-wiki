# Issue #5575: [Fleky Integration Test] Provisioning when Workload uses a provision admission check with BackoffLimitCount=1 Should retry if a ProvisioningRequest fails, then reject AdmissionCheck if the second ProvisioningRequest fails

**Summary**: [Fleky Integration Test] Provisioning when Workload uses a provision admission check with BackoffLimitCount=1 Should retry if a ProvisioningRequest fails, then reject AdmissionCheck if the second ProvisioningRequest fails

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5575

**Last updated**: 2025-06-09T11:54:45Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2025-06-09T11:54:06Z
- **Updated**: 2025-06-09T11:54:45Z
- **Closed**: 2025-06-09T11:54:42Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 2

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->

/kind flake


**What happened**:

Provisioning admission check suite: [It] Provisioning when Workload uses a provision admission check with BackoffLimitCount=1 Should retry if a ProvisioningRequest fails, then reject AdmissionCheck if the second ProvisioningRequest fails

```
{Timed out after 10.007s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/integration/singlecluster/controller/admissionchecks/provisioning/provisioning_test.go:1735 with:
Expected
    <v1beta1.CheckState>: Retry
to equal
    <v1beta1.CheckState>: Pending failed [FAILED] Timed out after 10.007s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/integration/singlecluster/controller/admissionchecks/provisioning/provisioning_test.go:1735 with:
Expected
    <v1beta1.CheckState>: Retry
to equal
    <v1beta1.CheckState>: Pending
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/integration/singlecluster/controller/admissionchecks/provisioning/provisioning_test.go:1739 @ 06/09/25 11:49:00.349
}
```

**What you expected to happen**:
No errors

**How to reproduce it (as minimally and precisely as possible)**:
https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/5572/pull-kueue-test-integration-baseline-release-0-11/1932040894110765056

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

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-06-09T11:54:38Z

/close 

Duplicate of https://github.com/kubernetes-sigs/kueue/issues/5573.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-06-09T11:54:43Z

@mbobrovskyi: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/5575#issuecomment-2955573388):

>/close 
>
>Duplicate of https://github.com/kubernetes-sigs/kueue/issues/5573.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
