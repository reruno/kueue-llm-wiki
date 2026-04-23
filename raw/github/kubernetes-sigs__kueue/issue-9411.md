# Issue #9411: Elastic JobSet support

**Summary**: Elastic JobSet support

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9411

**Last updated**: 2026-02-24T20:32:41Z

---

## Metadata

- **State**: open
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-02-23T08:14:37Z
- **Updated**: 2026-02-24T20:32:41Z
- **Closed**: —
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 4

## Description

**What would you like to be added**:

Support for Elastic JobSet using the https://github.com/kubernetes-sigs/kueue/issues/77 mechanism

**Why is this needed**:

To support Elastic JobSet, currently being worked on in the main controller: https://github.com/kubernetes-sigs/jobset/issues/463, see [KEP](https://github.com/kubernetes-sigs/jobset/pull/1147)

**Completion requirements**

As soon as the support is available in JobSet (might be prior to release of JobSet) we can start testing the Elastic Jobs. 

For the regular Elastic JobSet the framework we already have should be generic enough to handle them without code changes (or minimal). See how we added support for RayCluster: https://github.com/kubernetes-sigs/kueue/pull/6662/changes. 

However the TAS support may need a bit more work / testing in case of index conflicts. It seems those will be unavoidable so we need some recovery mechanisms.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-23T08:16:16Z

cc @kannon92 @sohankunkerkar

### Comment by [@aniket2405](https://github.com/aniket2405) — 2026-02-23T09:56:49Z

Thanks for raising this, @mimowo 
I'd be happy to help with this as well along with the open Elastic JobSet support.

### Comment by [@andreyvelich](https://github.com/andreyvelich) — 2026-02-24T20:18:33Z

Thank you for creating this @mimowo!
Do we need separate issue/changes in Kueue to support Elastic TrainJobs?

Once we introduce mutability for JobSet scaling fields, we plan to extend this functionality to TrainJob to ensure compatibility with [Elastic PyTorchJob](https://docs.pytorch.org/docs/stable/distributed.elastic.html) in Training Operator v1: https://github.com/kubeflow/trainer/issues/2903.
Also, potentially support of [Elastic Horovod](https://horovod.readthedocs.io/en/latest/elastic_include.html) via MPI-based Trainer Runtimes.

Given this, would we also need updates in Kueue’s TrainJob controller to properly handle these changes?

cc @kaisoz

### Comment by [@kannon92](https://github.com/kannon92) — 2026-02-24T20:32:41Z

I think we would need work for TrainJob also.

https://github.com/kubernetes-sigs/kueue/tree/main/keps/77-dynamically-sized-jobs#design-details

This is the KEP that is starting to allow Kueue to support dynamic jobs.
