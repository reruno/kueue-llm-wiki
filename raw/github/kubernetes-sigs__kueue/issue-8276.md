# Issue #8276: LWS unnecessary performance impact of using Pod finalizers

**Summary**: LWS unnecessary performance impact of using Pod finalizers

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8276

**Last updated**: 2026-01-13T15:07:40Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-12-16T15:06:35Z
- **Updated**: 2026-01-13T15:07:40Z
- **Closed**: 2026-01-13T15:07:40Z
- **Labels**: `kind/bug`, `priority/important-longterm`
- **Assignees**: _none_
- **Comments**: 4

## Description

**What happened**:

LWS integration is slower than it could if we eliminated managing of Pod finalizers.

**What you expected to happen**:

No need to manage Pod finalizers for LWS.

**Anything else we need to know?**:

Inspired by https://github.com/kubernetes-sigs/kueue/pull/8267, and possibly will be fixed by the PR. See comment https://github.com/kubernetes-sigs/kueue/pull/8267#discussion_r2623640784

I expect the analogous change should be possible for StatefulSet.

To make this change safe to cherrypick we may need a feature gate like `PodIntegrationSkipFinalizersForBuiltInWorkloads`

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-16T15:07:16Z

cc @mbobrovskyi @j-skiba @PBundyra

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-12-18T05:40:50Z

Probably it could be related https://github.com/kubernetes-sigs/kueue/issues/5298.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T09:28:32Z

/priority important-longterm

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-09T14:49:09Z

Root issue https://github.com/kubernetes-sigs/kueue/issues/5298
