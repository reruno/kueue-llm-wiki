# Issue #9145: Introduce a test to reproduce conversion webhooks on 0.15

**Summary**: Introduce a test to reproduce conversion webhooks on 0.15

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9145

**Last updated**: 2026-03-04T12:03:02Z

---

## Metadata

- **State**: open
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-02-12T09:09:34Z
- **Updated**: 2026-03-04T12:03:02Z
- **Closed**: —
- **Labels**: `kind/feature`
- **Assignees**: [@mykysha](https://github.com/mykysha), [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 3

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

An automated test which would reproduce the issues with conversion webhooks at scale encountered in 0.15

See the scenario: https://github.com/kubernetes/kubernetes/issues/136950#issuecomment-3889610473

**Why is this needed**:

To help to guide the graduation of the ConcurrentWatchObjectDecode feature gate in k8s core: https://github.com/kubernetes/kubernetes/issues/136950

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-12T09:09:56Z

@tenzen-y @gabesaba @IrvingMg cc @mbobrovskyi

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-02-12T09:15:30Z

/assign

### Comment by [@mykysha](https://github.com/mykysha) — 2026-03-04T12:03:02Z

/assign
