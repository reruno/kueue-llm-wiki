# Issue #8162: MultiKueue doesn't convey full up-to-date status upon workload suspension

**Summary**: MultiKueue doesn't convey full up-to-date status upon workload suspension

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8162

**Last updated**: 2025-12-19T07:22:40Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mwielgus](https://github.com/mwielgus)
- **Created**: 2025-12-10T11:03:14Z
- **Updated**: 2025-12-19T07:22:40Z
- **Closed**: 2025-12-19T07:22:40Z
- **Labels**: `kind/bug`
- **Assignees**: [@IrvingMg](https://github.com/IrvingMg)
- **Comments**: 1

## Description

**What happened**:

When a MK jobset workload is suspended, some of the status information may be not up to date:

```
spec:
  suspend: true
status:
  replicatedJobsStatus:
  - active: 1
    ready: 1
```

**What you expected to happen**:

There are no active and ready Jobs in Jobset when the whole thing is suspended.

**Environment**:

- Kueue version: 0.14.4

## Discussion

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2025-12-15T13:40:40Z

/assign
