# Issue #1410: Add a troubleshooting page

**Summary**: Add a troubleshooting page

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1410

**Last updated**: 2024-11-06T18:18:40Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2023-12-05T19:34:11Z
- **Updated**: 2024-11-06T18:18:40Z
- **Closed**: 2024-11-06T18:18:38Z
- **Labels**: `lifecycle/stale`, `kind/documentation`
- **Assignees**: [@PBundyra](https://github.com/PBundyra)
- **Comments**: 16

## Description

**What would you like to be added**:

We can start documenting common user errors. For example:

- Workload is not admitted
  - Check CQ status, verify flavors
- Job starts but doesn't have any node selectors
  - Check whether the template has any requests, otherwise they won't get assigned a flavor. Or use quota per pod.

**Why is this needed**:

I think one of this scenarios was reported in #1407.

/kind documentation

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-12-05T19:34:41Z

@tenzen-y @kerthcet have you seen any common user errors?

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-12-06T07:06:29Z

If `Workload is not admitted`, check the workload status. 

Also sometimes, I need to check the feature gates like kubernetes does `kubectl get --raw /metrics | grep kubernetes_feature_enabled`, maybe we should do the same in kueue. This is not an error.

The integrated component's version is also something we should consider, I used to meet our users complaining about kueue not working with kubeflow, he already installed kubeflow1.7, however, the training-operator is 1.6, but we need 1.7 specifically. Maybe we can take this as a special case.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-12-06T13:46:34Z

Q1. The desired flavor isn't assigned to the Job.
A2. The flavor in clusterQueue is evaluated from top to bottom and assigned to jobs. The highest-priority flavor need to be put on the top.

Q2. In spite of a job being admitted, pods from a job are pending.
A2. Kueue will consider only quotas defined in clusterQueues, not consider actual cluster usage. Please check if the cluster has free capacity.

Q3. In spite of enabled sequential admission, all pods can not be started, and the part of pods are started.
A3. Kueue isn't pod's scheduler. Kueue doesn't guarantee that all pods are started at the same time.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-12-06T14:18:43Z

/remove-kind feature

### Comment by [@PBundyra](https://github.com/PBundyra) — 2024-02-07T16:05:50Z

/assign

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-02-08T18:51:15Z

A state diagram of Workload conditions would be useful. Annecdotically, I just got a question from a developer about what is QuotaReserved.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-02-09T21:30:42Z

Another common user error: installing the integration (for example jobset or kuberay) after installing kueue. 
Kueue will not monitor these jobs.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-05-09T22:22:29Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle stale`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-10T13:00:17Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-08-08T13:19:46Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle stale`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-08-08T15:46:09Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-11-06T15:51:59Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle stale`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-06T16:40:27Z

What is missing here before we can close? We have the base version of the guide. I believe we can improve it in follow up issues focused on specific features. WDYT @tenzen-y ?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-11-06T18:18:28Z

> What is missing here before we can close? We have the base version of the guide. I believe we can improve it in follow up issues focused on specific features. WDYT @tenzen-y ?

I'm ok with closing of this. During this year, we evolved the troubleshooting guide, so let's re-organize what is missing separately.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-11-06T18:18:33Z

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-11-06T18:18:38Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1410#issuecomment-2460472185):

>/close
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
