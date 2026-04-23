# Issue #9448: Allow configuring Kueue's controller loglevel in the helm chart

**Summary**: Allow configuring Kueue's controller loglevel in the helm chart

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9448

**Last updated**: 2026-03-17T14:27:44Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mwysokin](https://github.com/mwysokin)
- **Created**: 2026-02-24T10:59:08Z
- **Updated**: 2026-03-17T14:27:44Z
- **Closed**: 2026-03-17T14:27:44Z
- **Labels**: `kind/feature`
- **Assignees**: [@PrateekKumar1709](https://github.com/PrateekKumar1709)
- **Comments**: 2

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
An ability to change the desired loglevel for the Kueue controller while using the helm chart.

**Why is this needed**:
Users would like an ability to configure the loglevel in the helm chart as otherwise it requires a manual kubectl intervention.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@PrateekKumar1709](https://github.com/PrateekKumar1709) — 2026-02-25T06:17:59Z

/assign

### Comment by [@gabesaba](https://github.com/gabesaba) — 2026-03-17T13:29:47Z

@PrateekKumar1709 are you still working on this?
