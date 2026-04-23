# Issue #9052: e2e testing: load images into kind worker nodes in parallel

**Summary**: e2e testing: load images into kind worker nodes in parallel

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9052

**Last updated**: 2026-02-20T10:29:41Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-02-09T08:12:45Z
- **Updated**: 2026-02-20T10:29:41Z
- **Closed**: 2026-02-20T10:29:41Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@vladikkuzn](https://github.com/vladikkuzn)
- **Comments**: 2

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

Looking at the function to load images: https://github.com/kubernetes-sigs/kueue/blob/1d93e45b8edac98851e05b9186058f3a7f9fe3a5/hack/e2e-common.sh#L363-L386

I think we could load the images in parallel.
This will require calling `docker save "$2"` prior to the parallel loading.

**Why is this needed**:

To improve time to setup the cluster for testing. This especially will matter for TAS e2e tests which create 8 worker nodes.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-09T08:12:53Z

cc @vladikkuzn @mbobrovskyi

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2026-02-11T11:28:35Z

/assign
