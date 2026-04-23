# Issue #3232: MVP support for serving workloads running as LeaderWorkerSet

**Summary**: MVP support for serving workloads running as LeaderWorkerSet

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3232

**Last updated**: 2025-03-10T08:11:04Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-10-15T06:50:04Z
- **Updated**: 2025-03-10T08:11:04Z
- **Closed**: 2025-03-10T08:11:02Z
- **Labels**: `kind/feature`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 13

## Description

**What would you like to be added**:

MVP support for LeaderWorkerSet in Kueue. It does not need to be ideal, but we want to have some support to unblock users and collect users' feedback. 

The idea is to base the support on StatefulSets, so the integration would also use Pod Groups, similarly as for regular StatefulSets. Each LeaderWorkerGroup creates a new Pod Group. I a single pod group we will have:

- Leader pod, controller by Leader’s STS
- Worker pods, controller by unique, dedicated STS

The size of the group will be taken from LeaderWorkerSet.Spec.LeaderWorkerTemplate.Size and increased by 1 (to include the leader).

This is a follow up to https://github.com/kubernetes-sigs/kueue/issues/2717.

**Why is this needed**:

We want to support serving primitives in Kueue as there is an increasing demand among users to run clusters mixing AI training and inference who want to manage the expensive GPU resources.

[LeaderWorkerSet](https://github.com/kubernetes-sigs/lws) is a new serving API which is gaining popularity as a primitive to host AI/ML inference.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-15T06:50:13Z

/assign @vladikkuzn

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-15T06:50:22Z

/cc @mwielgus @tenzen-y

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-02T11:13:11Z

I synced with @mbobrovskyi and @vladikkuzn on the feature and it seems complex, so I propose to have a KEP for it, and go via the Alpha phase so that we can update the implementation in the future easily.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-16T15:27:35Z

The already identified follow ups needed after https://github.com/kubernetes-sigs/kueue/pull/3515:
- support for resizing the LWS group by group  (potentially the same PR, but might be follow up) [already done in the main PR]
- support for the default StartupPolicy=LeaderReady
- support for TAS with rank-based ordering (with e2e tests)
- https://github.com/kubernetes-sigs/kueue/issues/4000

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-28T15:22:20Z

/reopen
to finalize the integration with TAS

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-01-28T15:22:26Z

@mimowo: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3232#issuecomment-2619313252):

>/reopen
>to finalize the integration with TAS 


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-28T15:24:19Z

Also, I would like to have e2e test for scaling the LWS when Startup policy is Leader ready (default).

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-02-04T10:10:42Z

/unassign @vladikkuzn 
/assign

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-12T18:01:14Z

@mbobrovskyi @mimowo Will you finalize MultiKueue and TAS support within this MVP issue?

### Comment by [@kannon92](https://github.com/kannon92) — 2025-03-08T15:56:32Z

What outstanding items do we have for this ticket?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-10T08:10:38Z

I think we can close it, AFAIK the only outstanding work for now is the support of rank-based ordering in TAS for groups.
However, I would  not call it MVP any longer: https://github.com/kubernetes-sigs/kueue/issues/4531

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-10T08:10:58Z

/close
Thank you @mbobrovskyi for the implementation!

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-03-10T08:11:03Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3232#issuecomment-2709742137):

>/close
>Thank you @mbobrovskyi for the implementation!


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
