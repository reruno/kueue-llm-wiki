# Issue #4919: Failing test: pull-kueue-test-e2e-multikueue-main

**Summary**: Failing test: pull-kueue-test-e2e-multikueue-main

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4919

**Last updated**: 2025-04-09T17:35:26Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kannon92](https://github.com/kannon92)
- **Created**: 2025-04-09T17:34:43Z
- **Updated**: 2025-04-09T17:35:26Z
- **Closed**: 2025-04-09T17:35:25Z
- **Labels**: _none_
- **Assignees**: _none_
- **Comments**: 1

## Description

We have https://testgrid.k8s.io/sig-scheduling#pull-kueue-test-e2e-multikueue-main failing on main.

There is no reporting on the tests run so it is difficult to see what is going wrong. Is it possible to expose junit on this job so we can see what tests are failing?

I realize that this is a presubmit so it may just be a PR..

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2025-04-09T17:35:25Z

okay.. this was just a flake actually..
