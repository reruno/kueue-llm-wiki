# Issue #7942: MultiKueue via ClusterProfile: add lightweight e2e tests to confirm MultiKueueCluster loaded ClusterProfile

**Summary**: MultiKueue via ClusterProfile: add lightweight e2e tests to confirm MultiKueueCluster loaded ClusterProfile

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7942

**Last updated**: 2025-12-08T09:07:40Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-11-27T09:47:15Z
- **Updated**: 2025-12-08T09:07:40Z
- **Closed**: 2025-12-08T09:07:40Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 2

## Description

I would like to have e2e tests which would be good enough to confirm the ClusterProfile is loaded into memory and recognized by MultiKueueCluster instance, even if the MultiKueueCluster is inactive (no real connection).

It will be already useful for verifying permissions to read intances of ClusterProfiles related to https://github.com/kubernetes-sigs/kueue/issues/7870

Related to https://github.com/kubernetes-sigs/kueue/issues/7943 and https://github.com/kubernetes-sigs/kueue/issues/7850

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-27T09:47:25Z

cc @mszadkow @hdp617

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-12-02T13:48:04Z

/assign
