# Issue #3767: Add higher-level of testing for "queue-name" handling in pod-based workloads

**Summary**: Add higher-level of testing for "queue-name" handling in pod-based workloads

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3767

**Last updated**: 2025-02-28T16:10:57Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-12-09T08:12:21Z
- **Updated**: 2025-02-28T16:10:57Z
- **Closed**: 2025-02-28T16:10:57Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@kaisoz](https://github.com/kaisoz)
- **Comments**: 8

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

Add integration-level testing for pod-based integrations (Pod themselves, STS, Deployment). 
In particular cover scenarios related to the recent changes around [namespace filtering](https://github.com/kubernetes-sigs/kueue/issues/3589) and [LQ defautling](https://github.com/kubernetes-sigs/kueue/issues/2936).

We may also consider adding a suite for e2e tests with `manageJobsWithoutQueueName: true`.

**Why is this needed**:

The logic around "queue-name" handling is getting complex, but the tests for Jobs aren't enough, because the handling is mostly separate for pod-based serving workloads.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-09T08:12:41Z

cc @mbobrovskyi @dgrove-oss @yaroslava-serdiuk @tenzen-y

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-12T06:39:26Z

Actually, I think with https://github.com/kubernetes-sigs/kueue/issues/3804 it should be relatively simple to start a new e2e suite within the same CI job with that configuration. So, I would suggest starting with that. The Pod-based integration is easier to test e2e than integration, because pods are actually created by kube-controller-manager's controllers (Deployment or StatefulSets). cc @dgrove-oss @tenzen-y @mbobrovskyi .

We could start with the e2e tests for the "sanity" checking and add more integration tests for corner cases.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-12-12T07:10:40Z

/assign

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-12-17T14:32:41Z

/unassign

Sorry, I don't have capacity to work on it for now.

### Comment by [@kaisoz](https://github.com/kaisoz) — 2025-01-13T06:18:55Z

/assign

I'll take this one since is a requirement to tackle #3829

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-10T14:20:46Z

/reopen
For the  follow ups: https://github.com/kubernetes-sigs/kueue/pull/4112#pullrequestreview-2605827962

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-02-10T14:20:52Z

@mimowo: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3767#issuecomment-2648140157):

>/reopen
>For the  follow ups: https://github.com/kubernetes-sigs/kueue/pull/4112#pullrequestreview-2605827962


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-14T14:43:21Z

I think with the ground work of https://github.com/kubernetes-sigs/kueue/pull/4112 we are ready to add some tests coverage which is crucial for correctness of this configuration with the pod-based frameworks.

I'm thinking about covering the following scenarios:
1. create Pod/Deployment/StatefulSet without queue-name in test namespace and verify it is suspended, then delete the API objects and verify the child pods are removed  too
2. create a Pod/Deployment/StatefulSet without queue-name in kube-system and verify they run, then delete the API objects and verify the child pods are removed too

I believe there are numerous nuances between the integrations which are very hard to test with integration test because they rely on pod creation and integration with kube-controller-manager (especially for StatefulSet). 

The scenarios above will require enabling the integrations in the Kueue configuration. IIUC we could just add more "Its" for them [here](https://github.com/kubernetes-sigs/kueue/blob/6ff4efc7047c8a345da4cc558aba5752e3b3f2bd/test/e2e/customconfigs/skipjobswithoutqueuename_test.go#L87).

My preference is to split the work into small PRs so that we can react and change plans as we continue the work.

cc @dgrove-oss @tenzen-y
