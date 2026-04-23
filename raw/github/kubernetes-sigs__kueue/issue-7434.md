# Issue #7434: Add integration test for using MultiKueue and ProvReq controllers

**Summary**: Add integration test for using MultiKueue and ProvReq controllers

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7434

**Last updated**: 2025-11-05T08:08:58Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-10-30T07:50:39Z
- **Updated**: 2025-11-05T08:08:58Z
- **Closed**: 2025-11-05T08:08:58Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@IrvingMg](https://github.com/IrvingMg)
- **Comments**: 2

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

I would like to have an integration test which uses both MultiKueue and ProvReq.

Ideally if we could reproduce the registration conflict for indexers as discovered in this bug https://github.com/kubernetes-sigs/kueue/pull/7432 (by reverting the fix but adding the test).

**Why is this needed**:

To reproduce reliably the bug which was discovered late after release when we started testing on GKE.

## Discussion

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2025-10-30T08:09:27Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-30T08:11:55Z

cc @mwysokin
