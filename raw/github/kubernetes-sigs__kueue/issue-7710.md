# Issue #7710: API Inconsistency in Fair Sharing and Admission Fair Sharing Configuration

**Summary**: API Inconsistency in Fair Sharing and Admission Fair Sharing Configuration

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7710

**Last updated**: 2026-03-31T14:04:18Z

---

## Metadata

- **State**: open
- **Author**: [@MichalZylinski](https://github.com/MichalZylinski)
- **Created**: 2025-11-17T14:18:32Z
- **Updated**: 2026-03-31T14:04:18Z
- **Closed**: —
- **Labels**: `kind/feature`, `priority/important-longterm`
- **Assignees**: [@andrewseif](https://github.com/andrewseif)
- **Comments**: 4

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
