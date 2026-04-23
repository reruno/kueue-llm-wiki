# Issue #201: Update Workload Admitted condition to true on a best-effort basis.

**Summary**: Update Workload Admitted condition to true on a best-effort basis.

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/201

**Last updated**: 2022-04-13T18:22:46Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@ahg-g](https://github.com/ahg-g)
- **Created**: 2022-04-10T15:40:02Z
- **Updated**: 2022-04-13T18:22:46Z
- **Closed**: 2022-04-13T18:22:46Z
- **Labels**: `kind/feature`, `priority/important-soon`, `kind/ux`
- **Assignees**: [@kerthcet](https://github.com/kerthcet)
- **Comments**: 2

## Description

**What would you like to be added**:

Update the workload admitted condition to true when the workload gets admitted. Currently users can look at the admission field in the spec to check if a workload was admitted, we can sync that with the workload's admitted condition on a best effort basis. Meaning we can do it in the workload controller (we will get an event for the addition of the .spec.admission field).

**Why is this needed**:

Improves UX.

## Discussion

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-04-12T04:52:00Z

/assign

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-04-13T01:59:55Z

/kind ux
