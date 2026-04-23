# Issue #2717: MVP support / extension of support for serving workloads

**Summary**: MVP support / extension of support for serving workloads

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2717

**Last updated**: 2024-10-30T06:27:28Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-07-29T13:05:23Z
- **Updated**: 2024-10-30T06:27:28Z
- **Closed**: 2024-10-30T06:27:28Z
- **Labels**: `kind/feature`
- **Assignees**: [@vladikkuzn](https://github.com/vladikkuzn)
- **Comments**: 17

## Description

**What would you like to be added**:

I would like to make sure we have basic support for running serving workloads for the use case of running AI inference.
In particular I would like to have support for Deployments, StatefulSets, and LeaderWorkerSets. 

In the MVP work the integrations are based on single Plain pods (for Deployments) or Pod Groups (for StatefulSets).

1. *Deployments* 
This is a follow up to https://github.com/kubernetes-sigs/kueue/issues/2677.

What is needed:
- introduce a dedicated Deployment integration, and validate that it can only be enabled when pod integration is enabled
- copy the queue-name from Deployment down to PodTemlates

2. *StatefulSets*

What is needed:
- introduce a dedicated StatefulSet integration, and validate that it can only be enabled when pod integration is enabled
- copy the queue-name from StatefulSet down to PodTemlates
- set the PodTemaplate labels for the PodGroup:
  
* kueue.x-k8s.io/queue-name - from STS
* kueue.x-k8s.io/pod-group-name - STS_ + STS name (+ probably some hash to avoid collisions as for workloads)
* kueue.x-k8s.io/pod-group-total-count - STS replica count 

In the longer run to support scaling of stateful sets we may need to do https://github.com/kubernetes-sigs/kueue/issues/77, but this is out of scope for the issue,

3. LeaderWorkerSet support is moved to a dedicated issue: https://github.com/kubernetes-sigs/kueue/issues/3232

**Why is this needed**:

To support use cases of running AI training and inference in the same clusters, where the access to GPU is constrained by Kueue.

**Completion requirements**:

The API changes required are minimal (just potentially new labels / annotations), so I believe a new KEP is not required, but we need a proper documentation.

This enhancement requires the following artifacts:

- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-07-29T13:10:26Z

/assign @trasc

### Comment by [@mimowo](https://github.com/mimowo) — 2024-07-29T13:15:40Z

/cc @mwielgus @tenzen-y @dgrove-oss

### Comment by [@kannon92](https://github.com/kannon92) — 2024-07-29T13:51:30Z

/cc @liurupeng @ahg-g 
for LWS.

### Comment by [@kannon92](https://github.com/kannon92) — 2024-07-29T13:52:11Z

For LWS, would including a suspend field be a better forward thinking strategy?

### Comment by [@mimowo](https://github.com/mimowo) — 2024-07-29T14:23:58Z

> For LWS, would including a suspend field be a better forward thinking strategy?

For now complete "suspend" for serving workload isn't a use case we hear about. The preference is to reduce capacity by preempting individual pods, so that stopping a serving workload completely is the last resort option. 

However, it is hard to say "never" in the long run, but I would keep it out of scope for this enhancement.

### Comment by [@kannon92](https://github.com/kannon92) — 2024-07-29T14:27:57Z

Sounds good. I guess in LWS case preemptiong would be the entire leader-worker group? Or preempting some workers?

### Comment by [@mimowo](https://github.com/mimowo) — 2024-07-29T14:31:19Z

For now, the entire group.

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2024-08-07T09:00:38Z

/assign

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-08-30T16:44:04Z

It looks like that this contains LWS and StatefulSet.
/reopen

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-08-30T16:44:08Z

@tenzen-y: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/2717#issuecomment-2321945727):

>It looks like that this contains LWS and StatefulSet.
>/reopen
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@kerthcet](https://github.com/kerthcet) — 2024-10-12T03:05:44Z

> For now complete "suspend" for serving workload isn't a use case we hear about.

+1 on behave of LWS. And evicting the entire group(leaderPod + workerSts) is the right path because they working as an unit, what you need to do is just reduce the **Replicas** to the resource boundary.

Some other feedbacks, as the maintainer of [llmaz](https://github.com/InftyAI/llmaz), another inference platform, what we need most is the capacity of accelerator fungibility, the same model could be served by several different kinds of GPUs for the sake of cost and performance. I think kueue can help in some ways, actually part of our integration roadmap. Ourself will implement the capacity as well but considering our customers are also using kueue, this could be a centralized control plane.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-10-14T15:16:32Z

@mimowo Couldn't we split LWS to a separate issue as we mentioned in the next release issue?

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-14T15:21:22Z

Sure, we can, would you like to do so? Otherwise I can split it tomorrow.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-10-14T15:26:29Z

> Sure, we can, would you like to do so? Otherwise I can split it tomorrow.

I'm not in a hurry. So, I'm ok with tomorrow.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-15T06:50:33Z

Done: https://github.com/kubernetes-sigs/kueue/issues/3232. PTAL

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-23T13:50:21Z

/reopen 
Let's close it when documentation for StatefulSet lends. cc @vladikkuzn

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-10-23T13:50:26Z

@mimowo: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/2717#issuecomment-2432272367):

>/reopen 
>Let's close it when documentation for StatefulSet lends. cc @vladikkuzn 


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
