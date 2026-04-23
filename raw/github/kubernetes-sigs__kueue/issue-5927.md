# Issue #5927: Add unit tests for slice-only TAS scheduling

**Summary**: Add unit tests for slice-only TAS scheduling

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5927

**Last updated**: 2025-08-22T15:15:10Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@lchrzaszcz](https://github.com/lchrzaszcz)
- **Created**: 2025-07-10T08:15:52Z
- **Updated**: 2025-08-22T15:15:10Z
- **Closed**: 2025-08-22T15:15:10Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 2

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:
In this [PR](https://github.com/kubernetes-sigs/kueue/pull/5905) a fix to slice-only TAS scheduling has been introduced with a e2e test as a confirmation that the fix works. However it was also spotted that we should add lower-level tests for quicker feedback loop. We merged the PR anyway to deliver the fix, but as a follow-up it would be great to add the requested tests:
- Test for validation that Kueue takes into consideration slice-only topology (it was removing the whole `TopologyRequest` before)
- Test for `HasLevel` that it checks slice topology as well (it was checking only main topology before)

**Why is this needed**:
Slice-only topology with rank-ordering required changes with multiple places in the code. We do have e2e test for that, but in the future that might hard to debug failing e2e test. That is why we should introduce lower-level tests for more code-pieces of slice-only TAS scheduling.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-10T08:19:30Z

/retitle Add unit tests for slice-only TAS scheduling

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-08-21T12:15:11Z

/assign
