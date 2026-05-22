# Issue #7710: API Inconsistency in Fair Sharing and Admission Fair Sharing Configuration

**Summary**: API Inconsistency in Fair Sharing and Admission Fair Sharing Configuration

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7710

**Last updated**: 2026-05-21T14:55:59Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@MichalZylinski](https://github.com/MichalZylinski)
- **Created**: 2025-11-17T14:18:32Z
- **Updated**: 2026-05-21T14:55:59Z
- **Closed**: 2026-05-21T14:55:58Z
- **Labels**: `kind/feature`, `priority/important-longterm`
- **Assignees**: [@andrewseif](https://github.com/andrewseif)
- **Comments**: 8

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

To improve API consistency, we propose consolidating the configuration for both Fair Sharing (FS) and Admission Fair Sharing (AFS) under a single, unified fairSharing object in the ClusterQueueSpec.

Currently, Fair Sharing is configured in `spec.fairSharing`, while Admission Fair Sharing is configured separately in `spec.admissionScope`. We recommend moving the AFS configuration to be nested within the fairSharing object.

Here is an example of the proposed structure:
```
...
fairSharing:
  weight: "1"
  admissionFairSharing: # new substruct for AFS
    mode: "UsageBasedAdmissionFairSharing"
...
```

**Why is this needed**:
There is an inconsistency between how fair sharing status is reported and how it is configured.

The status for both FS and AFS is combined within the FairSharingStatus object (`ClusterQueueStatus.fairSharing`). However, their configurations are split across two different fields in the ClusterQueue specification. This separation is unintuitive and makes the API harder to use.

Unifying the configuration to mirror the status structure would provide several benefits:

* Improved Consistency: The configuration and status APIs would align, creating a more predictable user experience.

* Better Discoverability: Users would find all fair sharing-related settings in a single, logical location.

* Enhanced Readability: The relationship between Fair Sharing and Admission Fair Sharing would be much clearer in the spec.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [x] API change
- [ ] Docs update

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T10:32:24Z

/priority important-longterm

### Comment by [@andrewseif](https://github.com/andrewseif) — 2026-03-16T16:27:29Z

I would like to work on this, if that's ok 😄

### Comment by [@andrewseif](https://github.com/andrewseif) — 2026-03-16T16:27:35Z

/assign

### Comment by [@kannon92](https://github.com/kannon92) — 2026-03-31T14:04:17Z

I commented on #10244 but changing the API is a breaking change.

We could consider this for v1 but I don't think we should make this change in v1beta1 or v1beta2.

### Comment by [@PBundyra](https://github.com/PBundyra) — 2026-05-18T09:02:48Z

IIRC after the PR: https://github.com/kubernetes-sigs/kueue/pull/7793 AFS status is not reported in the CQ at all. Currently the only place it's reported is LQ status. 

I think we need more discussion on what's our desired state. On the one hand, currently both AFS and preemption-based FS use `fairSharing.weight` API in LQ's/CQ/'s spec. So there's some existing overlap. On the other hand, I'm not fully convinced we should pursue having config/status in one place for both AFS and preemption-based FS. Those features can work independently and (at least currently) have little in common since one works on the LQ level, and the other one works on CQ/Cohort level. Maybe we should have aim for a clear distinction on the API level to hint admin, those are two separate features

### Comment by [@PBundyra](https://github.com/PBundyra) — 2026-05-18T09:03:02Z

/cc @mimowo @MichalZylinski @mwielgus

### Comment by [@kannon92](https://github.com/kannon92) — 2026-05-21T14:55:52Z

In our community meeting, we realize that we are not ready to take this change on. There is discussion needed on AFS at scale and there are other features that may change this API.

We are going to close this issue for now until we figure out the long term plan for AFS.

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-05-21T14:55:59Z

@kannon92: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/7710#issuecomment-4509488680):

>In our community meeting, we realize that we are not ready to take this change on. There is discussion needed on AFS at scale and there are other features that may change this API.
>
>We are going to close this issue for now until we figure out the long term plan for AFS.
>
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
