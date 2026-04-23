# Issue #2941: Support Structured Parameters (DRA) in Kueue

**Summary**: Support Structured Parameters (DRA) in Kueue

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2941

**Last updated**: 2026-04-09T20:56:58Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kannon92](https://github.com/kannon92)
- **Created**: 2024-08-30T13:51:42Z
- **Updated**: 2026-04-09T20:56:58Z
- **Closed**: 2026-04-09T20:56:57Z
- **Labels**: `kind/feature`
- **Assignees**: [@kannon92](https://github.com/kannon92), [@alaypatel07](https://github.com/alaypatel07)
- **Comments**: 31

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
Workloads should be able to use Resource Claims in their specs and Kueue should be aware of this when doing quota management.
**Why is this needed**:
Support DRA.
**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [x] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2024-08-30T14:04:26Z

Hoping to maybe discuss first what has been done with DRA. I can help with a KEP once we have a path forward.

@alculquicondor @tenzen-y Have either of you looked into how Kueue would work with DRA resources?

https://github.com/kubernetes-sigs/dra-example-driver/tree/main/demo

has a list of a few examples of how structured parameters works.

```yaml
---
apiVersion: v1
kind: Pod
metadata:
  namespace: gpu-test1
  name: pod1
  labels:
    app: pod
spec:
  containers:
  - name: ctr0
    image: ubuntu:22.04
    command: ["bash", "-c"]
    args: ["export; sleep 9999"]
    resources:
      claims:
      - name: gpu
  resourceClaims:
  - name: gpu
    resourceClaimTemplateName: gpu.example.com
```

Containers would now have a claim and the resourceClaimTemplate would dictate exactly what is being requested. It seems that there may be some indirection Kueue would need to take to support this.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-08-30T14:26:36Z

Nothing has been done for DRA :)

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-08-30T14:26:58Z

The only other related issue is #1538

### Comment by [@kannon92](https://github.com/kannon92) — 2024-08-30T14:41:18Z

Okay. I'm going to spend some cycles thinking about this then.
/assign

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-08-30T16:43:02Z

This looks great! 
@kannon92 Which will you take the DRA? Classic DRA? or DRA with structured parameters?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-08-30T17:08:58Z

Classic DRA is likely getting removed in the next few versions, so I wouldn't like to invest on it in Kueue.

### Comment by [@kannon92](https://github.com/kannon92) — 2024-08-30T17:09:12Z

Hey @tenzen-y. From the source (https://github.com/kubernetes/enhancements/issues/3063#issuecomment-2302065085), Classic DRA may be dropped in 1.32 so I will go with structured parameters

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-08-30T17:15:51Z

I agree with you.
In that case, we can somehow take the exact resource amount from the ResourceSlice object.
Although, we maybe want to tackle to handle ResourceSlice object as the separate features.

It would be great if you could consider the future ResourceSlice collaboration in this design.
In other words, I don't want to block the possibility of collaborating with Kueue and ResourceSlice with this ResourceClaim feature.

### Comment by [@kannon92](https://github.com/kannon92) — 2024-08-30T17:17:13Z

/retitle Support Structured Parameters (DRA) in Kueue

### Comment by [@kannon92](https://github.com/kannon92) — 2024-08-30T17:17:56Z

I think the API I use is what I need to research. Going to retitle as I don't have a clear direction yet.

### Comment by [@kannon92](https://github.com/kannon92) — 2024-08-30T17:22:40Z

So @tenzen-y you are saying that something like:

```yaml
---
apiVersion: v1
kind: Namespace
metadata:
  name: gpu-test4

---
apiVersion: resource.k8s.io/v1alpha3
kind: ResourceClaimTemplate
metadata:
  namespace: gpu-test4
  name: multiple-gpus
spec:
  spec:
    devices:
      requests:
      - name: gpus
        deviceClassName: gpu.example.com
        allocationMode: ExactCount
        count: 4

---
apiVersion: v1
kind: Pod
metadata:
  namespace: gpu-test4
  name: pod0
  labels:
    app: pod
spec:
  containers:
  - name: ctr0
    image: ubuntu:22.04
    command: ["bash", "-c"]
    args: ["export; sleep 9999"]
    resources:
      claims:
      - name: gpus
  resourceClaims:
  - name: gpus
    resourceClaimTemplateName: multiple-gpus
```

In this case, if a resourceClaimTemplate is using an allocationMode of ExactCount, that may be easier to support.

@alculquicondor @tenzen-y I'm open to suggestions on how you want to tackle DRA support in Kueue. We could piece by piece it or we create a KEP walking through the different options?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-08-30T17:29:06Z

cc @johnbelamaric @pohly

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-08-30T17:39:19Z

@kannon92 I'm not sure which approaches we should take here. I guess that DRA support is a big project, and we need to support all features step by step.
So, we want to evaluate in the KEP which features are supported in which iteration.

### Comment by [@kannon92](https://github.com/kannon92) — 2024-09-03T13:21:20Z

So I am not exactly sure what how we want to limit DRA claims in a ClusterQueue. I was thinking that we could add a counts to the claims but ResourceClaims are namespace scoped.

We could require that ResoureClaims that Kueue needs to be aware of in ClusterQueue are cluster scoped and enforce that?

It does look like ResourceSlices are cluster scoped so that could be an option.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-09-24T15:35:06Z

> So I am not exactly sure what how we want to limit DRA claims in a ClusterQueue. I was thinking that we could add a counts to the claims but ResourceClaims are namespace scoped.
> 
> We could require that ResoureClaims that Kueue needs to be aware of in ClusterQueue are cluster scoped and enforce that?
> 
> It does look like ResourceSlices are cluster scoped so that could be an option.

That makes sense. Let's discuss it in the KEP.

### Comment by [@kannon92](https://github.com/kannon92) — 2024-09-24T15:50:32Z

@tenzen-y I drafted the main idea I have in the KEP. We can defer those discussions to there for now on.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-12-23T16:02:54Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-12-28T19:45:00Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-03-28T20:14:14Z

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

### Comment by [@johnbelamaric](https://github.com/johnbelamaric) — 2025-03-28T21:16:05Z

/remove-lifecycle stale

### Comment by [@kannon92](https://github.com/kannon92) — 2025-04-10T16:23:23Z

/assign @alaypatel07 

I don't have much cycles to focus on this anymore but @alaypatel07 has volunteered to take this work on. 

Thank you @alaypatel07!

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-04-10T16:23:27Z

@kannon92: GitHub didn't allow me to assign the following users: alaypatel07.

Note that only [kubernetes-sigs members](https://github.com/orgs/kubernetes-sigs/people) with read permissions, repo collaborators and people who have commented on this issue/PR can be assigned. Additionally, issues/PRs can only have 10 assignees at the same time.
For more information please see [the contributor guide](https://git.k8s.io/community/contributors/guide/first-contribution.md#issue-assignment-in-github)

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/2941#issuecomment-2794428774):

>/assign @alaypatel07 
>
>I don't have much cycles to focus on this anymore but @alaypatel07 has volunteered to take this work on. 
>
>Thank you @alaypatel07!


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@alaypatel07](https://github.com/alaypatel07) — 2025-04-11T21:44:04Z

/assign

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-07-10T21:45:47Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-07-11T14:02:50Z

/remove-lifecycle stale

### Comment by [@alaypatel07](https://github.com/alaypatel07) — 2025-11-09T21:41:03Z

/reopen

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-11-09T21:41:08Z

@alaypatel07: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/2941#issuecomment-3508862140):

>/reopen


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-02-07T22:18:18Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-02-11T12:18:48Z

/remove-lifecycle stale

### Comment by [@kannon92](https://github.com/kannon92) — 2026-04-09T20:56:50Z

I don't know if we need to track this issue anymore.

DRA is in Kueue and work is ongoing to get this more stable.

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-04-09T20:56:58Z

@kannon92: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/2941#issuecomment-4217426144):

>I don't know if we need to track this issue anymore.
>
>DRA is in Kueue and work is ongoing to get this more stable.
>
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
