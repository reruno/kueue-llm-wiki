# Issue #2650: Make directive to update security insights

**Summary**: Make directive to update security insights

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2650

**Last updated**: 2024-07-26T15:48:30Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2024-07-19T15:03:40Z
- **Updated**: 2024-07-26T15:48:30Z
- **Closed**: 2024-07-26T15:48:30Z
- **Labels**: `kind/feature`
- **Assignees**: [@IrvingMg](https://github.com/IrvingMg)
- **Comments**: 1

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

`make update-security-insights` that updates the SECURITY_INSIGHTS.yaml file based on the GIT_TAG argument.

**Why is this needed**:

To automate the release process a little more and reduce chances of error.

See https://github.com/kubernetes-sigs/kueue/pull/2555 for an example

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-07-19T15:03:57Z

/assign @IrvingMg
