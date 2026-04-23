# Issue #1913: Support  AdmissionCheck per ResourceFlavors

**Summary**: Support  AdmissionCheck per ResourceFlavors

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1913

**Last updated**: 2024-03-27T08:38:59Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@PBundyra](https://github.com/PBundyra)
- **Created**: 2024-03-26T11:13:09Z
- **Updated**: 2024-03-27T08:38:59Z
- **Closed**: 2024-03-27T08:38:59Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 2

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

AdmissionCheck per ResourceFlavors

**Why is this needed**:

Introduce the ability to configure AdmissionChecks at the ResourceFlavor level, instead of solely at the ClusterQueue level. This allows for fine-grained control over which workload types undergo specific admission checks.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-03-26T20:30:44Z

@PBundyra What is the difference between this and https://github.com/kubernetes-sigs/kueue/issues/1432?

### Comment by [@PBundyra](https://github.com/PBundyra) — 2024-03-27T08:38:59Z

> @PBundyra What is the difference between this and #1432?

That's actually a duplicate. Thank you for pointing this out.
