# Issue #5216: Expose a fast makefiile goal for only code generation from api

**Summary**: Expose a fast makefiile goal for only code generation from api

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5216

**Last updated**: 2025-05-29T15:16:19Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-05-09T10:35:15Z
- **Updated**: 2025-05-29T15:16:19Z
- **Closed**: 2025-05-29T15:16:19Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 2

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

To quickly generate code from api changes.

I would suggest to either introduce `make generate-code` or move apiref generation to another goal, like make generate-all.

**Why is this needed**:

For fast development, the bare minimum to be able to run unit and integration tests. 

Currently we have `make generate`, but:
- it is slow, because it does also refererence generation and kueuectl
- it fails even if the api is correct, just because the code does not compile

The apiref is regenerated less often typically, only before push to CI.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-09T10:36:15Z

cc @PBundyra @mbobrovskyi @mszadkow 
wdyt? I workaround this locally but removing the api-ref generation and docs generation from make generate.

### Comment by [@kannon92](https://github.com/kannon92) — 2025-05-09T12:27:22Z

Yes please!
