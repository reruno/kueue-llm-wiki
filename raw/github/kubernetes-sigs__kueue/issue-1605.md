# Issue #1605: Flaky: Provisioning when A workload is using a provision admission check Should let a running workload to continue after the provisioning request deleted

**Summary**: Flaky: Provisioning when A workload is using a provision admission check Should let a running workload to continue after the provisioning request deleted

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1605

**Last updated**: 2024-01-19T15:26:14Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2024-01-17T19:32:11Z
- **Updated**: 2024-01-19T15:26:14Z
- **Closed**: 2024-01-19T15:26:14Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mimowo](https://github.com/mimowo)
- **Comments**: 7

## Description

**What happened**:

/kind flake

The provisioning request object was never deleted. Perhaps due to a finalizer?

```
{Timed out after 30.000s.
Expected
    <nil>: nil
to be a NotFound error failed [FAILED] Timed out after 30.000s.
Expected
    <nil>: nil
to be a NotFound error
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/integration/controller/admissionchecks/provisioning/provisioning_test.go:635 @ 01/17/24 19:24:43.397
}
```

**What you expected to happen**:

The provisioning request object to be deleted.

**How to reproduce it (as minimally and precisely as possible)**:

https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/1604/pull-kueue-test-integration-main/1747700693520617472

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

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-01-17T19:32:19Z

/assign @mimowo

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-01-17T19:34:22Z

Or could it be that the retry logic is creating a new ProvReq with the same name?

### Comment by [@mimowo](https://github.com/mimowo) — 2024-01-18T10:46:03Z

ack

> Or could it be that the retry logic is creating a new ProvReq with the same name?

yes, it gets recreated, but not sure why, because logic of recreation should be gourded by the `IsAdmitted` [check](https://github.com/kubernetes-sigs/kueue/blob/d4d3f3be091eea414ae8d7018108ff9a391dc14d/pkg/controller/admissionchecks/provisioning/controller.go#L138), and the code test checks that it is Admitted. Unless, there is some reconciliation started before it was admitted. Not sure ATM how to protect against it.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-01-18T13:51:38Z

I have reproduced this locally with extra logs, and what happens:
1. the test code awaits for the workload to have the Admitted condition
2. the test code deleted the ProvReq
3. the deleted ProvReq triggers reconciliation, but the workload retrieved from the client still does not have the condition, so we recreate the ProvReq

So indeed, there is a race condition exposed by the test, but only affects newly admitted workloads. I think the same would happen prior to the ProvReq retry mechanism. In the analogous way we would attempt to recreate the manually deleted ProvReq.

Now, I\m not sure what is the best way to resolve this. One idea is to inject 1s wait before deleting the ProvReq to make it almost for certain that the client returns new value.  Another idea could be to modify controller.go to OR IsAdmitted with HasQuotaReservation && relevant checks ready, in anticipation of the Admitted condition being added soon.

Sounds fishy, but no better idea so far. Any better ideas @alculquicondor ?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-01-18T16:54:39Z

What about changing the controller to not create a new ProvReq if the Workload object already has the AdmissionCheck as Ready?

### Comment by [@mimowo](https://github.com/mimowo) — 2024-01-18T17:27:46Z

> What about changing the controller to not create a new ProvReq if the Workload object already has the AdmissionCheck as Ready?

I think this should work, I will try. Maybe the only drawback is that this would be repeating logic of the workload_controller, but we can probably commonize is sufficiently, I will see.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-01-18T17:58:17Z

I don't mean all admission checks, just the check that corresponds to the ProvReq.
