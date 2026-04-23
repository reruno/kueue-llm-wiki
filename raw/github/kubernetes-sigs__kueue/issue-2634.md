# Issue #2634: Crash server on error in CreateAndStartVisibilityServer.

**Summary**: Crash server on error in CreateAndStartVisibilityServer.

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2634

**Last updated**: 2024-07-18T13:33:03Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2024-07-18T11:03:34Z
- **Updated**: 2024-07-18T13:33:03Z
- **Closed**: 2024-07-18T13:33:03Z
- **Labels**: `kind/feature`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 5

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
Use `os.Exit(1)` on error in `CreateAndStartVisibilityServer`.

**Why is this needed**:
The current silencing of the error is not the best. 

https://github.com/kubernetes-sigs/kueue/blob/dac07e65a3be053dfac3d21a3fade4c4991a6995/pkg/visibility/server.go#L51-L53

Some users may need it, Kueue will start for them but not work as expected.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-07-18T11:04:00Z

cc @mimowo @alculquicondor

### Comment by [@mimowo](https://github.com/mimowo) — 2024-07-18T11:25:57Z

+1 I like crashing (calling exit).

The only consideration from me is when users cannot configure visibility correctly, and they don't care about it, they would like to still be able to run Kueue. However, I expect we will get this kind of feedback before graduating to stable, and until then such users will have an option to disable by the feature gate.

cc @PBundyra

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-07-18T12:12:40Z

Have you seen this error happening in the wild? I wonder what are common scenarios that could lead to it.

Nevertheless, I think it's safer to crash.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-07-18T12:20:44Z

I didn't see it

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-07-18T12:35:43Z

/assign
