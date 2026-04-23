# Issue #3471: Reduce number of API requests in the Provisioning Controller

**Summary**: Reduce number of API requests in the Provisioning Controller

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3471

**Last updated**: 2024-11-07T12:23:31Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@PBundyra](https://github.com/PBundyra)
- **Created**: 2024-11-06T09:57:02Z
- **Updated**: 2024-11-07T12:23:31Z
- **Closed**: 2024-11-07T12:23:31Z
- **Labels**: `kind/feature`, `kind/cleanup`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 3

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
Currently Provisioning controller does up to three GET requests on ProvisioningRequestConfig per one reconcile loop
1. https://github.com/kubernetes-sigs/kueue/blob/e5dd891432f61c4a418e69405c840110553c07b0/pkg/controller/admissionchecks/provisioning/controller.go#L173
2. https://github.com/kubernetes-sigs/kueue/blob/e5dd891432f61c4a418e69405c840110553c07b0/pkg/controller/admissionchecks/provisioning/controller.go#L209
3. https://github.com/kubernetes-sigs/kueue/blob/e5dd891432f61c4a418e69405c840110553c07b0/pkg/controller/admissionchecks/provisioning/controller.go#L488

This could be reduced by requesting ProvisioningRequestConfig once and then storing it in map[checkName]ProvReqConfig

**Why is this needed**:
To reduce number of requests sent, optimize performance of the ProvisioningController

**Completion requirements**:

## Discussion

### Comment by [@PBundyra](https://github.com/PBundyra) — 2024-11-06T10:02:55Z

/kind cleanup

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-06T10:12:52Z

cc @mbobrovskyi @vladikkuzn @mszadkow

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-11-06T15:57:46Z

/assign
