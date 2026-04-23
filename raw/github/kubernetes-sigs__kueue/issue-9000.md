# Issue #9000: Update dependencies for Kueue populator

**Summary**: Update dependencies for Kueue populator

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9000

**Last updated**: 2026-02-05T12:38:33Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-02-05T08:41:45Z
- **Updated**: 2026-02-05T12:38:33Z
- **Closed**: 2026-02-05T12:38:33Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@IrvingMg](https://github.com/IrvingMg)
- **Comments**: 2

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

Update dependencies for kueue populator.


**Why is this needed**:

- It is currently using Kueue 0.14 which is out of support and old controller-runtime. 
- the upgrade Prs by dependabot are blocked and so the future will be

See blocked PRs:
- https://github.com/kubernetes-sigs/kueue/pull/8956
- https://github.com/kubernetes-sigs/kueue/pull/8957

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-05T08:42:01Z

cc @j-skiba @mbobrovskyi @mszadkow ptal

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-02-05T08:44:10Z

/assign @IrvingMg 

Who is working on it.
