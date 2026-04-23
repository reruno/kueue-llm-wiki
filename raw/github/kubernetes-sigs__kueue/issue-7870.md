# Issue #7870: MultiKueue: restrict access to the kueue-system namespace for ClusterProfiles

**Summary**: MultiKueue: restrict access to the kueue-system namespace for ClusterProfiles

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7870

**Last updated**: 2025-11-27T10:34:22Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-11-25T07:29:11Z
- **Updated**: 2025-11-27T10:34:22Z
- **Closed**: 2025-11-27T10:34:22Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 1

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

Restrict access to only the kueue-system namespace for ClusterProfiles, following https://github.com/kubernetes-sigs/kueue/pull/7188

**Why is this needed**:

To follow the principle of least privilege. Only access to kueue-system is required for the feature currently.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-25T07:30:07Z

/assign @mszadkow 
who is already working on the PR: https://github.com/kubernetes-sigs/kueue/pull/7843
cc @hdp617
