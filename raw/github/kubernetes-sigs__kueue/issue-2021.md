# Issue #2021: [MultiKueue] Report ClusterQueue as inactive (misconfigured) if not applied to all flavors

**Summary**: [MultiKueue] Report ClusterQueue as inactive (misconfigured) if not applied to all flavors

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2021

**Last updated**: 2024-04-25T18:11:35Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-04-19T14:33:46Z
- **Updated**: 2024-04-25T18:11:35Z
- **Closed**: 2024-04-25T18:11:34Z
- **Labels**: `kind/feature`
- **Assignees**: [@IrvingMg](https://github.com/IrvingMg)
- **Comments**: 3

## Description

**What would you like to be added**:

Fail validation for ClusterQueue in case the MultiKueue admission check is configured only for a subset of flavors. 
This can be now done with a similar mechanism to this: https://github.com/kubernetes-sigs/kueue/issues/1913. 

**Why is this needed**:

The managedBy field is immutable, so we cannot change it per flavor. 
To fail fast and avoid debugging of customer issues when using MultiKueue for a subset of flavors.

**Proposed approach**

A mechanism similar to this one: https://github.com/kubernetes-sigs/kueue/pull/1635

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-04-19T14:34:02Z

/assign @trasc 
/cc @alculquicondor

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2024-04-22T08:25:10Z

/assign

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-04-22T14:45:08Z

as a clarification: an admission check applies to all flavors if the list in `onFlavors` is empty.
