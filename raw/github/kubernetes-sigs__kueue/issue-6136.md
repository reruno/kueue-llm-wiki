# Issue #6136: Implement integraton tests for ManagedJobsNamespaceSelectorAlwaysRespected

**Summary**: Implement integraton tests for ManagedJobsNamespaceSelectorAlwaysRespected

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6136

**Last updated**: 2025-10-09T07:39:02Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-07-22T13:22:42Z
- **Updated**: 2025-10-09T07:39:02Z
- **Closed**: 2025-10-09T07:39:02Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@Singularity23x0](https://github.com/Singularity23x0)
- **Comments**: 2

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

Implementing integration tests for ManagedJobsNamespaceSelectorAlwaysRespected in test/integration/singlecluster/jobs/job/job_controller_test.go.

**Why is this needed**:

As we mentioned in https://github.com/kubernetes-sigs/kueue/pull/5638#discussion_r2216302030, we did not implement integration tests for ManagedJobsNamespaceSelectorAlwaysRespected. Both integration and E2E level still work well.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-07-22T13:22:54Z

@PannagaRao @mimowo

### Comment by [@Singularity23x0](https://github.com/Singularity23x0) — 2025-09-08T10:42:31Z

/assign
