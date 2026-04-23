# Issue #4377: Allow one to use cert manager to secure prometheus endpoints

**Summary**: Allow one to use cert manager to secure prometheus endpoints

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4377

**Last updated**: 2025-03-13T17:19:51Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kannon92](https://github.com/kannon92)
- **Created**: 2025-02-24T14:21:02Z
- **Updated**: 2025-03-13T17:19:51Z
- **Closed**: 2025-03-13T17:19:51Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 1

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
We would like to use cert manager with our metrics endpoint.

**Why is this needed**:
Metrics are only secure by using https and requiring the service account access. 

We want to make sure that our metrics endpoint has tls options as this is a recommended approach for our organization.

**Plan**:

https://book.kubebuilder.io/reference/metrics#recommended-enabling-certificates-for-production-disabled-by-default

We will need to add more options to the metrics config api object to reference the certicates for metrics server configs.

See [here](https://github.com/kubernetes-sigs/kubebuilder/blob/master/testdata/project-v4/cmd/main.go#L84)

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2025-02-26T00:20:58Z

@mimowo and @tenzen-y suggested I draft a KEP for this so we can clear up the supported options.

Opened https://github.com/kubernetes-sigs/kueue/pull/4404
