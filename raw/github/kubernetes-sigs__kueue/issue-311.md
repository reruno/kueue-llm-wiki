# Issue #311: Place webhook files under a separate folder

**Summary**: Place webhook files under a separate folder

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/311

**Last updated**: 2022-08-09T17:02:38Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kerthcet](https://github.com/kerthcet)
- **Created**: 2022-08-04T15:46:31Z
- **Updated**: 2022-08-09T17:02:38Z
- **Closed**: 2022-08-09T17:02:38Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 2

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
Currently we have webhooks for each type of Kueue Objs, maybe it's better to place them under a separate folder like `apis/kueue/webhooks/`, which seems more clearly.

**Why is this needed**:
Make the project more clearly.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-08-04T15:46:46Z

cc @ahg-g @alculquicondor For advices.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-08-04T17:56:30Z

+1
