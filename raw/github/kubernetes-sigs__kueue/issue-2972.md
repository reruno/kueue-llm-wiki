# Issue #2972: [kueuectl] Show DURATION column with the Job runtime to complete

**Summary**: [kueuectl] Show DURATION column with the Job runtime to complete

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2972

**Last updated**: 2024-09-04T15:54:55Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-09-04T09:18:28Z
- **Updated**: 2024-09-04T15:54:55Z
- **Closed**: 2024-09-04T15:54:55Z
- **Labels**: `kind/feature`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 2

## Description

**What would you like to be added**:

A new `DURATION` column in the `kueuectl list workload`. The value is computed from the last admission timestamp to 
completion timestamp for finished jobs. For running jobs we can compute as the time from the last admission timestamp to now. The column is empty for Pending workloads.

**Why is this needed**:

To inform the user about the actual runtime of a Job. 
Currently only age is available which tells the time from creation to now.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-04T09:18:47Z

/cc @mwielgus @mwysokin @trasc @mbobrovskyi

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-09-04T09:28:53Z

/assign
