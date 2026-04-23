# Issue #8143: [Multikueue] Admission checks stuck to one cluster

**Summary**: [Multikueue] Admission checks stuck to one cluster

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8143

**Last updated**: 2025-12-09T12:38:09Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@yaroslava-serdiuk](https://github.com/yaroslava-serdiuk)
- **Created**: 2025-12-09T10:10:03Z
- **Updated**: 2025-12-09T12:38:09Z
- **Closed**: 2025-12-09T12:38:09Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 2

## Description

Context: The ProvisioningRequest admission controller failed (created ProvisioningRequest has failed status) in one cluster and it stuck on this cluster. 
Expectation: If the ProvisioningRequest admission controller failed in one cluster, kueue should try to create a ProvisioningRequest in another cluster.

## Discussion

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2025-12-09T12:35:55Z

This seems to be a duplicate of #8089.

### Comment by [@yaroslava-serdiuk](https://github.com/yaroslava-serdiuk) — 2025-12-09T12:38:09Z

Correct, thanks for noticing that!
