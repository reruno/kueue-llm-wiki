# Issue #7137: FlavorFungability: surface to the user why certain flavors where skipped

**Summary**: FlavorFungability: surface to the user why certain flavors where skipped

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7137

**Last updated**: 2025-11-26T17:02:38Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-10-02T11:59:38Z
- **Updated**: 2025-11-26T17:02:38Z
- **Closed**: 2025-11-26T17:02:38Z
- **Labels**: `kind/feature`
- **Assignees**: [@mykysha](https://github.com/mykysha)
- **Comments**: 2

## Description

**What would you like to be added**:

I would like to expose to the user information why other considered flavors where not selected. 

This could be either the message for the "Admitted" condition or the event (or both).

I would expect the message to be: 

`Workload is admitted to flavor "on-demand" as "Fit". "reservation" skipped as NoFit ..., "spot" skipped as "Preempt".`

Or something along the lines, but the idea is to surface the information "per-flavor". 

**Why is this needed**:

When a workload is admitted out messages (Admitted condition and Event) say "Admitted by ClusterQueue %v, wait time since reservation was 0s". However, users often want to understand why the flavor was selected and not others.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-02T11:59:55Z

cc @mwysokin @MichalZylinski @amy

### Comment by [@mykysha](https://github.com/mykysha) — 2025-10-02T13:03:47Z

/assign
