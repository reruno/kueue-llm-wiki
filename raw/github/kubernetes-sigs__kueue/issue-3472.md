# Issue #3472: Add wrapper for ProvisioningRequestConfig to `util/testing` package

**Summary**: Add wrapper for ProvisioningRequestConfig to `util/testing` package

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3472

**Last updated**: 2024-12-02T09:37:01Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@PBundyra](https://github.com/PBundyra)
- **Created**: 2024-11-06T10:01:19Z
- **Updated**: 2024-12-02T09:37:01Z
- **Closed**: 2024-12-02T09:37:01Z
- **Labels**: `kind/feature`, `kind/cleanup`
- **Assignees**: [@TusharMohapatra07](https://github.com/TusharMohapatra07)
- **Comments**: 5

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
Wrapper for ProvisioningRequestConfig similarly to e.g. [PriorityClassWrapper](https://github.com/kubernetes-sigs/kueue/blob/main/pkg/util/testing/wrappers.go#L38-L61). Besides fundamental methods to create wrapper and actual object we also need methods to set:
- `.spec.provisioningClassName`
- `.spec.parameters`
- `.spec.managedResources`
- `.spec.retryStrategy`
- `.spec.retryStrategy.backoffLimitCount`
- `.spec.retryStrategy.backoffBaseSeconds`
- `.spec.retryStrategy.backoffMaxSeconds`

Wrapper should be used in all test files where `ProvisioningRequestConfig` is used, including:
- `pkg/controller/admissionchecks/provisioning/admissioncheck_reconciler_test.go`
- `pkg/controller/admissionchecks/provisioning/controller_test.go`
- `pkg/util/admissioncheck/admissioncheck_test.go`
- `test/integration/controller/admissionchecks/provisioning/provisioning_test.go`

**Why is this needed**:
Improve code quality

**Completion requirements**:

## Discussion

### Comment by [@PBundyra](https://github.com/PBundyra) — 2024-11-06T10:02:35Z

/kind cleanup

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-06T10:12:48Z

cc @mbobrovskyi @vladikkuzn @mszadkow

### Comment by [@TusharMohapatra07](https://github.com/TusharMohapatra07) — 2024-11-06T15:34:12Z

Can i work on this issue ?

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-06T15:39:01Z

Sure, please use '/assign' in that case

### Comment by [@TusharMohapatra07](https://github.com/TusharMohapatra07) — 2024-11-06T15:39:47Z

/assign
