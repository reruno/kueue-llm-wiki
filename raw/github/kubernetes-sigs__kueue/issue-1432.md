# Issue #1432: AdmissionChecks should be configurable per flavor

**Summary**: AdmissionChecks should be configurable per flavor

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1432

**Last updated**: 2024-04-16T14:57:34Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2023-12-08T16:54:04Z
- **Updated**: 2024-04-16T14:57:34Z
- **Closed**: 2024-04-16T14:57:34Z
- **Labels**: `kind/feature`
- **Assignees**: [@PBundyra](https://github.com/PBundyra)
- **Comments**: 4

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Allow AdmissionChecks to be required for a Workload if it gets assigned a specific flavor.

**Why is this needed**:

The user might want to only issue a ProvisioningRequest if targeting a specific flavor, or might want different engines.

**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [x] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-12-08T16:54:14Z

cc @mwielgus

### Comment by [@maci0](https://github.com/maci0) — 2023-12-28T03:06:35Z

+1

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-03-27T03:25:17Z

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

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-03-27T14:13:19Z

/assign @PBundyra 

/remove-lifecycle stale
