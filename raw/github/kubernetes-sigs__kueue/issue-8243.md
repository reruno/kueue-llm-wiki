# Issue #8243: Tracking DRA Support for Beta

**Summary**: Tracking DRA Support for Beta

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8243

**Last updated**: 2026-04-02T12:23:53Z

---

## Metadata

- **State**: open
- **Author**: [@sohankunkerkar](https://github.com/sohankunkerkar)
- **Created**: 2025-12-15T13:55:44Z
- **Updated**: 2026-04-02T12:23:53Z
- **Closed**: —
- **Labels**: `kind/feature`, `priority/important-soon`
- **Assignees**: [@sohankunkerkar](https://github.com/sohankunkerkar)
- **Comments**: 20

## Description

 ## Context

  DRA support in Kueue is currently Alpha, supporting ResourceClaimTemplates with `AllocationMode=ExactCount` and DeviceClass mapping.

  This issue is to discuss what's needed for Beta, aligned with upstream Kubernetes DRA development.

  KEP: [keps/2941-DRA](https://github.com/kubernetes-sigs/kueue/tree/main/keps/2941-DRA)

  ---

  ## Gaps in Current Implementation

  DRA Structured Parameters is GA in Kubernetes 1.34.

  ### Affects Quota (Needs Implementation)

  | Capability | Description |
  |------------|-------------|
  | AllocationMode=All | Request all devices on a node |
  | Direct ResourceClaims | Reference pre-created claims |
  | CEL Selectors | Filter devices by attributes (only with AllocationMode=All) |

  ### Does Not Affect Quota (Remove Rejection)

  | Capability | Description |
  |------------|-------------|
  | Device Constraints | Co-location requirements - pass through to scheduler |
  | Device Config | Driver configuration - pass through to scheduler |

  ---

  ## Upstream Features to Track

  | Feature | Kubernetes Status | Feature Gate |
  |---------|-------------------|--------------|
  | FirstAvailable | Beta | `DRAPrioritizedList` |
  | Extended Resources | Alpha | `DRAExtendedResource` |
  | Partitionable Devices | Alpha | `DRAPartitionableDevices` |
  | Consumable Capacity | Alpha | `DRAConsumableCapacity` |
  | Admin Access | Alpha | `DRAAdminAccess` |
  | Device Taints | Alpha | `DRADeviceTaints` |

  ---

  ## Discussion

  1. Which capabilities are required for Kueue DRA Beta?
  2. CEL Selectors: conservative counting or CEL evaluation?
  3. Should we include k8s Beta features (FirstAvailable)?
  4. Any Alpha features we should wait for?

## Discussion

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2025-12-15T14:41:12Z

/kind discussion

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-12-15T14:41:14Z

@sohankunkerkar: The label(s) `kind/discussion` cannot be applied, because the repository doesn't have them.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/8243#issuecomment-3656012214):

>/kind discussion


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2025-12-15T14:44:45Z

/kind feature

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2025-12-15T14:59:39Z

cc @alaypatel07

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T09:36:02Z

/priority important-soon

### Comment by [@kannon92](https://github.com/kannon92) — 2025-12-19T19:16:35Z

I'd also like to see e2e tests for beta. I'm fine with using the fake dra driver but I think this feature should have e2e testing before beta.

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2025-12-19T19:43:15Z

/assign

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2025-12-19T22:14:33Z

Jotting down here for posterity. Things to consider for Beta:
- Support v1 API of DRA in core K8s
- Beta status for `Extended Resources` and `Partitionable Devices` in k8s
- Support integration with MultiKueue
- E2E tests using dra-example-driver

### Comment by [@kannon92](https://github.com/kannon92) — 2025-12-28T18:10:36Z

I think Kueue DRA is using v1 APIs now.

https://github.com/kubernetes-sigs/kueue/commit/9ac669dc55a0cd89abb53477fafd6e465c87fcaf

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-01-05T15:32:03Z

> I think Kueue DRA is using v1 APIs now.
> 
> [9ac669d](https://github.com/kubernetes-sigs/kueue/commit/9ac669dc55a0cd89abb53477fafd6e465c87fcaf)

Yes, based on that I have raised https://github.com/kubernetes-sigs/kueue/pull/8421

### Comment by [@alaypatel07](https://github.com/alaypatel07) — 2026-01-05T23:38:53Z

IMO, before going to beta, we should explore what the support for Extended Resources backed by DRA will look like in Kueue. There are overlapping concepts with DRA support in Kueue and Extended Resources backed by DRA in k8s, like the need for creating a mapping from a extended resources string -> to a device class. This work will prove out the gaps if any in the current solution that will help boost confidence for beta.

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-01-06T18:01:13Z

Thanks for raising this. I looked into Extended Resources backed by DRA details. IIUC, the current alpha logic should handle the runtime behavior. When users request GPUs via extended resource syntax (no explicit `ResourceClaimTemplate`), Kueue extracts it as part of normal pod resource aggregation. Explicit `ResourceClaimTemplates` and `Extended Resources` backed by DRA are alternative approaches, so no double-counting in normal usage.

The main concerns I see for Beta:

1. Config mismatch risk: If Kueue's `DeviceClassMapping` and `DeviceClass.spec.extendedResourceName` diverge, quota could be counted differently depending on whether users use explicit `ResourceClaimTemplates` vs extended resource syntax.
2. Redundant config: When using Extended Resources backed by DRA, the `DeviceClassMapping` becomes unnecessary since the mapping already lives in the `DeviceClass` itself.

Should we consider reading from `DeviceClass.spec.extendedResourceName` directly for Beta? Or at minimum, validate/warn on mismatch?

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-09T14:26:03Z

One follow up from the e2e testing PR: https://github.com/kubernetes-sigs/kueue/pull/8421#discussion_r2676232741

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-01-19T18:19:51Z

> One follow up from the e2e testing PR: [#8421 (comment)](https://github.com/kubernetes-sigs/kueue/pull/8421#discussion_r2676232741)

This is fixed by https://github.com/kubernetes-sigs/kueue/pull/8503

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-01-19T18:20:58Z

I have up up a PR to add support for extended resource support: https://github.com/kubernetes-sigs/kueue/pull/8597

I would appreciate the feedback.

### Comment by [@alaypatel07](https://github.com/alaypatel07) — 2026-01-19T21:00:50Z

@sohankunkerkar do you have a design doc explaining the implementation of extended resources by DRA in kueue? It would be good to have a PR updating the original KEP to reflect the implementation

### Comment by [@kannon92](https://github.com/kannon92) — 2026-01-19T21:45:25Z

https://github.com/kubernetes-sigs/kueue/pull/8597/commits/a3df960d4e806095d071194fbf0fab822fd6ae6d pushes an update to the KEP.

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-01-19T22:01:41Z

> [@sohankunkerkar](https://github.com/sohankunkerkar) do you have a design doc explaining the implementation of extended resources by DRA in kueue? It would be good to have a PR updating the original KEP to reflect the implementation

I can create a separate PR for the KEP if you think https://github.com/kubernetes-sigs/kueue/pull/8597
 is too hairy.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-20T11:56:59Z

@sohankunkerkar @kannon92 it would be great to prepare documentation for the DRA integration. I can imagine 2 pages:
- concepts describing high level
- tasks page for "hands on" tutorial for using the feature
wdyt?

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-03-20T12:16:46Z

> [@sohankunkerkar](https://github.com/sohankunkerkar) [@kannon92](https://github.com/kannon92) it would be great to prepare documentation for the DRA integration. I can imagine 2 pages:
> 
> * concepts describing high level
> * tasks page for "hands on" tutorial for using the feature
>   wdyt?

Yup, that makes sense!  This is next item on my radar.
