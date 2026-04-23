# Issue #8782: v1beta2: use for e2e performance testing

**Summary**: v1beta2: use for e2e performance testing

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8782

**Last updated**: 2026-04-14T09:44:55Z

---

## Metadata

- **State**: open
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-01-26T11:37:03Z
- **Updated**: 2026-04-14T09:44:55Z
- **Closed**: —
- **Labels**: `kind/cleanup`
- **Assignees**: _none_
- **Comments**: 2

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

See example place: https://github.com/kubernetes-sigs/kueue/blob/main/test/performance/e2e/podgroups/templates/resource-flavor.yaml#L1

**Why is this needed**:

To migrate to v1beta2 consistently.

## Discussion

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-01-26T11:53:14Z

Oh, this is used for test Configuration. We should probably postpone it and switch to v1beta2 after we fully remove v1beta1.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-04-14T09:44:55Z

> We should probably postpone it and switch to v1beta2 after we fully remove v1beta1.

Why do we need to wait until v1beta1 is removed? Currently all supported branches of Kueue use v1beta2 for storage and serving, and so I think we could use that for the performance tests, wdyt?
