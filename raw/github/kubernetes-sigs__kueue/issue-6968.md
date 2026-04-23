# Issue #6968: Namespaced Secret access

**Summary**: Namespaced Secret access

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6968

**Last updated**: 2025-10-16T08:08:09Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@sbgla-sas](https://github.com/sbgla-sas)
- **Created**: 2025-09-23T15:26:23Z
- **Updated**: 2025-10-16T08:08:09Z
- **Closed**: 2025-10-16T08:08:09Z
- **Labels**: `kind/feature`
- **Assignees**: [@sbgla-sas](https://github.com/sbgla-sas)
- **Comments**: 4

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Narrower access to Secrets granted to the `kueue-controller-manager` service account when using the Kueue Helm chart.

**Why is this needed**:

The current Helm chart templates grant the `kueue-controller-manager` cluster-wide access (get, list, update, watch) to Secrets. I may be missing something, but from what I can see Kueue interacts only with secrets in its own namespace for:

* Cert generation/rotation if using internal certificate management.
* Obtaining the kubeconfig(s) for worker clusters if using MultiKueue.

If the above is indeed the case it would be good to follow the principle of least privilege and restrict access to Secrets in the Kueue system namespace only, in a similar way to the existing `leader-election-role` Role and RoleBinding for ConfigMaps and Leases.

**Completion requirements**:

* Move Kueue controller manager Secret permissions from the existing ClusterRole to a namespaced Role.
* Bind the Role to the Kueue controller manager service account.

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@sbgla-sas](https://github.com/sbgla-sas) — 2025-09-23T15:27:34Z

Happy to contribute a PR, of course.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-23T15:30:19Z

cc @kannon92

### Comment by [@kannon92](https://github.com/kannon92) — 2025-09-23T18:13:26Z

Makes sense to me.

Please make sure the namespace is configurable based on install. We don't want to hardcode kueue-system anywhere.

### Comment by [@sbgla-sas](https://github.com/sbgla-sas) — 2025-10-07T10:32:00Z

/assign
