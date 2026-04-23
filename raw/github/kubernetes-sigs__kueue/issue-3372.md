# Issue #3372: TAS: support all Job CRDs (including Pods)

**Summary**: TAS: support all Job CRDs (including Pods)

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3372

**Last updated**: 2024-11-05T15:20:21Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-10-30T08:05:45Z
- **Updated**: 2024-11-05T15:20:21Z
- **Closed**: 2024-11-05T15:20:20Z
- **Labels**: `kind/feature`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 7

## Description

**What would you like to be added**:

Add support for all Job CRDs. Currently we have Job and JobSet covered.

This consists two parts:
- computation of the TopologyRequest as in [here](https://github.com/kubernetes-sigs/kueue/blob/1e6d6cc6ae5124bd0317adf34724656bdbe7a812/pkg/controller/jobs/jobset/jobset_controller.go#L124)
-  validation as in [here](https://github.com/kubernetes-sigs/kueue/blob/1e6d6cc6ae5124bd0317adf34724656bdbe7a812/pkg/controller/jobs/jobset/jobset_webhook.go#L135)

The above should be unit tested (new TestPodSets function per CRD).
I suggest one PR per CRD so that we can release at any point, even if not all are done.

**Why is this needed**:

This is part of https://github.com/kubernetes-sigs/kueue/issues/2724 which can be easily separated as another task.
To support TAS for all Job CRDs, it is a point of the plan in the [spreadsheet](https://docs.google.com/spreadsheets/d/1MXCjKZtAfqBTb61bJo46u7jIUqRIlu1NrYj1L8Xz-UU/)

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-30T08:05:59Z

/assign @mbobrovskyi 
cc @PBundyra @tenzen-y

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-10-30T19:56:16Z

> /assign @mbobrovskyi cc @PBundyra @tenzen-y

+1
We can just move all Job support to the Alpha stage in the KEP.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-31T07:10:02Z

I have also synced with @mbobrovskyi we will add a basic integration test per integration. From Job creation to create workload assignment

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-10-31T15:54:26Z

/reopen

Oops. Added fixes by mistake on https://github.com/kubernetes-sigs/kueue/pull/3402.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-10-31T15:54:32Z

@mbobrovskyi: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3372#issuecomment-2450232615):

>/reopen


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-05T15:20:14Z

/close
Up to my knowledge we have all CRDs covered

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-11-05T15:20:20Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3372#issuecomment-2457454745):

>/close
>Up to my knowledge we have all CRDs covered


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
