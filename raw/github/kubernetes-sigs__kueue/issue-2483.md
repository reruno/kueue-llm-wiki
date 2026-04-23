# Issue #2483: Flaky integration test for provisioning AdmissionCheck

**Summary**: Flaky integration test for provisioning AdmissionCheck

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2483

**Last updated**: 2024-06-27T15:57:18Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2024-06-26T18:10:22Z
- **Updated**: 2024-06-27T15:57:18Z
- **Closed**: 2024-06-27T15:57:18Z
- **Labels**: `kind/bug`
- **Assignees**: [@PBundyra](https://github.com/PBundyra)
- **Comments**: 2

## Description

**What happened**:

Test: `Provisioning when A workload is using a provision admission check Should not set AdmissionCheck status to Rejected, deactivate Workload, emit an event, and bump metrics when workloads is not Finished, and the ProvisioningRequest's condition is set to CapacityRevoked`

```
{Timed out after 5.000s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/integration/controller/admissionchecks/provisioning/provisioning_test.go:663 with:
Expected
    <v1beta1.CheckState>: Pending
to equal
    <v1beta1.CheckState>: Ready failed [FAILED] Timed out after 5.000s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/integration/controller/admissionchecks/provisioning/provisioning_test.go:663 with:
Expected
    <v1beta1.CheckState>: Pending
to equal
    <v1beta1.CheckState>: Ready
In [It] at: /home/prow/go/src/kubernetes-sigs/kueue/test/integration/controller/admissionchecks/provisioning/provisioning_test.go:669 @ 06/26/24 17:35:44.329
}
```

**What you expected to happen**:

No flakiness

**How to reproduce it (as minimally and precisely as possible)**:

https://prow.k8s.io/view/gs/kubernetes-jenkins/logs/periodic-kueue-test-integration-main/1806017708857233408

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

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-06-26T18:10:29Z

/assign @trasc

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-06-26T18:11:15Z

actually
/unassign trasc
/assign @PBundyra
