# Issue #8860: TAS: support ResourceTransformations

**Summary**: TAS: support ResourceTransformations

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8860

**Last updated**: 2026-03-05T10:28:21Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-01-28T15:34:55Z
- **Updated**: 2026-03-05T10:28:21Z
- **Closed**: 2026-03-05T10:28:21Z
- **Labels**: `kind/feature`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 4

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

I would like to be able to configure ResourceTransformations with custom "credits" resource, using ResourceGroups.

Currently, the credits approach, as detailed in https://github.com/kubernetes-sigs/kueue/issues/5877#issuecomment-3150075310 does not work with TAS.

This is because we assume TAS always has only one flavor: https://github.com/kubernetes-sigs/kueue/blob/51c7da0b46d40871677098cb3000630f0e3b39bb/pkg/scheduler/flavorassigner/tas_flavorassigner.go#L77


**Why is this needed**:

To enable putting one limit on all TPUs/GPUs across all flavors. For example, I may have 3 models of GPU, each with 50 quota, but I want to have a common cap that 100 GPUs might be used total.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-28T15:35:09Z

/assign 
tentatively

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-28T16:55:50Z

Strongly +1!

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-29T10:45:26Z

/assign @mbobrovskyi 
transferring assignment to Mike who agreed to take it
/unassign

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-29T10:47:27Z

I have done some initial investigation and I think we don't need new API. The most important assumption we need to relax is in the function `onlyFlavor`, because now we may have multiple flavors. I think we should have a function like `onlyTASFlavor`. 
We may also need to tweak a couple of other places, but I would like to suggest starting with integration tests (TDD way) to identify the places and adjust one-by-one. Happy to drive the process.

I hope maybe @sohankunkerkar could also help reviewing here.
