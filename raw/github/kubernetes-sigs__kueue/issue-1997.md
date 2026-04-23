# Issue #1997: Split Makefile

**Summary**: Split Makefile

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1997

**Last updated**: 2024-05-09T21:01:40Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2024-04-17T13:04:12Z
- **Updated**: 2024-05-09T21:01:40Z
- **Closed**: 2024-05-09T21:01:40Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@vladikkuzn](https://github.com/vladikkuzn), [@trasc](https://github.com/trasc)
- **Comments**: 3

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

We can at least split all tool installations to a separate Makefile (`build/tools`) and external CRDs (`build/crds`).

We can also consider the debug image in `build/debug`, although this is just one rule.

And finally, we can put the different test rules inside the `test` folder.

**Why is this needed**:

The Makefile is getting too big to follow. Since the Makefile sometimes serves as documentation for developers, it's still useful to have the widely used directives in the root file.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-04-17T13:04:34Z

/assign @trasc

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2024-04-26T11:51:23Z

/assign

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-04-26T14:41:52Z

When splitting the Makefile, keep in mind that there is CI job that depends on the current target: https://github.com/kubernetes/test-infra/blob/7520ad96a99792cf20e7ed6e2387589d2801952e/config/jobs/kubernetes-sigs/kueue/kueue-presubmits-main.yaml#L299

I think you can just leave the target with the same name and make it call the target in the other makefile.
