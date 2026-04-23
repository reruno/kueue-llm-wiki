# Issue #4615: Unexport Kueue

**Summary**: Unexport Kueue

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4615

**Last updated**: 2026-04-13T16:10:25Z

---

## Metadata

- **State**: open
- **Author**: [@gabesaba](https://github.com/gabesaba)
- **Created**: 2025-03-14T12:17:32Z
- **Updated**: 2026-04-13T16:10:25Z
- **Closed**: —
- **Labels**: `kind/cleanup`
- **Assignees**: _none_
- **Comments**: 18

## Description

**What would you like to be cleaned**:
We currently export Kueue as a library. By moving from `pkg` to `internal`, we can unexport it.

Let's discuss whether we want to do this. If so, we need to determine what actually needs to be exported, if anything (JobFramework?)

**Downsides:**
1. Disruptive to developers
2. Maybe docs disappear from https://pkg.go.dev/sigs.k8s.io/kueue@v0.10.2/pkg (maybe reappear in internal?)

I argue that these downsides are minimal, and it seems pretty straightforward: https://github.com/kubernetes-sigs/kueue/commit/52b75f17fa8c56586dbd8637aa841a2e4534c862

**Why is this needed**:
Prevent users from taking dependencies on Kueue internals

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-14T12:35:45Z

> Let's discuss whether we want to do this. If so, we need to determine what actually needs to be exported, if anything (JobFramework?)

At least, we want to expose utility functions so that the external JobFramework can leverage those.
However, I agree with moving core logic like queue and scheduler to internal.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-03-14T12:51:45Z

In `kjob`, we use constants such as labels and annotations from `/pkg/controller/constants` and utilities from `/pkg/util`.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-14T12:56:28Z

Declarations of labels and annotations should be moved to api packages, as these objects are anyway api surface, so hiding constants doesn't do good. Analogously we export labels as api constants in core k8s: https://github.com/kubernetes/kubernetes/blob/611abd3bcdeb8ee513ab7814c4ac251575e48cbd/pkg/apis/batch/types.go#L26-L56

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-14T13:41:34Z

> Declarations of labels and annotations should be moved to api packages, as these objects are anyway api surface, so hiding constants doesn't do good. Analogously we export labels as api constants in core k8s: https://github.com/kubernetes/kubernetes/blob/611abd3bcdeb8ee513ab7814c4ac251575e48cbd/pkg/apis/batch/types.go#L26-L56

We want to select labels and annotations that we need to expose since I guess all labels and annotations do not need to be exposed, right?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-14T13:47:57Z

> We want to select labels and annotations that we need to expose since I guess all labels and annotations do not need to be exposed, right?

Maybe, probably alpha-level labels & annots don't need to be exposed.
Certainly all labels & annotations used by kjob should be exposed, so that we don't use the util package.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-14T13:50:17Z

Opened the issue for kjob: https://github.com/kubernetes-sigs/kjob/issues/79, it will require both PRs in Kueue and kjob

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2025-03-18T19:00:33Z

fwiw, in the AppWrapper 1.0.x branch (which is AppWrapper as an external framework against Kueue 0.10), we imported the following Kueue packages:
```
	utilslices "sigs.k8s.io/kueue/pkg/util/slices"
	utilmaps "sigs.k8s.io/kueue/pkg/util/maps"
	"sigs.k8s.io/kueue/pkg/podset"
	"sigs.k8s.io/kueue/pkg/controller/jobframework"
```

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-19T07:38:12Z

Packages representing APIs and jobfframework will continue to be exported. 

However the other packages like utils for maps we will unexport at some point, so I would suggest to migrate away from them in AppWrapper, as we did in kjob. So that at least the project we know about don't use the packages which are going to be unexported.

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2025-03-19T13:50:56Z

> Packages representing APIs and jobfframework will continue to be exported.
> 
> However the other packages like utils for maps we will unexport at some point, so I would suggest to migrate away from them in AppWrapper, as we did in kjob. So that at least the project we know about don't use the packages which are going to be unexported.

Right.  We did eliminate imports of the all the non-API packages in AppWrapper 0.11 (built against Kueue 0.11.0-rc.0).   Part of that was having our own copy of `maps.MergeKeepFirst` and `maps.HaveConflict` because AppWrapper needs that functionality internally to provide the utility used by`RunWithPodSetsInfo`.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-06-17T13:59:21Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle stale`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-06-17T14:00:04Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-09-15T14:33:39Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle stale`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-15T14:48:06Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-12-14T15:14:09Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle stale`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-01-13T16:02:43Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle rotten

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-01-13T16:07:26Z

/remove-lifecycle rotten

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-04-13T16:08:48Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle stale`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@mimowo](https://github.com/mimowo) — 2026-04-13T16:10:22Z

/remove-lifecycle stale
