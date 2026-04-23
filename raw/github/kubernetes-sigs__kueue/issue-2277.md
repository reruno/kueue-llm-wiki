# Issue #2277: enabling manageJobsWithoutQueueName breaks OpenShift clusters

**Summary**: enabling manageJobsWithoutQueueName breaks OpenShift clusters

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2277

**Last updated**: 2024-06-25T20:32:37Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@dgrove-oss](https://github.com/dgrove-oss)
- **Created**: 2024-05-24T18:54:29Z
- **Updated**: 2024-06-25T20:32:37Z
- **Closed**: 2024-06-25T20:32:35Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 3

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
Deploying Kueue with `manageJobsWithoutQueueName` set to true on an OpenShift cluster broke core system functionality. 
In particular,  batchv1/Jobs that are used by OpenShift operators to perform administrative operations were suspended indefinitely resulting in degraded system functionality. 

See #2119 for discussion of some alternative solutions, such as namespace-level configuration of `manageJobsWithoutQueueName`, namespace-level configuration of the `batch/jobs` integration, and removal of the `manageJobsWithoutQueueName` functionality entirely. 

**What you expected to happen**:
In the short run, we should at least document that this configuration is ill-advised.  Ideally, we should dynamically flag it as a configuration error.

In the longer run, we should implement one of the alternatives discussed in #2119. 

**How to reproduce it (as minimally and precisely as possible)**:

Deploy Kueue with `manageJobsWithoutQueueName` true and the `batch/jobs` integration enabled.  Deploy an operator that uses Jobs (for example the Node Feature Discovery Operator) and observe that the operator does not work as intended.

**Anything else we need to know?**:

**Environment**:
An OpenShift 2.14 cluster with Kueue configured to enable `manageJobsWithoutQueueName`.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-24T19:57:06Z

Feel free to send a documentation PR warning about the use of the setting. But I'm still on the fence about adding more policy-like features in the Kueue.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-06-25T20:32:31Z

/close
with #2279

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-06-25T20:32:36Z

@alculquicondor: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/2277#issuecomment-2189917006):

>/close
>with #2279


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
