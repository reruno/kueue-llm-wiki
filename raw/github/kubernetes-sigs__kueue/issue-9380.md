# Issue #9380: CI Job for e2e testing MultiKueue + TAS

**Summary**: CI Job for e2e testing MultiKueue + TAS

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9380

**Last updated**: 2026-03-03T15:09:25Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-02-19T18:53:32Z
- **Updated**: 2026-03-03T15:09:25Z
- **Closed**: 2026-03-03T15:09:25Z
- **Labels**: `kind/feature`
- **Assignees**: [@ikchifo](https://github.com/ikchifo)
- **Comments**: 2

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

A CI Job for provisioning and testing e2e the MultiKueue + TAS setup.


**Why is this needed**:

- to test the important two features combined
- to provide an easy to provision environment for manual testing which does not require manual maintanence, following the MultiKueue+DRA setup, see: https://github.com/kubernetes-sigs/kueue/pull/9308#issuecomment-3929236554

This could basically script the setup: https://kueue.sigs.k8s.io/docs/tasks/dev/setup_multikueue_development_environment/#setup-multikueue-with-tas

and we could setup just by `E2E_MODE=dev make kind-image-build test-multikueue-tas-e2e`

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-19T18:53:45Z

cc @olekzabl @kshalot @IrvingMg

### Comment by [@ikchifo](https://github.com/ikchifo) — 2026-02-20T03:22:22Z

/assign
