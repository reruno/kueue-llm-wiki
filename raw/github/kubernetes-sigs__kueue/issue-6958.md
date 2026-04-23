# Issue #6958: Follow-up for drop of the QueueVisibility feature

**Summary**: Follow-up for drop of the QueueVisibility feature

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6958

**Last updated**: 2025-09-24T13:20:55Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-09-23T11:48:39Z
- **Updated**: 2025-09-24T13:20:55Z
- **Closed**: 2025-09-24T07:42:24Z
- **Labels**: `kind/cleanup`
- **Assignees**: _none_
- **Comments**: 3

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:
We should clean up of QueueVisibility config validation codes: https://github.com/kubernetes-sigs/kueue/blob/b7cd74b0424928f1da26ae150abf1c0ca7e27902/pkg/config/validation.go#L165

**Why is this needed**:

We forgot to clean up those in https://github.com/kubernetes-sigs/kueue/pull/6631

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-09-23T11:49:08Z

cc @vladikkuzn @mbobrovskyi

### Comment by [@yankay](https://github.com/yankay) — 2025-09-24T09:37:44Z

Ref https://github.com/kubernetes-sigs/kueue/pull/6978#pullrequestreview-3261170524, There are docs that need to be dropped or change .

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-09-24T13:20:55Z

> Ref [#6978 (review)](https://github.com/kubernetes-sigs/kueue/pull/6978#pullrequestreview-3261170524), There are docs that need to be dropped or change .

Thank you!
