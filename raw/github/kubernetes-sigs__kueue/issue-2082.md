# Issue #2082: Expand documentation for adding an custom Job type to Kueue via external controller

**Summary**: Expand documentation for adding an custom Job type to Kueue via external controller

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2082

**Last updated**: 2024-05-13T17:49:42Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@dgrove-oss](https://github.com/dgrove-oss)
- **Created**: 2024-04-26T17:32:21Z
- **Updated**: 2024-05-13T17:49:42Z
- **Closed**: 2024-05-13T17:49:42Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 3

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Rework the [page on adding a custom job type to Kueue](https://kueue.sigs.k8s.io/docs/tasks/dev/integrate_a_custom_job/) to equally describe adding an external extension. 

**Why is this needed**:

Kueue actually supports external extension fairly well and documenting it would help grow the community. 

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ x ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2024-04-26T17:36:44Z

I'm planning to do this based on our experience with building the AppWrapper controller.  The main question I had was whether you would prefer the final doc to be one page with 2 sections or a short summary page with two child pages each giving the details of internal and external.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-05-01T11:38:37Z

> I'm planning to do this based on our experience with building the AppWrapper controller. The main question I had was whether you would prefer the final doc to be one page with 2 sections or a short summary page with two child pages each giving the details of internal and external.

@dgrove-oss IMO, we depend on the amount of differences between the existing integration approach (https://kueue.sigs.k8s.io/docs/tasks/dev/integrate_a_custom_job/) and new external integration.

@alculquicondor @mimowo Any thought?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-01T13:13:01Z

The existing page looks small enough, so maybe it would be fine to add it there. But don't stress about it and open a new page if it feels right.
