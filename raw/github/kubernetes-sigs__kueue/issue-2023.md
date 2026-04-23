# Issue #2023: [MultiKueue] Report a ClusterQueue as inactive (misconfigured) if there is ProvReq used with MK

**Summary**: [MultiKueue] Report a ClusterQueue as inactive (misconfigured) if there is ProvReq used with MK

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2023

**Last updated**: 2025-12-19T08:00:30Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-04-19T14:45:49Z
- **Updated**: 2025-12-19T08:00:30Z
- **Closed**: 2025-12-19T08:00:29Z
- **Labels**: `kind/feature`
- **Assignees**: [@bouaouda-achraf](https://github.com/bouaouda-achraf)
- **Comments**: 25

## Description

**What would you like to be added**:

Validation for ClusterQueue, if there is a MK and ProvReq admission check configured.

**Why is this needed**:

Provisioning nodes on the management cluster does not make sense.
We want to fail fast, and warn user about possibly wasted money to scale-up the cluster.

**Proposed approach**:

Use a mechanism similar to the one here: https://github.com/kubernetes-sigs/kueue/pull/1635.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-04-19T14:46:04Z

/assign @trasc 
/cc @alculquicondor

### Comment by [@mimowo](https://github.com/mimowo) — 2024-04-26T08:12:01Z

I reviewed https://github.com/kubernetes-sigs/kueue/pull/2047, and I think we could follow the pattern here. 

The `AdmissionCheck` condition would be `CompatibleWithMultiKueue`, and the reason for inactive ClusterQueue could be `AdmissionCheckNonCompatibleWithMultiKueue`. We would do the check inside `updateWithAdmissionChecks` as for other checks.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-04-26T13:45:01Z

The only problem is that the condition would be specific to MultiKueue. What if other checks need similar semantics against others?

I would rather sit on this one for now until we observe more admission checks, in-tree or out-of-tree.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-05-07T16:15:40Z

> What if other checks need similar semantics against others?

Right, this approach cannot be used for arbitrary pairs of admission checks. However, MultiKueue seems more than an admission check. For example, it has a global configuration in the config map [link](https://github.com/kubernetes-sigs/kueue/blob/de1fe1f6ff69e88e62c51f89428a5addc00ffadc/apis/config/v1beta1/configuration_types.go#L71-L72).

> I would rather sit on this one for now until we observe more admission checks, in-tree or out-of-tree.

I see, but it can take a long time until we have other pairs of AdmissionChecks which don't like each other, and having some protection before graduating MK and ProvReq to Beta would be nice. 

The approach using the existing mechanism should be very quick to implement, and if one day we have a more generic mechanism, developed for the needs of other AC pairs, then we could switch to it.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-07T17:35:59Z

Let's wait and see

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2024-05-16T16:12:17Z

/assign

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2024-05-17T07:08:24Z

/unassign

### Comment by [@bouaouda-achraf](https://github.com/bouaouda-achraf) — 2024-07-07T19:27:36Z

/assign

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-07-08T12:20:06Z

@mimowo I think we don't have a proper design for this. And it hasn't proved to be very useful. Should we close it?

### Comment by [@mimowo](https://github.com/mimowo) — 2024-07-08T13:21:26Z

I'm ok to close it until we revisit the design or some evidence for users running into this issue.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-07-08T14:18:57Z

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-07-08T14:19:01Z

@alculquicondor: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/2023#issuecomment-2214209387):

>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-06T15:39:07Z

/reopen
I believe with the recent changes (https://github.com/kubernetes-sigs/kueue/pull/3254) to make cache aware of the MultiKueue and ProvisioningRequest AdmissionChecks we can easily validate this conditions.
cc @mbobrovskyi @mszadkow

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-12-06T15:39:13Z

@mimowo: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/2023#issuecomment-2523518677):

>/reopen
>I believe with the recent changes (https://github.com/kubernetes-sigs/kueue/pull/3254) to make cache aware of the MultiKueue and ProvisioningRequest AdmissionChecks we can easily validate this conditions.
>cc @mbobrovskyi @mszadkow 


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-03-06T16:01:57Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-06T16:08:32Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-06-04T16:10:05Z

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

### Comment by [@samos123](https://github.com/samos123) — 2025-06-16T21:52:30Z

Hitting this and unsure why this is happening. Any insights?

Kubectl describe workload
```
Status:
  Conditions:
    Last Transition Time:  2025-06-16T21:48:02Z
    Message:               ClusterQueue cluster-queue is inactive
    Observed Generation:   1
    Reason:                Inadmissible
    Status:                False
    Type:                  QuotaReserved
```


```
k get clusterqueue
NAME            COHORT   PENDING WORKLOADS
cluster-queue            31

k get localqueue
NAME               CLUSTERQUEUE    PENDING WORKLOADS   ADMITTED WORKLOADS
multislice-queue   cluster-queue   31                  0
```

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-07-16T22:49:44Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle rotten

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-07T08:22:43Z

/remove-lifecycle rotten

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-07T08:24:00Z

@samos123 what is your CQ configuration? Maybe provide the entire `kubectl describe` for the CQ

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-11-05T08:30:04Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-05T08:32:24Z

/remove-lifecycle stale

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T08:00:24Z

/close
Let me reopen in the new context

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-12-19T08:00:30Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/2023#issuecomment-3673995471):

>/close
>Let me reopen in the new context


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
