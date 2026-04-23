# Issue #3351: Flaky Test: Multikueue Should requeue the workload with a delay when the connection to the admitting worker is lost

**Summary**: Flaky Test: Multikueue Should requeue the workload with a delay when the connection to the admitting worker is lost

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3351

**Last updated**: 2024-10-29T12:26:56Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2024-10-28T20:33:53Z
- **Updated**: 2024-10-29T12:26:56Z
- **Closed**: 2024-10-29T12:26:56Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 6

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

Flaky test for "Multikueue Suite: [It] Multikueue Should requeue the workload with a delay when the connection to the admitting worker is lost [slow] expand_more"

```shell
{Timed out after 45.000s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/integration/multikueue/multikueue_test.go:1399 with:
Expected object to be comparable, diff:   &v1beta1.AdmissionCheckState{
  	Name:  "ac1",
- 	State: "Retry",
+ 	State: "Pending",
  	... // 2 ignored and 1 identical fields
  }
 failed [FAILED] Timed out after 45.000s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/integration/multikueue/multikueue_test.go:1399 with:
Expected object to be comparable, diff:   &v1beta1.AdmissionCheckState{
  	Name:  "ac1",
- 	State: "Retry",
+ 	State: "Pending",
  	... // 2 ignored and 1 identical fields
  }
In [It] at: /home/prow/go/src/kubernetes-sigs/kueue/test/integration/multikueue/multikueue_test.go:1408 @ 10/28/24 18:18:21.347
}
```

**What you expected to happen**:

No errors happen.

**How to reproduce it (as minimally and precisely as possible)**:

https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-integration-main/1850961678087229440

<img width="1203" alt="Screenshot 2024-10-29 at 5 33 03" src="https://github.com/user-attachments/assets/2481a560-1c82-4ce2-9e24-c8a59171749d">

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-10-28T20:34:01Z

/kind flake

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-10-28T20:36:08Z

I guess that this flaky testing brought by https://github.com/kubernetes-sigs/kueue/pull/3323

cc: @PBundyra

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-29T07:25:15Z

Ok, so I haven't done any testing, but I looked at the code and it seems with https://github.com/kubernetes-sigs/kueue/pull/3323 we essentially replace what MultiKueue controller was doing in this flow:
1. setting Retry if the connection was lost (as in the test) (see [here](https://github.com/kubernetes-sigs/kueue/blob/90ef60760b849e475f7cf32d07669bb91bbb479f/pkg/controller/admissionchecks/multikueue/workload.go#L396-L401))
2. when the QuotaReservation was lost "resetting" back to Pending [here](https://github.com/kubernetes-sigs/kueue/blob/90ef60760b849e475f7cf32d07669bb91bbb479f/pkg/controller/admissionchecks/multikueue/workload.go#L306)

Now, to make this possible the MK controller was taking ownership of the fields [here](https://github.com/kubernetes-sigs/kueue/blob/90ef60760b849e475f7cf32d07669bb91bbb479f/pkg/controller/admissionchecks/multikueue/workload.go#L334C150-L334C164). Now, because core controller does not own the fields it is not able to evict the Workload, and remove the QuotaReservation, and so MK controller is not able to switch to Pending, nor the core controller.

Since now (after  https://github.com/kubernetes-sigs/kueue/pull/3323) core kueue controller needs to also update the fields we need to take the ownership back. We only need to do it when `ResetChecksOnEviction` makes any change, but I'm ok to make this unconditional for simplicity. 

Still, I might be missing something, this wasn't tested.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-29T09:34:51Z

IIUC this is not really a flaky test - it would fail deterministically, but it is disabled on presubmits

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-10-29T10:43:06Z

> IIUC this is not really a flaky test - it would fail deterministically, but it is disabled on presubmits

Yeah, the reason is this is marked as slow.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-29T12:21:15Z

@PBundyra please open a follow up issue to remember to cleanup https://github.com/kubernetes-sigs/kueue/blob/90ef60760b849e475f7cf32d07669bb91bbb479f/pkg/controller/admissionchecks/multikueue/workload.go#L305-L307. I think this is no longer needed based on the investigation / summary in https://github.com/kubernetes-sigs/kueue/issues/3351#issuecomment-2443442695.
