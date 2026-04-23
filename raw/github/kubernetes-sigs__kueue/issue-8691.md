# Issue #8691: Concurrent Admission (Alpha)

**Summary**: Concurrent Admission (Alpha)

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8691

**Last updated**: 2026-01-28T17:06:20Z

---

## Metadata

- **State**: open
- **Author**: [@PBundyra](https://github.com/PBundyra)
- **Created**: 2026-01-20T11:16:04Z
- **Updated**: 2026-01-28T17:06:20Z
- **Closed**: —
- **Labels**: `kind/feature`
- **Assignees**: [@PBundyra](https://github.com/PBundyra)
- **Comments**: 2

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
I'd like to have ability to schedule a Workload on multiple ResourceFlavors at the same time. Additionally, I'd like to have capability to express what should happen if a Workload has been admitted a particular ResourceFlavor, and migrate to a more preferable ResourceFlavor if necessary

**Why is this needed**:

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@PBundyra](https://github.com/PBundyra) — 2026-01-20T14:52:12Z

/assign

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2026-01-28T16:42:10Z

> I'd like to have ability to schedule a Workload on multiple ResourceFlavors at the same time.

Could you please clarify "at the same time".
Does it mean workload requested quota resources can spawn multiple Resource Flavors (RFs)?
I.E.: WL(100cpu) -> RF1(40cpu) + RF2(60cpu)

Or, does it mean that workload is reserving identical quota in both RFs?
I.E. WL(100cpu) -> RF1(100cpu) and RF2(100cpu)

--- 
Update: found the answer in KEP.
