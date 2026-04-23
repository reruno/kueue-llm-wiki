# Issue #8201: Disable RayJob integration

**Summary**: Disable RayJob integration

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8201

**Last updated**: 2026-01-21T10:08:46Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@yaroslava-serdiuk](https://github.com/yaroslava-serdiuk)
- **Created**: 2025-12-12T10:30:13Z
- **Updated**: 2026-01-21T10:08:46Z
- **Closed**: 2026-01-21T10:08:46Z
- **Labels**: `kind/cleanup`, `priority/important-longterm`
- **Assignees**: _none_
- **Comments**: 8

## Description

The following KubeRay Custom Resources (CRs) are used to manage Ray applications:
- RayCluster
- RayJob
- RayService

The central object is the RayCluster. Both RayJob and RayService are designed to configure and initiate a RayCluster.

**Current Integration with Kueue**
The following points summarize how Ray resources currently integrate with Kueue:
- RayCluster objects are managed directly by Kueue.
- RayService objects are not directly managed by Kueue. Instead, Kueue manages the RayCluster that is created by the RayService.
- RayJob objects can be managed by Kueue, with management logic depending on how the RayJob is configured:
  - If the RayJob uses a pre-existing RayCluster, Kueue doesn’t manage RayJob; in this case, Kueue manages only the RayCluster.
  - **If the RayJob creates a new RayCluster object, it involves**:
     - **Kueue manages the RayJob if the RayCluster uses a disabled autoscaler.**
     - If the RayCluster has autoscaler enabled, Kueue manages the RayCluster instead of the RayJob. ([PR](https://github.com/kubernetes-sigs/kueue/pull/7769))


All above idicates that RayJob integration could be disabled, so the Kueue manages directly RayCluster object.


**Advantages of disabling RayJob integration:** 
- Simplifies the code. So the hacks as IsTopLevel() or Skip() for RayJob in autoscaling or pre-existing RayCluster scenarios won't be needed. 
- Tight relationship between Kueue and RayCluster features would make quick support for Ray features in all Ray job types. 


**Disadvantages**  
- If RayJob were to create pods outside of RayCluster, Kueue would not be able to manage them. However, this scenario is currently inconsistent with KubeRay's established design principles.


**Required changes:**

- [ ] Update webhook for RaySubmitterJob to add a queue label. But this is already a case when autoscaling is enabled. 
- [ ] We should have multiple releases with disabled RayJob by default but still being able to enable it. And if there would be no issues during couple of releases, the integration could be removed.

## Discussion

### Comment by [@yaroslava-serdiuk](https://github.com/yaroslava-serdiuk) — 2025-12-12T11:08:10Z

/cc @mimowo @andrewsykim

### Comment by [@hiboyang](https://github.com/hiboyang) — 2025-12-12T16:21:36Z

Agree with the proposal here! This will simplify Kueue code base to handle RayJob/RayService, and good for long term maintainability. I can work on this if people decide to proceed.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-12-12T17:41:34Z

cc @laurafitzgerald

### Comment by [@kannon92](https://github.com/kannon92) — 2025-12-12T17:42:46Z

IMO many people treat integrations as an important API.

I ask that disabling integrations undergo a deprecation process to give people a release or two to migrate.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-15T06:34:52Z

I like the direction.

However, we need some deprecation plan as mentioned in https://github.com/kubernetes-sigs/kueue/issues/8201#issuecomment-3647515124. 

Something like:
1. support for running rayjob via Kueue (no autoscaling) when RayJob integration is disabled (using similar mechanism as currently, but as a fallback when rayjob integration is disabled), integration & e2e tests for running RayJob when rayjob integration is disabled
2. disable rayjob integration by default and deprecate
3. drop support for enabling rayjob integration

So here:
- (1.) is a preparatory step to ensure it can be done safely without losing functionality for users
- (2.) is deprecation and changing of default
- (3.) actual drop

While (1.) and (2.) may happen in the same release say 0.16, (3.) needs to be delayed by two releases at least.

### Comment by [@hiboyang](https://github.com/hiboyang) — 2025-12-18T21:13:03Z

To move this forward, I created a PR to make RayCluster and Submitter Job always top level for RayJob: https://github.com/kubernetes-sigs/kueue/pull/8341 . This is part of (1.) in the discussion.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T09:36:22Z

/priority important-longterm

### Comment by [@yaroslava-serdiuk](https://github.com/yaroslava-serdiuk) — 2026-01-21T10:08:46Z

[MultiKueue: Support Elastic RayJob #8712](https://github.com/kubernetes-sigs/kueue/issues/8712) issue means that we should not go on this direction
