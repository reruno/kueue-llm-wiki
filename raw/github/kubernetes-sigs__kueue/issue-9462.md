# Issue #9462: PreemptionOverBorrowing FlavorFungibility leading to undesirable scheduling behavior

**Summary**: PreemptionOverBorrowing FlavorFungibility leading to undesirable scheduling behavior

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9462

**Last updated**: 2026-02-26T08:59:57Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@varunsyal](https://github.com/varunsyal)
- **Created**: 2026-02-24T21:50:10Z
- **Updated**: 2026-02-26T08:59:57Z
- **Closed**: 2026-02-26T08:59:56Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 4

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
While moving from v0.15 to v0.16, we are trying to remove the feature gate "FlavorFungibilityImplicitPreferenceDefault" that we have been using but no longer supported since v0.16. In order to enable the same functionality without the feature flag, we have set the FlavorFungibility as the following on the Clusterqueues:
```
Flavor Fungibility:
    Preference:        PreemptionOverBorrowing
    When Can Borrow:   TryNextFlavor
    When Can Preempt:  TryNextFlavor
```
We observe that the preemption over borrowing functionality across 2 flavors is not working as expected.
In the example we run:

We have 3 Clusterqueues under the same Cohort

CQ-1:
   > FairSharing Weight = 1
    Flavor 1: Nominal Quota = 1cpu, Borrowing Limit = 4cpu
    Flavor 2: Nominal Quota = 0, Borrowing Limit = 4cpu

CQ-2:
>    FairSharing Weight = 1
    Flavor 1: Nominal Quota = 1, Borrowing Limit = 4cpu
    Flavor 2: Nominal Quota = 0, Borrowing Limit = 4cpu

CQ-3:
>    FairSharing Weight = 1
    Flavor 1: Nominal Quota = 0, Borrowing Limit = 4cpu
    Flavor 2: Nominal Quota = 2, Borrowing Limit = 4cpu

Now we submit 2 workloads requesting 1 cpu each to CQ-1
> Result: Both workloads go to Flavor-1

Next, we submit 2 workloads requesting 1 cpu each to CQ-2
>    Result: Both workloads go to Flavor-2 ---> This is not expected, since CQ-2 has nominal quota in Flavor-1, so before borrowing in Flavor-2, it should preempt in Flavor-1
    Expectation is: Both CQ-1 and CQ-2 eventually have 1 workload running in each of its flavor.

Adding YAML test files:
[Test-setup-scenario-multiflavor-fungibility.zip](https://github.com/user-attachments/files/25531385/Test-setup-scenario-multiflavor-fungibility.zip)

**Anything else we need to know?**:

**Environment**: 
- Kubernetes version (use `kubectl version`): v1.32.11
- Kueue version (use `git describe --tags --dirty --always`): v0.15.3
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-02-25T03:12:15Z

@varunsyal Thank you for reporting that.

@gabesaba @mimowo I'm suspecting this is a bug on https://github.com/kubernetes-sigs/kueue/blob/04bec226c57290c0a34ec582232637b4b5bd8c56/pkg/scheduler/flavorassigner/flavorassigner.go#L412-L419.

The `isPreferred` function has an incorrect switching enum and an actionable function.
I guess that the correct approach is the following:

```go
	if fungibilityConfig.Preference != nil {
		switch *fungibilityConfig.Preference {
		case kueue.BorrowingOverPreemption:
			return borrowingOverPreemption()
		case kueue.PreemptionOverBorrowing:
			return preemptionOverBorrowing()
		}
	}
```

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-25T06:06:22Z

Good spot, looks like a good candidate fox fixing place.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-02-26T08:59:51Z

I'm closing this as we fixed. @varunsyal Please let us know when you face other bugs, thanks!

Fixed by #9464

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-02-26T08:59:57Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/9462#issuecomment-3965124611):

>I'm closing this as we fixed. @varunsyal Please let us know when you face other bugs, thanks!
>
>Fixed by #9464
>
>/close
>
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
