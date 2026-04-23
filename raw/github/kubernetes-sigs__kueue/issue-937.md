# Issue #937: Add unit coverage for flavorassigner and scheduler when there are reclaimed pods

**Summary**: Add unit coverage for flavorassigner and scheduler when there are reclaimed pods

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/937

**Last updated**: 2023-07-05T15:56:59Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2023-06-30T14:07:58Z
- **Updated**: 2023-07-05T15:56:59Z
- **Closed**: 2023-07-05T15:56:59Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 1

## Description

**What would you like to be cleaned**:

`.status.admission.podsetAssigment[*].Count` depend on the reclaimed pods.

Also cover in an integration test that:

1. admits a workload
2. completes/reclaims some pods
3. gets evicted
4. gets readmitted

**Why is this needed**:

Better coverage and also to verify if #934 is making the right assumptions.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-06-30T14:08:12Z

/assign @trasc
