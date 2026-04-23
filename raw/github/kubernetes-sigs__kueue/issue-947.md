# Issue #947: Feature Request: Python Examples

**Summary**: Feature Request: Python Examples

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/947

**Last updated**: 2023-07-06T22:25:05Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@vsoch](https://github.com/vsoch)
- **Created**: 2023-07-05T07:54:34Z
- **Updated**: 2023-07-06T22:25:05Z
- **Closed**: 2023-07-06T22:25:05Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 5

## Description

**What would you like to be added**:

A handle to interact with Kueue from Python.

**Why is this needed**:

Kueue is a nice interface for multi-tenancy running of jobs (and CRDs that implement them) but for extending it easily to workflow tools, we would ideally be able to programmatically control it one level up, meaning the workflow tool with a DAG would generate and submit jobs in a logical way on behalf of the user.

**Completion requirements**:

I would say completion requirements should include:

- [ ] An automated generation of the Python SDK (with tests)
- [ ] Basic examples for usage

This enhancement requires the following artifacts:

I'm not sure about the below - likely we don't need a design doc if we use an automated tool, nor do we need an API change. Docs would make sense!

- [ ] Design doc
- [ ] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-07-05T07:58:44Z

@vsoch Does that mean that you would like to manage ClusterQueue, LocalQueue, ResourceFlavor, and Workload by workflows?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-07-05T08:04:06Z

I'm not sure of use cases in which batch-users want to operate ClusterQueue, LocalQueue, ResourceFlavor, and Workload by workflows.

### Comment by [@vsoch](https://github.com/vsoch) — 2023-07-05T12:09:55Z

Perhaps the need is even easier then - we just need examples of using the Kubernetes Python SDK to submit labeled jobs / MiniCluster, etc. that will be given to batch. Yes, I do think it would be nice to have a handle to the different queues / resource flavors (because this could be useful in the context of running workflows)  but it sounds like you do not agree.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-07-05T12:16:46Z

In general, end-users (the ones running workflows) shouldn't need to deal with the queues or quotas. So this mostly makes sense just for the job objects (Job, MPIJob, etc). For Job, you should be able to use the generic k8s python client. For other CRDs, you can still use the generic python client, but for more "native" support, I would expect you to use the python client from the respective CRD. I know MPIJob has one.

In any case, I agree that examples would be useful. I would welcome a PR to the documentation.

### Comment by [@vsoch](https://github.com/vsoch) — 2023-07-05T12:20:50Z

Yep I like that idea too - will get in some examples hopefully this week. Thanks to you both!
