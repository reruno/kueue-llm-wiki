# Issue #1461: Automatically sync webhookConfigurations to helm charts

**Summary**: Automatically sync webhookConfigurations to helm charts

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1461

**Last updated**: 2024-01-29T12:41:53Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2023-12-15T14:46:52Z
- **Updated**: 2024-01-29T12:41:53Z
- **Closed**: 2024-01-29T12:41:53Z
- **Labels**: `kind/feature`
- **Assignees**: [@B1F030](https://github.com/B1F030)
- **Comments**: 2

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
We should implement scripts to sync webhookConfigurations to helm charts and validate automatically.

**Why is this needed**:
To avoid forgetting to sync webhookConfigurations to helm charts.

ref: https://github.com/kubernetes-sigs/kueue/issues/1407

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@B1F030](https://github.com/B1F030) — 2024-01-09T03:26:50Z

Hi! I wirte a PR to resolve this, can you take a look? @tenzen-y

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-01-10T10:29:59Z

/assign @B1F030
