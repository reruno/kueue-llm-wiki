# Issue #6457: Move pod owner index from job_controller to core

**Summary**: Move pod owner index from job_controller to core

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6457

**Last updated**: 2025-08-05T07:41:40Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@ichekrygin](https://github.com/ichekrygin)
- **Created**: 2025-08-05T07:12:58Z
- **Updated**: 2025-08-05T07:41:40Z
- **Closed**: 2025-08-05T07:41:40Z
- **Labels**: `kind/cleanup`
- **Assignees**: _none_
- **Comments**: 0

## Description

<!-- Please only use this template for submitting cleanup requests -->

**What would you like to be cleaned**:

Move the "Pod Owner Index setup" from the specific job integration into `core/indexer`.

**Why is this needed**:

The pod owner index was originally added in `pkg/controller/jobs/job.SetupIndexes` as part of the `ElasticJobsViaWorkloadSlices` feature. However, multiple integrations may eventually need to leverage this index. Because it is currently defined within the job-specific integration, any additional integration that attempts to define the same index will result in an index collision.

So far this hasn’t been an issue, since `batch/v1.Job` is the only integration that supports ElasticJobs.
