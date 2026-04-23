# Issue #2414: Add a watch for Ray and Training Operator CRDs

**Summary**: Add a watch for Ray and Training Operator CRDs

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2414

**Last updated**: 2024-09-12T16:07:55Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@ChristianZaccaria](https://github.com/ChristianZaccaria)
- **Created**: 2024-06-14T15:04:26Z
- **Updated**: 2024-09-12T16:07:55Z
- **Closed**: 2024-09-12T16:07:53Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 16

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
When the Kueue component is installed before the Ray OR Training Operator, Kueue doesn't monitor RayCluster or PyTorchJob resources + any other [CRDs from the Training Operator.](https://github.com/kubeflow/training-operator/tree/master/manifests/base/crds)

When the user creates a RayCluster or PyTorchJob resources, Kueue doesn't control admission of those resources.

Logs:
>{"level":"info","ts":"2024-05-30T11:07:08.761740832Z","logger":"setup","caller":"jobframework/setup.go:69","msg":"No matching API in the server for job framework, skipped setup of controller and webhook","jobFrameworkName":"kubeflow.org/pytorchjob"}

**What you expected to happen**:
JobFramework Controller and Webhook should start/restart once required CRDs from Ray OR Training-Operator are available.

**How to reproduce it (as minimally and precisely as possible)**:
1. Deploy Kueue without the Ray or Training-Operator CRDs.
2. Check Kueue logs.

**Anything else we need to know?**:
Proposed Solution:
Add a watcher to controller and webhook, to start/restart in the event of availability of Ray OR Training-Operator CRDs.

I have a draft PR ready - still needs some work.

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@trasc](https://github.com/trasc) — 2024-06-17T10:56:30Z

Adding a watch just for this looks too much for me since having the CRDs installed before enabling an integration in the Kueue's config it's a reasonable expectation and even if it's not the case `rollout restart`-ing the Kueue's controller manager can easily solve the issue.

@alculquicondor WDYT?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-06-17T17:27:47Z

I also think that it's a reasonable expectation that the administrator needs to restart Kueue.

But I'm willing to accept a PR if it doesn't add significant complexity. It's probably going to be similar to the watch we have for k8s version.

### Comment by [@ChristianZaccaria](https://github.com/ChristianZaccaria) — 2024-06-19T09:39:41Z

@alculquicondor here is a draft PR we have on our fork: https://github.com/opendatahub-io/kueue/pull/33/files

Planning on changing it a bit to account for Training Operator OR Ray CRDs, then restart the JobFramework controller and webhook once CRDs are available. The approach in the PR separates concerns, providing a more readable and robust code. Please let me know if it looks good, and if should continue and make a PR. Thanks a lot for your help!

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-06-19T17:36:04Z

so overall you are adding a watch... Maybe it isn't too bad.

wdyt @trasc?

### Comment by [@trasc](https://github.com/trasc) — 2024-06-20T07:19:50Z

I guess it could work, but it should work for any CRD (maybe some kind of wrapper like https://github.com/kubernetes-sigs/kueue/blob/main/pkg/controller/core/leader_aware_reconciler.go).

Given the limited use-case and available alternatives, the work might outweigh the added benefits, however we can try it.

(controller-runtime might a better place to implement this kind of feature)

### Comment by [@ChristianZaccaria](https://github.com/ChristianZaccaria) — 2024-07-09T11:47:44Z

Hi folks, before making a PR to resolve this issue, we would like to get some feedback on which option would suit best. We have 3-4 proposals in place.

Here are the 3 proposals:
- https://github.com/ChristianZaccaria/kueue/pull/3 (Watcher using Dynamic Client - Restarting Kueue pod)
- https://github.com/ChristianZaccaria/kueue/pull/4 (RESTMapper - Restarting Kueue pod)
- https://github.com/ChristianZaccaria/kueue/pull/5 (RESTMapper - Starting controller/webhook of the respective framework on availability of the CRD - No restarts on Kueue pod)
- A 4th idea is to use the apiextension clientset which queries for CRDs directly. 

Preference may be on the RESTMapper as it's the [current way Kueue is verifying](https://github.com/kubernetes-sigs/kueue/blob/main/pkg/controller/jobframework/setup.go#L70) if the APIs exist. - Minimal changes.

Thank you! @alculquicondor @trasc

### Comment by [@trasc](https://github.com/trasc) — 2024-07-10T06:28:20Z

If it works as expected, for me I think the 3rd option is the cleanest. 

The problem with the first one is that in my opinion we cannot assume that the plural of a kind is the lexical plural of that kind in lowercase,

### Comment by [@ChristianZaccaria](https://github.com/ChristianZaccaria) — 2024-07-10T08:20:53Z

@trasc the 3rd option is definitely the cleanest. I'll wait a few for @alculquicondor's opinion on this and will make a PR for further reviewing.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-07-10T14:14:56Z

sgtm

### Comment by [@mimowo](https://github.com/mimowo) — 2024-07-24T13:15:27Z

As part of fixing this issue please update the documentation to amend or revert: https://github.com/kubernetes-sigs/kueue/pull/2685.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-04T16:37:45Z

/reopen
To update the documentation accordingly, or cherry-pick https://github.com/kubernetes-sigs/kueue/pull/2574

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-09-04T16:37:50Z

@mimowo: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/2414#issuecomment-2329529782):

>/reopen
>To update the documentation accordingly, or cherry-pick https://github.com/kubernetes-sigs/kueue/pull/2574


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@ChristianZaccaria](https://github.com/ChristianZaccaria) — 2024-09-04T17:19:07Z

Hi @mimowo it looks like we'll be updating the documentation if this is considered as feature rather as a bug fix. Would like to have confirmation on this. Let me know if the consensus is to update the docs and I'll create a PR promptly. Thanks a lot!

https://github.com/kubernetes-sigs/kueue/pull/2685#issuecomment-2326102778

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-04T17:26:59Z

I would suggest to reconsider this decision, as the fix does not introduce any API changes, and from the end user perspective this is a bug - at least this is the impression I was getting when investigating some of the users' issues. 

I posted also under the PR https://github.com/kubernetes-sigs/kueue/pull/2574.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-12T16:07:48Z

/close
As the documentation update is already queued to merge. The remaining work is already ticketed.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-09-12T16:07:53Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/2414#issuecomment-2346702671):

>/close
>As the documentation update is already queued to merge. The remaining work is already ticketed.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
