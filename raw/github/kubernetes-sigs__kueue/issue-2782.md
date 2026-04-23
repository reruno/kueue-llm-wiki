# Issue #2782: shell-check errors introduced in kjobctl PRs break PR builds

**Summary**: shell-check errors introduced in kjobctl PRs break PR builds

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2782

**Last updated**: 2024-08-06T17:12:52Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-08-06T16:03:16Z
- **Updated**: 2024-08-06T17:12:52Z
- **Closed**: 2024-08-06T17:12:52Z
- **Labels**: _none_
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 1

## Description

The PR with docs update failed on shell-check errors: https://github.com/kubernetes-sigs/kueue/pull/2781.

This is because the PR https://github.com/kubernetes-sigs/kueue/pull/2642 merged files failing the recently added shell-check which is verified in `pull-kueue-verify-main`. This was possible because PRs to kjobctl don't run `pull-kueue-verify-main`.

The PR https://github.com/kubernetes-sigs/kueue/pull/2780 mitigates this issue, but we should make sure that
kjobctl PRs don't break merging other PRs.

The idea for fix is:
- exclude kjobctl from `pull-kueue-verify-main`
- add a dedicated step during kjobctl to verify shell-check (and potentially other stuff checked in `pull-kueue-verify-main`)

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-08-06T16:03:26Z

/assign @mbobrovskyi
